from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from functools import singledispatch
from typing import Any, Dict, List, Optional, Type, Union
from uuid import uuid4

import attr

from src.converters import Converters
from src.database import get_database
from src.enums.job_status import JobStatus
from src.gpu import GPU
from src.types import ABCJob
from src.user import User


@singledispatch
def _load_gpus_list(arg: Any) -> List[GPU]:
    raise NotImplementedError(f"Unexpected arg: {arg} ({type(arg)})")


@_load_gpus_list.register(list)
def _load_gpus_list_as_is(arg: List[GPU]) -> List[GPU]:
    return arg


@_load_gpus_list.register(str)
def _load_gpus_list_json_string(arg: str) -> List[GPU]:
    res: Any = json.dumps(arg)
    if isinstance(res, list):
        _list: List[GPU] = [gpu
                            for gpu in map(GPU.load, res)
                            if gpu is not None]
        return _list

    raise NotImplementedError(f"Unexpected decoded arg: {res} ({type(res)})")


@attr.define(slots=False, frozen=False)
class Job(ABCJob):
    name: str
    script_path: str
    cli_args: str = ''
    uuid: str = attr.ib(factory=lambda: str(uuid4().hex))

    user: Optional[User] = attr.ib(
        default=None,
        converter=User.load,
    )
    gpus_list: List[GPU] = attr.ib(
        default=[],
        converter=_load_gpus_list
    )

    start_time: Optional[datetime] = attr.ib(
        default=None,
        converter=Converters.optional_datetime,
    )
    finish_time: Optional[datetime] = attr.ib(
        default=None,
        converter=Converters.optional_datetime,
    )
    duration_ms: Optional[int] = None

    status: JobStatus = attr.ib(
        default=JobStatus.QUEUED,
        converter=lambda v: JobStatus(v)
    )

    def job_start(self, time: Optional[datetime] = None):
        self.start_time = time or datetime.now()

    def job_finished(self, time: datetime):
        self.finish_time = time
        assert self.start_time is not None
        self.duration_ms = int((time - self.start_time).total_seconds())

    def get_id(self) -> str:
        return self.uuid

    def get_DB_key(self) -> str:
        return self._get_DB_key(self.get_id())

    @staticmethod
    def _get_DB_key(uuid: str) -> str:
        return f'-Job-{uuid}'

    def to_dict(self) -> Dict[str, Union[str, int, Dict[str, Any]]]:
        _dict: Dict[str, Union[str, Enum]] = attr.asdict(
            self,
            filter=lambda a, v: v is not None,
        )
        return dict([
            (k, v.value if isinstance(v, Enum) else v)
            for k, v in _dict.items()
        ])

    def dump(self) -> Dict[str, Union[str, float, Optional[int]]]:
        @singledispatch
        def _converters(arg: Any) -> Union[str, float, Optional[int]]:
            raise NotImplementedError(f"Unexpected arg: {arg} ({type(arg)})")

        @_converters.register(str)
        @_converters.register(int)
        @_converters.register(type(None))
        def _converters_as_is(arg: Union[str, Optional[int]]):
            return arg

        @_converters.register(Enum)
        def _converters_enum(arg: Enum) -> str:
            return arg.value

        @_converters.register(datetime)
        def _converters_datetime(arg: datetime) -> float:
            return arg.timestamp()

        @_converters.register(list)
        def _converters_list(args: List[GPU]) -> str:
            _list: List[str] = [arg.get_id() for arg in args]
            print(f"_converters_list({_list})")
            return json.dumps(_list)

        @_converters.register(User)
        def _converters_user(arg: User) -> str:
            return arg.get_id()

        _dict: Dict[str, Union[str, float, Optional[int]]]
        _dict = attr.asdict(
            self,
            filter=lambda a, v: v is not None,
            recurse=False,
            value_serializer=lambda inst, a, v: _converters(v),
        )

        return _dict

    @staticmethod
    def from_dict(dict: Dict[str, Any]):
        return Job(**dict)

    @classmethod
    def load(cls, arg: Any) -> Optional[Job]:
        return load(arg, cls)


@singledispatch
def load(arg: Any, cls: Type[GPU]) -> Optional[Job]:
    raise NotImplementedError(f"Unexpected arg: {arg} ({type(arg)})")


@load.register(str)
def _load_str(arg: str, cls: Type[GPU]) -> Optional[Job]:
    key: str = cls._get_DB_key(arg)
    _data: Dict[str, Union[str, float, Optional[int]]]
    _data = get_database().fetch_key(key)

    if _data == {}:
        return None

    return cls(**_data)


@load.register
def _load_user(arg: Job, cls: Type[GPU]) -> Optional[Job]:
    return arg
