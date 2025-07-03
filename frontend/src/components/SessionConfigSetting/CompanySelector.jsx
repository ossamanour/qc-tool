import React, { useEffect, useState } from "react";
import Select from "react-select";
import Modal from "../Modal/Modal";

const CompanySelector = ({ value, setValue }) => {
    const [companyTemplateList, setCompanyTemplateList] = useState([]);
    const [viewTemplatePath, setViewTemplatePath] = useState();
    const [templateViewModalOpen, setTemplateViewModalOpen] = useState(false);
    const [currentCompany, setCurrentCompany] = useState();
    const [selectAvailable, setSelectAvailable] = useState(true);

    useEffect(() => {
        const getCompanyTemplateList = async() => {
            try {
                const response = await fetch(
                    '/api/config/company_list', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                if (data.status) {
                    setCompanyTemplateList(data.list);
                } else {
                    setCurrentCompany(data.company);
                    setSelectAvailable(false);
                };
            } catch (error) {
                console.log(error);
            };
        };

        getCompanyTemplateList();
    }, []);

    const viewTemplate = async(event) => {
        event.preventDefault();

        if (!value) {
            alert("Select a template to view.");
        } else {
            try {
                const response = await fetch(
                    '/api/config/template_path', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify(value)});
                if (!response.ok) {
                    throw new Error(response.statusText);
                };
                const data = await response.json();
                console.log(data);
                if (data.status) {
                    setViewTemplatePath(data.templatePath);
                    setTemplateViewModalOpen(true);
                } else {
                    alert(data.errorMessage);
                };
            } catch (error) {
                console.log(error);
            };
        };
    };

    const viewCurrentTemplate = async(event) => {
        event.preventDefault();

        const sendData = {value: currentCompany.toLowerCase()}
        try {
            const response = await fetch(
                '/api/config/template_path', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(sendData)});
            if (!response.ok) {
                throw new Error(response.statusText);
            };
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setViewTemplatePath(data.templatePath);
                setTemplateViewModalOpen(true);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <>
        {selectAvailable ? <div>
            <span>Select Company Template {'\u00A0'}</span>
            <button onClick={viewTemplate}>view</button>
            <Select 
            options={companyTemplateList} 
            hideSelectedOptions={false} 
            placeholder="Select Produce Company" 
            onChange={(selected) => setValue(selected)} 
            value={value}></Select>
        </div> : <div>
            <span>Company Template: {currentCompany}</span>
            <button onClick={viewCurrentTemplate}>view</button>
        </div>}
        
        {templateViewModalOpen && 
        <Modal 
        title="Template Preview" 
        onClose={() => setTemplateViewModalOpen(false)}>
                <img src={`/api/config/view_template/${viewTemplatePath}`} width="100%"></img>    
        </Modal>}
        </>
    );
};

export default CompanySelector;