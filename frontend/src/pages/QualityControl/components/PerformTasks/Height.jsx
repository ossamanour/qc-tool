import React, { useEffect, useState } from "react";
import useStore from "../../../../components/store/store";
import commonStyles from "../../../../components/commonStyle";

const Height = ({setComplete, setInformation, taskId}) => {
    const [moduleList, setModuleList] = useState([
        {id: 0, name: "building-height", progress: 0},
    ]);

    const [paramRequirement, setParamRequirement] = useState([]);
    const [startInput, setStartInput] = useState(false);

    const {chatbotInUse} = useStore();

    useEffect(() => {
        const getAllRequiredParams = async() => {
            const send_data = {"chatbotInUse": chatbotInUse}

            try {
                const response = await fetch(
                    '/api/communicate/height-param-gen', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(send_data)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data.paramRequirementList);
                setParamRequirement(data.paramRequirementList.map((param) => ({
                    key: param.key, 
                    choiceState: param.choiceState, 
                    choices: param.choices, 
                    selected: "", 
                    paramList: [], 
                    maximumHeightLimit: param.maximumHeightLimit, 
                    value: "", 
                    statement: ""
                })));
                setStartInput(true);
            } catch(error) {
                console.log(error);
            };
        }; 

        getAllRequiredParams();
    }, []);

    const handleConditionChange = async(event, key) => {
        setParamRequirement(prevParam => prevParam.map(item => 
            item.key === key ? {...item, selected: event.target.value} : item
        ));

        setParamRequirement(prevRequirement => prevRequirement.map(item => 
            item.key === key ? {...item, value: "", statement: "", paramList: []} : item
        ))

        if (event.target.value !== "") {
            const send_data = {
                "selected": event.target.value, 
                "statement": paramRequirement.find(item => item.key === key).choiceState[event.target.value]
            }
    
            try {
                const response = await fetch(
                    '/api/communicate/height-condition', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(send_data)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                setParamRequirement(prevParam => prevParam.map(item => 
                    item.key === key ? {...item, statement: data.statement} : item
                ));
                setParamRequirement(prevParam => prevParam.map(item => 
                    item.key === key ? {...item, paramList: data.paramList} : item
                ));
            } catch(error) {
                console.log(error);
            };
        };
    };

    const handleKeyParamInputChange = (event, key) => {
        setParamRequirement(prevParam => prevParam.map(item => 
            item.key === key ? {...item, value: event.target.value} : item
        ));
    };

    const handleParamInputChange = (event, index, key) => {
        const newParamList = paramRequirement.find(param => param.key === key).paramList;
        newParamList[index].value = event.target.value;
        setParamRequirement(prevParam => prevParam.map(item => 
            item.key === key ? {...item, paramList: newParamList} : item
        ));
    };

    const handleSubmitClick = async(event) => {
        event.preventDefault();

        const hasEmptyFieldKeyValue = paramRequirement.some(item => item.statement !== "" && item.value == "");
        const hasEmptyFieldValue = paramRequirement.some(item => item.paramList.some(param => param.value == ""));

        if (hasEmptyFieldKeyValue || hasEmptyFieldValue) {
            alert("Please fill all required field!");
        } else {
            try {
                const response = await fetch(
                    '/api/communicate/height-check', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}, 
                        body: JSON.stringify(paramRequirement)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
            } catch(error) {
                console.log(error);
            };
            setComplete();
        };
    };

    return (
        <div>
            <h3>Building Height</h3>
            <ul>
                {moduleList.map((module, index) => (
                    <li key={index} style={commonStyles.listItem}>
                        <div style={commonStyles.itemColumn}>{module.name}</div>
                        <div style={commonStyles.itemColumn}>
                            <progress value={module.progress}></progress>
                            {startInput && <>
                                {paramRequirement.map((param, index) => (
                                <div key={index}>
                                    <p>{param.key}</p>
                                    {param.statement != "" && 
                                    <div>
                                        <span>input information: </span>
                                        <input type="text"
                                        onChange={(e) => handleKeyParamInputChange(e, param.key)}></input>
                                    </div>}
                                    {param.choices.length != 0 && 
                                    <div>
                                        <span>Select the one that fit the case: </span>
                                        <select 
                                        value={param.selected}
                                        onChange={(e) => handleConditionChange(e, param.key)}
                                        style={{width: "250px"}}>
                                            <option value=""> Select an option</option>
                                            {param.choices.map((choice, index1) => (
                                                <option key={index1} value={choice}>{choice}</option>
                                            ))}
                                        </select>
                                        {param.paramList.length != 0 && <div>
                                            <ul>
                                                {param.paramList.map((p, index2) => (
                                                    <li key={index2}>
                                                        <span>{p.name}: </span>
                                                        <input type="text"
                                                        onChange={(e) => handleParamInputChange(e, index2, param.key)}></input>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>}
                                    </div>}
                                </div> 
                            ))}
                            <br></br>
                            <button onClick={handleSubmitClick}>submit</button>
                            </>}
                        </div>
                    </li>
                ))}
            </ul>
            
        </div>
    );
};

export default Height;