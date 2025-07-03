import React, { useEffect, useState } from "react";
import CompanySelector from "../../../../components/SessionConfigSetting/CompanySelector";
import KeynoteSelector from "../../../../components/SessionConfigSetting/KeynoteSelector";

const SessionConfigSetting = () => {
    const [selectedCompany, setSelectedCompany]  = useState();
    const [selectedkeynote, setSelectedKeynote] = useState();

    const submitOnClick = async(event) => {
        event.preventDefault();

        const sendData = {
            company: selectedCompany.value, 
            keynote: selectedkeynote.value, 
        }
        try {
            const response = await fetch(
                '/api/config/generate', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify(sendData)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                };
                const data = await response.json();
                console.log(data);
                if (data.status) {
                    window.location.reload();
                    alert("config updated");
                } else {
                    alert(data.errorMessage);
                };
        } catch (error) {
            console.log(error);
        };
    };
    
    return (
        <>
        <CompanySelector 
        value={selectedCompany} 
        setValue={setSelectedCompany}></CompanySelector>
        
        <KeynoteSelector
        value={selectedkeynote} 
        setValue={setSelectedKeynote}></KeynoteSelector>

        <button onClick={submitOnClick}>Generate Config</button>

        <br></br>
        </>
    );
};

export default SessionConfigSetting;