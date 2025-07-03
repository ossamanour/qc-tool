import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCaretDown, faCaretUp } from "@fortawesome/free-solid-svg-icons";
import "./DropDownSubMenu.css";

const DropDownSubMenu = ({ title, children }) => {
    const [menuExpand, setMenuExpand] = useState(true); 

    return (
        <>
        <div className="sub-menu-container">
            <div 
            className="toggle-button"
            onClick={() => setMenuExpand(!menuExpand)}>
                {title}
                <FontAwesomeIcon className="expand-icon" 
                icon={menuExpand ? faCaretDown : faCaretUp} />
            </div>
            <div 
            className="menu-form" 
            style={{display: menuExpand ? "block" : "none"}}>
                {children}
            </div>
        </div>
        
        </>
    );
};
 
export default DropDownSubMenu;