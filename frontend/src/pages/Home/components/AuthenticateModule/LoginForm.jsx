import React, { useState } from "react";
import useStore from "../../../../components/store/store";
import "./AuthenticateModule.css";

const LoginForm = ({ switchFunc }) => {
    const {setIsAuthenticated, setUsername} = useStore();
    const [formData, setFormData] = useState({
        email: "", 
        password: "", 
    });
    
    const handleFormChange = (event) => {
        setFormData({...formData, [event.target.name]: event.target.value});
    };   

    const loginClick = async(event) => {
        event.preventDefault();
        try {
            const response = await fetch(
                '/api/auth/login', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(formData)
                }); 
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setIsAuthenticated(data.isAuthenticated);
                setUsername(data.username);
            } else {    
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };
    
    return (
        <>
        <div className="form-container">
            <form className="form-css">
                <label htmlFor="email">E-mail:</label>
                <input 
                type="text" 
                name="email" 
                placeholder="email" 
                value={formData.email} 
                onChange={handleFormChange}></input>

                <label htmlFor="password">Password:</label>
                <input 
                type="password" 
                name="password" 
                placeholder="password" 
                value={formData.password} 
                onChange={handleFormChange}></input>
            </form>
            <br></br>
            <button
            className="auth-button" 
            type="submit" 
            onClick={loginClick}>Sign In</button>
        </div>
        <div className="side-container">
            <p>Welcome Back</p>
            <button 
            className="auth-button" 
            onClick={switchFunc}>Sign Up</button>
        </div>
        </>
    );
};

export default LoginForm;