import React from "react";
import "./TaskSelectorContainer.css";

const TaskSelectorContainer = ({ taskOptions, handleCheckBoxChange, direction }) => {
    return (
        <div 
        className="select-container"
        style={{flexDirection: direction}}>
            <div className="title">Select Tasks</div>
            <div 
            className="option-container"
            style={{flexDirection: direction}}>
                {taskOptions.map((task, index) => (
                    <label 
                    className={task.disabled ? "option-disabled" : "option"} 
                    key={index}>
                        <input 
                        type="checkbox" 
                        checked={task.checked} 
                        value={task.value}
                        onChange={(event) => handleCheckBoxChange(event)}
                        disabled={task.disabled}
                        ></input>
                        {task.label}
                    </label>
                ))}
            </div>
        </div>
    );
};

export default TaskSelectorContainer;