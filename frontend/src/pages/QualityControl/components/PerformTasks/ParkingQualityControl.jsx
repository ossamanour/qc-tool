import React, { useEffect, useState } from "react";
import useStore from "../../../../components/store/store";
import commonStyles from "../../../../components/commonStyle";

const ParkingQualityControl = ({setComplete, setInformation, taskId}) => {
    const [moduleList, setModuleList] = useState([
        {id: 0, name: "parking-quality-control", progress: 0},
    ]);
    const [landuse, setLanduse] = useState();
    const [variableDict, setVaraibleDict] = useState();
    const [conditionDict, setConditionDict] = useState();
    const [startInput, setStartInput] = useState(false);

    const landuseInputChange = (event) => {
        event.preventDefault();

        if (event.target.value === "") {
            setStartInput(false);
            setVaraibleDict();
            setConditionDict();
        } else {
            setLanduse(event.target.value);
        }
    };

    const initializeVariableDict = (inputList) => {
        const tempDict = inputList.reduce((obj, item) => {
            obj[item] = "";
            return obj
        }, {});
        setVaraibleDict(tempDict)
    };

    const setVariableDictValue = (key, value) => {
        setVaraibleDict(prevDict => ({
            ...prevDict, 
            [key]: value,
        }));
    };

    const setConditionDictValue = (key, value) => {
        setConditionDict(prevDict => ({
            ...prevDict, 
            [key]: value,
        }));
    };

    const initializeCondtionDict = (inputList) => {
        const tempDict = inputList.reduce((obj, item) => {
            obj[item] = "";
            return obj
        }, {});
        setConditionDict(tempDict)
    };

    const landuseSubmit = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                '/api/communicate/parking-landuse', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(landuse)});
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                initializeVariableDict(data.variableList);
                initializeCondtionDict(data.conditionList);
                setStartInput(true);
            } else {    
                alert(data.errorMessage);
            };
        } catch(error) {
            console.log(error);
        };
    }; 

    const checkOnClick = async(event) => {
        event.preventDefault();

        const sendData = {
            "landuse": landuse, 
            "variableDict": variableDict, 
            "conditionDict": conditionDict
        };

        try {
            const response = await fetch(
                '/api/communicate/parking-check', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(sendData)});
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setInformation(taskId, data.message);
            } else {    
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
        setComplete();
    };

    useEffect(() => {
        setModuleList(prevList => prevList.map(task => task.id == 0 ? {...task, progress: null} : task))
    }, []);

    return (
        <div>
            <h3>Parking Quality Control</h3>
            <ul>
                {moduleList.map((module, index) => (
                    <li key={index} style={commonStyles.listItem}>
                        <div style={commonStyles.itemColumn}>{module.name}</div>
                        <div style={commonStyles.itemColumn}>
                            <progress value={module.progress}></progress>
                            <div>
                                <span>Input Landuse: </span>
                                <input 
                                type="text" 
                                onChange={(e) => landuseInputChange(e)}></input>
                                <br></br>
                                <button onClick={(e) => landuseSubmit(e)}>Submit</button>
                            </div>
                            {startInput && <>
                                <span>Input the necessary information</span>
                                <br></br>
                                <span>**Variables**</span>
                                <ul>
                                    {Object.keys(variableDict).map((key, index) => (
                                        <li key={index}>
                                            <span>{key} </span>
                                            <br></br>
                                            <input
                                            type="text" 
                                            onChange={(e) => setVariableDictValue(key, e.target.value)}></input>
                                        </li>
                                    ))}
                                </ul>
                                <span>**Conditions**</span>
                                <ul>
                                    {Object.keys(conditionDict).map((key, index) => (
                                        <li key={index}>
                                            <span>{key} </span>
                                            <br></br>
                                            <input
                                            type="text" 
                                            onChange={(e) => setConditionDictValue(key, e.target.value)}></input>
                                        </li>
                                    ))}
                                </ul>
                                <button onClick={checkOnClick}>Submit</button>
                            </>}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ParkingQualityControl;