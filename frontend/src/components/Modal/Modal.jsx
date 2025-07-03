import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClose } from "@fortawesome/free-solid-svg-icons";
import "./Modal.css"

const Modal = ({ title, onClose, onSubmit, children }) => {
    
    return (
        <>
        <div 
        className="modal-container"
        onClick={(e) => {
            if (e.target.className === "modal-container") {onClose()};
        }}>
            <div className="modal-main">
                <div className="modal-header">
                    <span className="modal-title">{title}</span>
                    <button 
                    className="icon_button"
                    onClick={onClose}>
                        <FontAwesomeIcon icon={faClose} />
                    </button>
                </div>
                <div className="modal-body">
                    {children}
                </div>
                {onSubmit ? 
                <div className="modal-footer">
                    <button 
                    className="modal-button" 
                    onClick={onSubmit}>
                        Submit
                    </button>
                    {"\u00A0"}
                    <button 
                    className="modal-button"
                    onClick={() => {onClose()}}>
                        Cancel
                    </button>
                </div> : <></>}
            </div>
        </div>
        </>
    );
};

export default Modal; 