import React, { useState } from "react";
import useStore from "../../../../components/store/store";
import "./AuthenticateModule.css";

const RegisterForm = ({ switchFunc }) => {
    const {setIsAuthenticated, setUsername} = useStore();
    const [formData, setFormData] = useState({
        email: "", 
        username: "", 
        password: "", 
        confirmPassword: "", 
        registrationCode: ""
    });
    const [passwordError, setPasswordError] = useState(false);

    const handleFormChange = (event) => {
        setFormData({...formData, [event.target.name]: event.target.value});
        if (event.target.name == "confirmPassword") {
            if (event.target.value != formData.password) {
                setPasswordError(true);
            } else {
                setPasswordError(false);
            };
        };
    };       

    const registerClick = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                '/api/auth/register', {
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

                <label htmlFor="username">User Name:</label>
                <input 
                type="text" 
                name="username" 
                placeholder="username" 
                value={formData.username} 
                onChange={handleFormChange}></input>

                <label htmlFor="password">Password:</label>
                <input 
                type="password" 
                name="password" 
                placeholder="password" 
                value={formData.password} 
                onChange={handleFormChange}></input>

                <label htmlFor="confirmPassword">Confirm Password:</label>
                <input 
                type="password" 
                name="confirmPassword" 
                placeholder="confirm password" 
                value={formData.confirmPassword} 
                onChange={handleFormChange}></input>

                <label htmlFor="registrationCode">Registration Code</label>
                <input 
                type="text" 
                name="registrationCode" 
                placeholder="registration code" 
                value={formData.registrationCode} 
                onChange={handleFormChange}></input>
                {passwordError && <p className="error-message">Password not match</p>}
            </form>
            <br></br>
            <button
            className="auth-button" 
            type="submit" 
            onClick={registerClick}>Sign Up</button>
        </div>
        <div className="side-container">
            <p>Welcome</p>
            <button 
            className="auth-button"
            onClick={switchFunc}>Sign In</button>
        </div>
        </>
    );
};

export default RegisterForm;