import React, { useState, useEffect } from "react";
import TaskSelectorContainer from "../../../../components/TaskSelectorContainer/TaskSelectorContainer";
import useStore from "../../../../components/store/store";

const OnsiteTaskSelector = () => {
    const [taskOptions, setTaskOptions] = useState([
        {value: "ALL", label: "ALL", disabled: false, checked: false},
        {value: "FIRE HYDRANT", label: "FIRE HYDRANT", disabled: false, checked: false}, 
        {value: "LIGHT POLE", label: "LIGHT POLE", disabled: false, checked: false}, 
        {value: "ADA RAMP", label: "ADA RAMP", disabled: false, checked: false}, 
        {value: "ADA SIGN", label: "ADA SIGN", disabled: false, checked: false}, 
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
        } else {
            setSelectedOptions(selectedOptions.filter(task => task.value !== event.target.value));
            // any unselect should cause the ALL to be unselected
            setTaskOptions(prevOptions => prevOptions.map((task) => task.value === "ALL" ? {...task, checked: false} : task)); 
        };
    };

    return(
        <TaskSelectorContainer
        taskOptions={taskOptions} 
        handleCheckBoxChange={handleCheckBoxChange}
        direction="column"></TaskSelectorContainer>
    );
};

export default OnsiteTaskSelector;