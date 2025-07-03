import React, { useEffect, useState } from "react";
import useStore from "../../../../components/store/store";
import commonStyles from "../../../../components/commonStyle";

const ParkingQualityControl = ({setComplete, setInformation, taskId}) => {
    const [moduleList, setModuleList] = useState([
        {id: 0, name: "parking-quality-control", progress: 0},
    ]);

    const [startInput, setStartInput] = useState(false);
    const {chatbotInUse} = useStore();

    const [usageType, setUsageType] = useState("");
    const [usageList, setUsageList] = useState([]);
    const [selectedUsage, setSelectedUsage] = useState("");

    const [startParam, setStartParam] = useState(true);
    const [paramList, setParamList] = useState([]);
    const [statement, setStatement] = useState("");

    const [conditionLevel1, setConditionLevel1] = useState(false);
    const [conditionStr1, setConditionStr1] = useState("");
    const [choiceState1, setChoiceState1] = useState([]);
    const [selectedChoice1, setSelectedChoice1] = useState("");

    const [conditionLevel2, setConditionLevel2] = useState(false);
    const [conditionStr2, setConditionStr2] = useState("");
    const [choiceState2, setChoiceState2] = useState([]);
    const [selectedChoice2, setSelectedChoice2] = useState("");


    useEffect(() => {
        setModuleList(prevList => prevList.map(task => task.id == 0 ? {...task, progress: null} : task))

        const getUsageType = async() => {
            const sendData = {"chatboatInUse": chatbotInUse};

            try {
                const response = await fetch(
                    '/api/communicate/parking-landuse', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(sendData)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                setStartInput(true);
                setUsageType(data["usageType"]);
                setUsageList(data["usageList"]);
            } catch(error) {
                console.log(error);
            };
        };

        getUsageType();
    }, []);

    const handleUsageChange = async(event) => {
        setSelectedUsage(event.target.value);

        setConditionLevel1(false);
        setConditionStr1("");
        setChoiceState1([]);
        setSelectedChoice1("");

        setConditionLevel2(false);
        setConditionStr2("");
        setChoiceState2([]);
        setSelectedChoice2("");

        setStartParam(false);
        setParamList([]);
        setStatement("");

        if (event.target.value != "") {
            const send_data = {"selectedUsage": event.target.value};

            try {
                const response = await fetch(
                    '/api/communicate/parking-condition1', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(send_data)});
                if (!response.ok) {
                    if (response.status == 400) {
                        alert("Not support");
                    };
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                if (!data["simpleStatement"]) {
                    setConditionLevel1(true);
                    setConditionStr1(data["conditionStr"]);
                    setChoiceState1(data["choiceState"]);
                } else {
                    setStartParam(true);
                    setParamList(data.paramList)
                    setStatement(data["statement"]);
                };
            } catch(error) {
                console.log(error);
            };
        };
    };

    const handleCondition1Change = async(event) => {
        setSelectedChoice1(event.target.value);

        setConditionLevel2(false);
        setConditionStr2("");
        setChoiceState2([]);
        setSelectedChoice2("");

        setStartParam(false);
        setParamList([]);
        setStatement("");

        if (event.target.value != "") {
            const send_data = {
                "selectedChoice": event.target.value, 
                "choiceState": choiceState1
            };

            try {
                const response = await fetch(
                    '/api/communicate/parking-condition2', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(send_data)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                if (!data["simpleStatement"]) {
                    setConditionLevel2(true);
                    setConditionStr2(data["conditionStr"]);
                    setChoiceState2(data["choiceState"]);
                } else {
                    setStartParam(true);
                    setParamList(data.paramList)
                    setStatement(data["statement"]);
                };
            } catch(error) {
                console.log(error);
            };
        };
    };

    const handleCondition2Change = async(event) => {
        setSelectedChoice2(event.target.value);

        setStartParam(false);
        setParamList([]);
        setStatement("");

        if (event.target.value != "") {
            const send_data = {
                "selectedChoice": event.target.value,
                "choiceState": choiceState2
            };

            try {
                const response = await fetch(
                    '/api/communicate/parking-paramlist', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(send_data)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                setStartParam(true);
                setParamList(data.paramList)
                setStatement(data["statement"]);
            } catch(error) {
                console.log(error);
            };
        };
    };

    const handleInputChange = (index, value) => {
        const newParamList = [...paramList];
        newParamList[index].value = value;
        setParamList(newParamList);
    };

    const handleSubmit = async(event) => {
        event.preventDefault();

        const hasEmptyFieldParamList = paramList.some(item => item.value === "");

        if (hasEmptyFieldParamList) {
            alert("Please fill all required field!");
        } else {
            const send_data = {
                "statement": statement, 
                "paramList": paramList, 
                "chatbotInUse": chatbotInUse
            }
    
            try {
                const response = await fetch(
                    '/api/communicate/parking-check', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(send_data)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
            } catch(error) {
                console.log(error);
            };
        };
        
    };
    
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
                        {startInput && <>
                            <span>Select {usageType}</span>
                            <select
                            value={selectedUsage}
                            onChange={(e) => handleUsageChange(e)}
                            style={{width: "250px"}}>
                                <option value=""> Select an option</option>
                                {usageList.map((usage, index) => (
                                    <option key={index} value={usage}>{usage}</option>
                                ))}
                            </select>
                        </>}
                            {conditionLevel1 && <>
                                <span>{conditionStr1}</span>
                                <select
                                value={selectedChoice1} 
                                onChange={(e) => handleCondition1Change(e)}
                                style={{width: "250px"}}>
                                    <option value="">Select an option</option> 
                                    {choiceState1.map((choice, index1) => (
                                        <option key={index1} value={choice.key}>{choice.key}</option>
                                    ))}
                                </select>
                            </>}
                            {conditionLevel2 && <>
                                <span>{conditionStr2}</span>
                                <select 
                                value={selectedChoice2} 
                                onChange={(e) => handleCondition2Change(e)} 
                                style={{width: "250px"}}>
                                    <option value="">Select an option</option>
                                    {choiceState2.map((choice, index2) => (
                                        <option key={index2} value={choice.key}>{choice.key}</option>
                                    ))}
                                </select>
                            </>}
                            {startParam && <>
                                <ul>
                                    {paramList.map((param, index3) => (
                                        <li key={index3}>
                                            <span>{param.name}</span>
                                            <input type="text"
                                            onChange={(e) => handleInputChange(index3, e.target.value)}></input>
                                        </li>
                                    ))}
                                </ul>
                                <button onClick={handleSubmit}>Submit</button>
                            </>}
                            </div>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ParkingQualityControl;