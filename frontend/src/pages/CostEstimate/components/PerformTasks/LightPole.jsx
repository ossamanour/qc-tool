import React, { useState } from "react";
import SingleTask from "../../../../components/SingleTask/SingleTask";

const LightPole = ({setComplete, setInformation, taskId}) => {
    const [moduleList, setModuleList] = useState([
        {id: 0, name: "body-sidebar", progress: 0}, 
        {id: 1, name: "body-ocr", progress: 0},
        {id: 2, name: "keynote-gen", progress: 0}, 
        {id: 3, name: "keynote-match-pre", progress: 0},
        {id: 4, name: "costestimate-prepare", progress: 0}, 
        {id: 5, name: "light-pole", progress: 0},
    ]);

    return (
        <SingleTask
        moduleList={moduleList} 
        setModuleList={setModuleList} 
        setComplete={setComplete} 
        setInformation={setInformation} 
        taskId={taskId} 
        taskName="Light Pole"></SingleTask>
    );
};

export default LightPole;