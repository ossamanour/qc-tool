import React, { useState } from "react";
import DropDownSubMenu from "../../../../components/DropDownSubMenu/DropDownSubMenu";
import InformationPanel from "../../../../components/InformationPanel/InformationPanel";
import SessionConfigSetting from "./SessionConfigSetting";
import ChatBotToggle from "../../../../components/ChatBotToggle/ChatBotToggle";
import TaskSelector from "../TaskSelector/TaskSelector";
import PerformTasksParent from "../PerformTasks/PerformTasksParent";
import Modal from "../../../../components/Modal/Modal";
import ExcelView from "../../../../components/ExcelView/ExcelView";
import ReportGenerator from "../../../../components/ReportGenerator/ReportGenerator";

const SideBar = () => {
    const [tableViewModalOpen, setTableViewModalOpen] = useState(false);
    const [priceSheetHeader, setPriceSheetHeader] = useState([]);
    const [priceSheetViewTable, setPriceSheetViewTable] = useState({
        onsite: [], 
        offsite: []
    });

    const viewCurrentCostTable = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                '/api/pricesheet/load_current', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}});
            if (!response.ok) {
                throw new Error(response.statusText);
            };
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setPriceSheetHeader(data.sheetHeader);
                setPriceSheetViewTable(prev => ({...prev, onsite: data.onsiteSheet}));
                setPriceSheetViewTable(prev => ({...prev, offsite: data.offsiteSheet})); 
                setTableViewModalOpen(true);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

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
            <br></br>
            <button onClick={viewCurrentCostTable}>View Cost Table</button>
            {tableViewModalOpen && <Modal
            title="Cost Estimate Table" 
            onClose={() => setTableViewModalOpen(false)}>
                <ExcelView 
                header={priceSheetHeader} 
                tables={priceSheetViewTable}></ExcelView>
            </Modal>}
        </DropDownSubMenu>

        <DropDownSubMenu title="Results">
            <ReportGenerator></ReportGenerator>
        </DropDownSubMenu>
        </>
    );
};

export default SideBar;