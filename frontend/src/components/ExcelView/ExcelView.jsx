import React, { useState } from "react";
import TableView from "../TableView/TableView";

const ExcelView = ({ header, tables }) => {
    const [activateTab, setActiveTab] = useState("onsite");

    return (
        <div>
            <div>
                <button onClick={() => setActiveTab("onsite")}>onsite</button>
                <button onClick={() => setActiveTab("offsite")}>offsite</button>
            </div>

            {activateTab === "onsite" && 
            <TableView 
            header={header} 
            table={tables.onsite}></TableView>}

            {activateTab === "offsite" && 
            <TableView 
            header={header} 
            table={tables.offsite}></TableView>}
        </div>
    );
};

export default ExcelView;