import React, { useEffect, useState } from "react";
import TaskSelectorContainer from "../../../../components/TaskSelectorContainer/TaskSelectorContainer";
import useStore from "../../../../components/store/store";

const TaskSelector = () => {
    const [taskOptions, setTaskOptions] = useState([
        {value: "ALL", label: "ALL", disabled: false, checked: false},
        {value: "ZONING", label: "ZONING", disabled: false, checked: false}, 
        {value: "DIMENSION", label: "DIMENSION", disabled: false, checked: false}, 
        {value: "KEYNOTE MATCH", label: "KEYNOTE MATCH", disabled: false, checked: false}, 
        {value: "PARKING", label: "PARKING", disabled: false, checked: false}, 
        {value: "BUILDING HEIGHT", label: "BUIDLING HEIGHT", disabled: false, checked: false}, 
        {value: "SETBACK", label: "SETBACK", disabled: true, checked: false}
    ]);

    const [selectedOptions, setSelectedOptions] = useState([]);
    const {setSubmittedTasks} = useStore();

    useEffect(() => {
        setSubmittedTasks(selectedOptions.map(task => task.value));
    }, [selectedOptions]);

    const handleCheckBoxChange = (event) => {
        setTaskOptions(prevOptions => prevOptions.map((task) => task.value === event.target.value ? {...task, checked: event.target.checked} : task)); 

        if (event.target.checked) {
            if (event.target.value !== "ALL") {
                setSelectedOptions([...selectedOptions, taskOptions.find(task => task.value == event.target.value)]);
            }
            // select ALL
            if (event.target.value === "ALL") {
                setTaskOptions(prevOptions => prevOptions.map((task) => task.disabled ? task : {...task, checked: true}));
                const allOptionsOtherThanALL = taskOptions.filter(task => task.value != "ALL" && task.disabled != true)
                const allOptions = allOptionsOtherThanALL.map(task => task);
                setSelectedOptions(allOptions);
            }; 
            // select PARKING
            if (event.target.value == "PARKING" && taskOptions.find(task => task.value === "ZONING").checked == false) {
                setTaskOptions(prevOptions => prevOptions.map((task) => task.value === "ZONING" ? {...task, checked: true} : task));
                setSelectedOptions([...selectedOptions, taskOptions.find(task => task.value == "PARKING"), taskOptions.find(task => task.value == "ZONING")]);
            };
            // select BUILDING HEIGHT
            if (event.target.value == "BUILDING HEIGHT" && taskOptions.find(task => task.value === "ZONING").checked == false) {
                setTaskOptions(prevOptions => prevOptions.map((task) => task.value === "ZONING" ? {...task, checked: true} : task));
                setSelectedOptions([...selectedOptions, taskOptions.find(task => task.value == "BUILDING HEIGHT"), taskOptions.find(task => task.value == "ZONING")]);
            };
            
        } else {
            setSelectedOptions(selectedOptions.filter(task => task.value !== event.target.value));
            // any unselect should cause the ALL to be unselected
            setTaskOptions(prevOptions => prevOptions.map((task) => task.value === "ALL" ? {...task, checked: false} : task)); 
            // unselect ZONING
            if (event.target.value === "ZONING") {
                setTaskOptions(prevOptions => prevOptions.map((task) => task.value === "PARKING" ? {...task, checked: false} : task));
                setTaskOptions(prevOptions => prevOptions.map((task) => task.value === "BUILDING HEIGHT" ? {...task, checked: false} : task));
                setSelectedOptions(selectedOptions.filter(task => task.value != event.target.value && task.value != "PARKING" && task.value != "BUILDING HEIGHT"));
            };
        };
    };

    return (
        <TaskSelectorContainer
        taskOptions={taskOptions} 
        handleCheckBoxChange={handleCheckBoxChange}
        direction="column"></TaskSelectorContainer>
    );
};

export default TaskSelector;