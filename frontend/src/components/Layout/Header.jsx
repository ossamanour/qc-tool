import React from "react";
import { useNavigate } from "react-router-dom";
import useStore from "../store/store";
import logoImg from "../../assets/AIAEC-logo.png";
import "./Layout.css";

const Header = ({ taskName }) => {
    const {isAuthenticated, setIsAuthenticated, username} = useStore();
    const navigate = useNavigate();

    const logoOnClick = (event) => {
        navigate("/");
    };

    const logoutOnClick = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                `/api/auth/logout`, {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}
                });
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setIsAuthenticated(data.isAuthenticated);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <>  
            <div className="logo-div" onClick={logoOnClick}>
                <img src={logoImg} className="logo-img"></img>
                AIAEC
            </div>

            <div className="task-div">{taskName}</div>

            {isAuthenticated ? 
            <div className="header-user">
                <button>{username}</button>
                <button onClick={logoutOnClick}>Log Out</button>
            </div> : <div className="header-user">
                no user
            </div>}
        </>
    );
};

export default Header;