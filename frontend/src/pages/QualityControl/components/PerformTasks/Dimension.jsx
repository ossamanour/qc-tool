import React, { useState } from "react";
import SingleTask from "../../../../components/SingleTask/SingleTask";

const Dimension = ({ setComplete, setInformation, taskId }) => {
    const [moduleList, setModuleList] = useState([
        {id: 0, name: "body-sidebar", progress: 0}, 
        {id: 1, name: "body-ocr", progress: 0},
        {id: 2, name: "arrow-gen", progress: 0},
        {id: 3, name: "dimension-gen", progress: 0}, 
        {id: 4, name: "scale-gen", progress: 0}, 
        {id: 5, name: "dimension-qc", progress: 0},
    ]);

    return (
        <SingleTask
        moduleList={moduleList} 
        setModuleList={setModuleList} 
        setComplete={setComplete} 
        setInformation={setInformation} 
        taskId={taskId} 
        taskName="Dimension"></SingleTask>
    );
};

export default Dimension;