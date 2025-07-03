import React, { useEffect, useState } from "react";
import Select from "react-select";
import Modal from "../Modal/Modal";
import ExcelView from "../ExcelView/ExcelView";

const PriceSheetSelector = ({ value, setValue }) => {
    const [priceSheetList, setPriceSheetList] = useState([]);
    const [priceSheetHeader, setPriceSheetHeader] = useState([]);
    const [priceSheetViewTable, setPriceSheetViewTable] = useState({
        onsite: [], 
        offsite: []
    });
    const [sheetViewModalOpen, setSheetViewModalOpen] = useState(false);
    const [currentPriceSheet, setCurrentPriceSheet] = useState();
    const [selectAvailable, setSelectAvailable] = useState(true);

    useEffect(() => {
        const getPriceSheetList = async() => {
            try {
                const response = await fetch(
                    '/api/config/pricesheet_list', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}});
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                const data = await response.json();
                console.log(data);
                if (data.status) {
                    setPriceSheetList(data.list);
                } else {
                    setCurrentPriceSheet(data.price);
                    setSelectAvailable(false);
                };
            } catch (error) {
                console.log(error);
            };
        };
        
        getPriceSheetList();
    }, []);

    const viewTable = async(event) => {
        event.preventDefault();

        if (!value) {
            alert("Select a price sheet to view.");
        } else {
            try {
                const response = await fetch(
                    '/api/config/pricesheet_view', {
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
                    setPriceSheetHeader(data.sheetHeader);
                    setPriceSheetViewTable(prev => ({...prev, onsite: data.onsiteSheet}));
                    setPriceSheetViewTable(prev => ({...prev, offsite: data.offsiteSheet})); 
                    setSheetViewModalOpen(true);
                } else {
                    alert(data.errorMessage);
                };
            } catch (error) {
                console.log(error);
            };
        };
    };

    const viewCurrentPriceSheet = async(event) => {
        event.preventDefault();

        const sendData = {value: currentPriceSheet};
        try {
            const response = await fetch(
                '/api/config/pricesheet_view', {
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
                setPriceSheetHeader(data.sheetHeader);
                setPriceSheetViewTable(prev => ({...prev, onsite: data.onsiteSheet}));
                setPriceSheetViewTable(prev => ({...prev, offsite: data.offsiteSheet})); 
                setSheetViewModalOpen(true);
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
            <span>Select Price Sheet {'\u00A0'}</span>
            <button onClick={viewTable}>view</button>
            <Select 
            options={priceSheetList} 
            hideSelectedOptions={false} 
            placeholder="Select Price Sheet" 
            onChange={(selected) => setValue(selected)} 
            value={value}></Select>
        </div> : <div>
            <span>Price Sheet Template: {currentPriceSheet}</span>
            <button onClick={viewCurrentPriceSheet}>view</button>
        </div>}

        {sheetViewModalOpen && <Modal 
        title="Price Sheet" 
        onClose={() => setSheetViewModalOpen(false)}>
            <ExcelView 
            header={priceSheetHeader} 
            tables={priceSheetViewTable}></ExcelView>
        </Modal>}
        </>
    );
};

export default PriceSheetSelector;