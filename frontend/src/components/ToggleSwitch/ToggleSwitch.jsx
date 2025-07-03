import React from "react";
import "./ToggleSwitch.css";

const ToggleSwitch = ({ label, onChange, disabled, checked }) => {
    return (
        <>
        <div className="toggle-switch-div">
            <span>{`${label} `}{'\u00A0'}</span>
            <div className="toggle-switch">
                <input 
                type="checkbox" 
                className="toggle-switch-checkbox" 
                name={label} 
                id={label}
                checked={checked}
                onChange={onChange} 
                disabled={disabled}></input>
                <label className={disabled? "label-disabled" : "label"} htmlFor={label}>
                    <span className="inner"></span>
                    <span className="switch"></span>
                </label>
            </div>
        </div>
        
        </>
    );
};

export default ToggleSwitch; 