import React, { useState } from "react";
import RegisterForm from "./RegisterForm";
import LoginForm from "./LoginForm";
import "./AuthenticateModule.css";

const AuthenticateModule = () => {
    const [login, setLogin] = useState(true);

    return (
        <div className="auth-container">
            {login ? 
            <LoginForm switchFunc={() => setLogin(!login)}></LoginForm> :
            <RegisterForm switchFunc={() => setLogin(!login)}></RegisterForm> }
        </div >
    );
};

export default AuthenticateModule;