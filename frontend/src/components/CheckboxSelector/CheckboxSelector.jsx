import React from "react";
import "./CheckboxSelector.css";

const CheckboxSelector = ({ 
    title,
    optionList, 
    setOptionList, 
    selectedOptions, 
    setSelectedOptions, 
    handleCheckBoxChange, 
    direction, 
    singleChoice}) => {

    const localHandleCheckBoxChange = (event) => {
        // event.preventDefault();

        setOptionList(prevList => prevList.map((option) => option.value === event.target.value ? {...option, checked: event.target.checked} : option));
        if (singleChoice) {
            setOptionList(prevList => prevList.map((option) => option.value !== event.target.value ? {...option, checked: false} : option));
        };
        if (event.target.checked) {
            setSelectedOptions([...selectedOptions, optionList.find(option => option.value === event.target.value)]);
        } else {
            setSelectedOptions(selectedOptions.filter(option => option.value !== event.target.value))
        };
    };

    const checkboxOnChange = (event) => {
        if (handleCheckBoxChange) {
            handleCheckBoxChange(event);
        } else {
            localHandleCheckBoxChange(event);
        };
    };

    return (
        <div 
        className="select-container"
        style={{flexDirection: direction}}>
            <div className="title" style={{fontWeight: "bold"}}>{title}</div>
            <div 
            className="option-container"
            style={{flexDirection: direction}}>
                {optionList.map((option, index) => (
                    <label 
                    className={option.disabled ? "option-disabled" : "option"} 
                    key={index}>
                        <input 
                        type="checkbox" 
                        checked={option.checked} 
                        value={option.value}
                        onChange={(event) => checkboxOnChange(event)}
                        disabled={option.disabled}
                        ></input>
                        {option.label}
                    </label>
                ))}
            </div>
        </div>
    );
};

export default CheckboxSelector;