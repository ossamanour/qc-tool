import React, { useState } from "react";
import SingleTask from "../../../../components/SingleTask/SingleTask";

const Parking = ({setComplete, setInformation, taskId}) => {
    const [moduleList, setModuleList] = useState([
        {id: 0, name: "body-sidebar", progress: 0}, 
        {id: 1, name: "body-ocr", progress: 0},
        {id: 2, name: "parking-count", progress: 0},
    ]);

    return (
        <SingleTask 
        moduleList={moduleList} 
        setModuleList={setModuleList} 
        setComplete={setComplete} 
        setInformation={setInformation} 
        taskId={taskId} 
        taskName="Parking"></SingleTask>
    );
};

export default Parking;