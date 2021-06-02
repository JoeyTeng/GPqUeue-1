import React from "react";
import {Route, BrowserRouter as Router, Link} from "react-router-dom";
import "./App.css";

const NavbarLink = (props) => {
    return (
        <li className="nav-item">
            <Link className="nav-link active" to={props.to}>{props.text}</Link>
        </li>
    );
};

const Navbar = () => {
    return (
        <React.Fragment>
            <nav className="navbar navbar-expand-xxl navbar-light bg-light">
                <div className="container-fluid">
                    <Link className="navbar-brand" to="/">GPqUeue</Link>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <NavbarLink to="/overview" text="Overview"/>
                            <NavbarLink to="/myexperiments" text="My Experiments"/>
                            <NavbarLink to="/gpus" text="GPUs" />
                        </ul>
                        <Link to="/newexperiment">
                            <button className="btn btn-primary">
                                New Experiment
                            </button>
                        </Link>
                    </div>
                </div>
            </nav>
        </React.Fragment>
    );
};

const Login = () => {
    return (
        <div>
            <h1>Login</h1>
        </div>
    );
};

const GPUCard = (props) => {
    const icon = props.user == "" ? "" : "busy.png";
    const user = props.user == "" ? "Available" : props.user;

    return (
        <div className="row border mb-3">
            <div className="icon-col align-self-center pt-3 mb-3 me-3">
                <img className="icon" src={icon} />
            </div>
            <div className="col pt-3">
                <h3>GPU {props.key} - {props.name}</h3>
                <p>{user}</p>
            </div>
            <div className="col pt-3 me-3 text-end">
                <p>Utilisation: {props.util}%</p>
                <p>Memory: {props.memory} / {props.maxMemory} MiB</p>
            </div>
        </div>
    );
};

const GPUOverview = (props) => {
    const gpuCards = props.gpuData.map((data, index) =>
        <GPUCard key={index} name={data.name} user={data.user} util={data.util} memory={data.memory} maxMemory={data.maxMemory} />
    );

    return (
        <div>
            <div className="row">
                <div className="col">
                    <h2>GPU Loads</h2>
                </div>
                <div className="col text-end">
                    <div className="dropdown">
                        <button className="btn btn-outline-primary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Sort by
                        </button>
                        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                            <li><a className="dropdown-item" href="#">Utilisation</a></li>
                            <li><a className="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            {gpuCards}
        </div>
    );
};

const Overview = () => {
    const gpuData = [
        {name: "RTX 3060", user: "Delilah Han", util: 50, memory: 7432, maxMemory: 11019},
        {name: "RTX 2080 Ti", user: "", util: 4, memory: 500, maxMemory: 11019},
        {name: "V100", user: "Joe Stacey", util: 74, memory: 12302, maxMemory: 15258},
    ];

    return (
        <div className="container-md">
            <h1 className="pt-4 mb-4">Overview</h1>
            <GPUOverview gpuData={gpuData} />
        </div>
    );
};

const MyExperiments = () => {
    return (
        <div>
            <h1>My Experiments</h1>
        </div>
    );
};

const Gpus = () => {
    return (
        <div>
            <h1>GPUs</h1>
        </div>
    );
};

const NewExperiment = () => {
    return (
        <div>
            <h1>New Experiment</h1>
        </div>
    );
};

const App = () => {
    const routing = (
        <Router>
            <Navbar/>
            <div className="container">
                <Route exact path="/" component={Login}></Route>
                <Route exact path="/overview" component={Overview}></Route>
                <Route exact path="/myexperiments" component={MyExperiments}></Route>
                <Route exact path="/gpus" component={Gpus}></Route>
                <Route exact path="/newexperiment" component={NewExperiment}></Route>
            </div>
        </Router>
    );

    return (
        <div>
            {routing}
        </div>
    );
};

export default App;
