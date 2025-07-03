import React from "react";
import DropDownSubMenu from "../../../../components/DropDownSubMenu/DropDownSubMenu";
import InformationPanel from "../../../../components/InformationPanel/InformationPanel";
import ChatBotToggle from "../../../../components/ChatBotToggle/ChatBotToggle";
import SessionConfigSetting from "./SessionConfigSetting";
import TaskSelector from "./TaskSelector";
import PerformTasksParent from "../PerformTasks/PerformTasksParent";
import ReportGenerator from "../../../../components/ReportGenerator/ReportGenerator";

const SideBar = () => {
    return (
        <>
        <DropDownSubMenu title="Information">
            <InformationPanel></InformationPanel>
        </DropDownSubMenu>

        <DropDownSubMenu title="Setting">
            <SessionConfigSetting></SessionConfigSetting>
        </DropDownSubMenu>

        <DropDownSubMenu title="Perform Tasks">
            {/* <ChatBotToggle></ChatBotToggle> */}
            <TaskSelector></TaskSelector>
            <PerformTasksParent buttonIcon="Perform Tasks"></PerformTasksParent>
        </DropDownSubMenu>

        <DropDownSubMenu title="Results">
            <ReportGenerator></ReportGenerator>
        </DropDownSubMenu>
        </>
    );
};

export default SideBar;