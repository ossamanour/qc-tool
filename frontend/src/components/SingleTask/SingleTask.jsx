import React, { useEffect, useState } from "react";
import useStore from "../store/store";
import commonStyles from "../commonStyle";

const SingleTask = ({moduleList, setModuleList, setComplete, setInformation, taskId, taskName}) => {
    const {moduleFetchData, setKeynoteNumber, setTaskLog} = useStore();
    const [progress, setProgress] = useState(0);

    const setSubProgress = (id, value) => {
        setModuleList(prevList => prevList.map(
            module => module.id === id ? {...module, progress: value} : module))
    };

    useEffect(() => {
        const performSingleTask = async() => {
            let data;
            for (let i = 0; i < moduleList.length; i++) {
                setSubProgress(i, null);
                data = await moduleFetchData(moduleList[i].name);
                setSubProgress(i, 1)
                if (data.message) {
                    setInformation(taskId, data.message);
                    setTaskLog(data.message);
                }
                if (moduleList[i].name == "keynote-match-prepare") {
                    if (data.keynoteNum) {
                        setKeynoteNumber(data.keynoteNum);
                    }
                }
            }
            setComplete();
        };

        performSingleTask();
    }, []);

    useEffect(() => {
        const doneModule = moduleList.filter(module => module.progress === 1)
        setProgress(doneModule.length);
    }, [moduleList]);

    return (
        <div>
            <h3>{taskName}</h3>
            <progress max={moduleList.length} value={progress}></progress>
            {/* <ul>
                {moduleList.map((module, index) => (
                    <li key={index} style={commonStyles.listItem}>
                        <div style={commonStyles.itemColumn}>{module.name}</div>
                        <div style={commonStyles.itemColumn}><progress value={module.progress}></progress></div>
                    </li>
                ))}
            </ul> */}
        </div>
    );
};

export default SingleTask;