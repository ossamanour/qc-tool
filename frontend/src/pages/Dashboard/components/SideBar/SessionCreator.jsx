import React, { useRef, useState } from "react";
import useStore from "../../../../components/store/store";
import { faFolderOpen, faUpload, faSpinner } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Navigate, useNavigate } from "react-router-dom";

const SessionCreator = ({ navigateTo }) => {
    const [file, setFile] = useState(null);
    const [sessionName, setSessionName] = useState("session name");
    const [inProcess, setInProcess] = useState(false);
    const fileInputRef = useRef(null);
    const navigate = useNavigate();

    const handleFileChoose = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = async(event) => {
        const file = event.target.files[0];
        setFile(file);
        setSessionName(file.name.replace(".pdf", ""));
    };

    const uploadFile = async(event) => {
        event.preventDefault();

        const uploadFmData = new FormData();
        uploadFmData.append("file", file);
        uploadFmData.append("sessionName", sessionName);

        setInProcess(true);

        try {
            const response = await fetch(
                '/api/session/create', {
                    method: "POST", 
                    credentials: "include", 
                    body: uploadFmData
                }); 
            setInProcess(false);
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                console.log(data);
                navigate(navigateTo);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <>
        <form>
            <label>Select File: </label>
            <button onClick={handleFileChoose}>
                <FontAwesomeIcon icon={faFolderOpen} />
            </button>
            <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange}
            style={{display: "none"}}></input>
            <br></br>
            <label>Session Name: </label>
            <input 
            type="text" 
            name="sessionName" 
            placeholder={sessionName} 
            onChange={(e) => setSessionName(e.target.value)}></input>
        </form>
        <button 
        type="submit" 
        onClick={uploadFile}>
            <FontAwesomeIcon icon={faUpload} />
        </button> 
        {"\u00A0"}
        {inProcess ? <FontAwesomeIcon icon={faSpinner} className="fa-spin" /> : <></>}
        </>
    );
};

export default SessionCreator;