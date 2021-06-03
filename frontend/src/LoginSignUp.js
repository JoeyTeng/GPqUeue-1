import {Link} from "react-router-dom";
import "./LoginSignUp.css";

const Login = () => {
    return (
        <div className="container login">
            <h1 className="pt-4 mb-4">Login</h1>
            <form action="/api/login" >
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input type="text" className="form-control" id="username" />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input type="password" className="form-control" id="password" />
                </div>
                <button type="submit" className="btn btn-primary login-button">Login</button>
            </form>
            <div className="text-center pt-3">
                <Link to="signup">Or create an account</Link>
            </div>
        </div>
    );
};

const SignUp = () => {
    return (
        <div>

        </div>
    );
};

export {Login, SignUp};
