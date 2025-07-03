import React, { useState } from "react";
import TaskSelectorContainer from "../../../../components/TaskSelectorContainer/TaskSelectorContainer";
import useStore from "../../../../components/store/store";
import OnsiteTaskSelector from "./OnsiteTaskSelector";
import OffsiteTaskSelector from "./OffsiteTaskSelector";

const TaskSelector = () => {
    const [activateTab, setActiveTab] = useState("onsite");

    return (
        <div>
            <div>
                <button onClick={() => setActiveTab("onsite")}>onsite</button>
                <button onClick={() => setActiveTab("offsite")}>offsite</button>
            </div>

            {activateTab === "onsite" && 
            <OnsiteTaskSelector></OnsiteTaskSelector>}

            {activateTab === "offsite" && 
            <OffsiteTaskSelector></OffsiteTaskSelector>}
        </div>
    );
};

export default TaskSelector;