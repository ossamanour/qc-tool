import React, { useEffect, useState } from "react";
import Select from "react-select";
import "./SessionConfigSetting.css";

const KeynoteSelector = ({ value, setValue }) => {
    const [keynoteTemplateList, setKeynoteTemplateList] = useState([]);
    const [currentKeynoteTemplate, setCurrentKeynoteTemplate] = useState();
    const [selectAvailable, setSelectAvailable] = useState(true);

    const setKeynoteTemplateOptions = (valueList) => {
        const temp = valueList.map((valueKey, index) => ({
            value: valueKey, 
            label: <img src={`/api/config/keynote_view/${valueKey}`} className="small-img"></img>}))
        setKeynoteTemplateList(temp);
    };

    useEffect(() => {
        const getKeynoteTemplateList = async() => {
            try {
                const response = await fetch(
                    '/api/config/keynote_list', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                if (data.status) {
                    setKeynoteTemplateOptions(data.list);
                } else {
                    setCurrentKeynoteTemplate(data.keynoteTemplate);
                    setSelectAvailable(false);
                };
            } catch (error) {
                console.log(error);
            };
        };

        getKeynoteTemplateList();
    }, []);

    return (
        <>
        {selectAvailable ? <div>
            <span>Select Keynote Template {'\u00A0'}</span>
            <Select 
            options={keynoteTemplateList} 
            hideSelectedOptions={false} 
            placeholder="Select Keynote Company" 
            onChange={(selected) => setValue(selected)} 
            value={value}></Select>
        </div> : <div>
            <span>Keynote Template: </span>
            <img src={`/api/config/keynote_view/${currentKeynoteTemplate}`} className="small-img"></img>
        </div>}
        </>
    );
};

export default KeynoteSelector;