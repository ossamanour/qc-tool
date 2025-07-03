import React from "react";
import { useNavigate } from "react-router-dom";
import useStore from "../store/store";

const InformationPanel = () => {
    const {currentApp, currentSession} = useStore();
    const navigate = useNavigate();

    return (
        <>
        <div style={{margin: "0", padding: "0"}}>
            Session Name: {currentSession.session_name}
        </div>
        <div style={{margin: "0", padding: "0"}}>
            Input File: {currentSession.filename}
        </div>
        <button onClick={(e) => navigate(`/${currentApp}/dashboard`)}>Go To Dashboard</button>
        </>
    );
};

export default InformationPanel;