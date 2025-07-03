import React from "react";
import { faCopyright, faRegistered, faTrademark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import ToggleSwitch from "../ToggleSwitch/ToggleSwitch";
import useStore from "../store/store";

const Footer = () => {
    const {testMode, setTestMode} = useStore();

    return (
        <>
            <div style={{left: "5px", position: "absolute"}}>
                <ToggleSwitch 
                label="Test Mode"
                onChange={() => setTestMode(!testMode)} 
                checked={testMode}></ToggleSwitch>
            </div>
            <b>AIAEC</b><sup><FontAwesomeIcon icon={faTrademark} /></sup>
        </>
    );
};

export default Footer;