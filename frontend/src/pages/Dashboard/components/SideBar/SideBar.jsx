import React from "react";
import DropDownSubMenu from "../../../../components/DropDownSubMenu/DropDownSubMenu";
import SessionCreator from "./SessionCreator";

const SideBar = ({ navigateTo }) => {
    return (
        <>
        <DropDownSubMenu title="Create New Session">
            <SessionCreator navigateTo={navigateTo}></SessionCreator>
        </DropDownSubMenu>
        </>
    );
};

export default SideBar;