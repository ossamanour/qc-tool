import React, { useEffect, useState } from "react";
import SingleTask from "../../../../components/SingleTask/SingleTask";

const Zoning = ({ setComplete, setInformation, taskId }) => {
    const [moduleList, setModuleList] = useState([
        {id: 0, name: "body-sidebar", progress: 0}, 
        {id: 1, name: "body-ocr", progress: 0},
        {id: 2, name: "info-gen", progress: 0},
        {id: 3, name: "zoning", progress: 0},
    ]);
    // const [progress, setProgress] = useState(0);

    // useEffect(() => {
    //     const doneModule = moduleList.filter(module => module.progress === 1)
    //     setProgress(doneModule.length);
    // }, [moduleList]);

    return (
        <div>
            {/* <progress max={moduleList.length} value={progress}></progress> */}
            <SingleTask 
            moduleList={moduleList} 
            setModuleList={setModuleList} 
            setComplete={setComplete} 
            setInformation={setInformation} 
            taskId={taskId} 
            taskName="Zoning"></SingleTask>
        </div>
    );
};

export default Zoning;