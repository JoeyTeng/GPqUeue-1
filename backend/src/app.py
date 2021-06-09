import os
from typing import Any, Dict, Optional

from flask import Flask, request
from flask_login import LoginManager, current_user, login_required

import src.auth
from src.database import get_database, setup_database
from src.enums.job_status import JobStatus
from src.gpu import GPU
from src.job import Job
from src.mocked_gpu import MockedGPU
from src.user import User

app = Flask(__name__)
app.secret_key = '0785f0f7-43fd-4148-917f-62f915d94e38'  # a random uuid4
app.register_blueprint(src.auth.bp)

login_manager = LoginManager()
login_manager.init_app(app)

HAS_GPU = ((os.environ.get("gpu") or '').lower() in ('true', '1', 't'))
GPU_DCT: Dict[str, GPU] = {}


@login_manager.user_loader
def load_user(username) -> Optional[User]:
    return User.load(username)


@app.before_first_request
def get_gpus():
    if not HAS_GPU:
        mock_available_gpus()
    else:
        pass


@app.before_first_request
def setup_redis():
    setup_database()


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/available_gpus")
def get_available_gpu_names() -> Dict[str, Any]:
    return {'gpus': list(GPU_DCT.keys())}


@app.route("/gpu_stats")
def get_gpu_stats() -> Dict[str, Dict[str, Any]]:
    result = {}
    for gpu_name, gpu in GPU_DCT.items():
        result[gpu_name] = gpu.get_stats()
    return result


@app.route("/finished_jobs")
@login_required
def get_finished_jobs() -> Dict[str, Any]:
    return {"jobs": get_database().fetch_all_matching('status', JobStatus.COMPLETED.value)
            + get_database().fetch_all_matching('status', JobStatus.FAILED.value)}


@app.route("/ongoing_jobs")
@login_required
def get_ongoing_jobs() -> Dict[str, Any]:
    return {"jobs": get_database().fetch_all_matching('status', JobStatus.QUEUED.value)
            + get_database().fetch_all_matching('status', JobStatus.RUNNING.value)}


@app.route("/add_job", methods=['POST'])
@login_required
def add_new_job() -> Dict[str, Any]:
    name = request.json.get('experiment_name')
    script_path = request.json.get('script_path')
    cli_args = request.json.get('cli_args')
    user: User = current_user

    job = Job(name, script_path, cli_args, user=user)
    get_database().add_key(job.get_DB_key(), job.dump())
    return {"status": "success"}


def mock_available_gpus():
    global GPU_DCT
    GPU_DCT.update({
        "0": MockedGPU(name="0", model="mockedGPU", total_memory_mib=12000),
        "1": MockedGPU(name="1", model="mockedGPU", total_memory_mib=10000),
        "2": MockedGPU(name="2", model="mockedGPU", total_memory_mib=8000),
        "3": MockedGPU(name="3", model="mockedGPU", total_memory_mib=16000)
    })
