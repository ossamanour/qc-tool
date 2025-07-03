import React, { useState } from "react";
import Modal from "../../../../components/Modal/Modal";

const AdvancedSetting = () => {
    const [modalOpen, setModalOpen] = useState(false);
    const [tolerance, setTolerance] = useState([
        {title: "Hard Duty Pavement", value: 0},
    ]);

    const clickAdvancedLoad = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                '/api/advance/load', {
                        method: "POST", 
                        credentials: "include", 
                        headers: {"Content-Type": "application/json"}
                    });
                if (!response.ok) {
                    throw new Error(response.statusText);
                };
                const data = await response.json();
                console.log(data);
                if (data.status) {
                    setTolerance(data.advancedConfig.tolerance);
                    setModalOpen(true);
                } else {
                    setModalOpen(true);
                };
        } catch (error) {
            console.log(error);
        };
    };

    const updateTolerance = (title, newValue) => {
        const updatedValue = tolerance.map(item => 
            item.title == title ? {...item, value: newValue} : item
        );
        setTolerance(updatedValue);
    };

    const submitOnClick = async(event) => {
        event.preventDefault();

        const sendData = {tolerance: tolerance};
        try {
            const response = await fetch(
                '/api/advance/setup', {
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
                    setModalOpen(false);
                    alert("Advance setting done!");
                } else {
                    alert(data.errorMessage);
                };
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <>
        <button onClick={clickAdvancedLoad}>Advance Setting</button>
        {modalOpen && <Modal 
        title="Advance Setting"
        onClose={() => setModalOpen(false)} 
        onSubmit={submitOnClick}>
            <div>
                <span style={{fontWeight: "bold"}}>Tolerance:</span>
                {tolerance.map((item, index) => (
                    <li key={index}>
                        {item.title}:
                        <br></br>
                        {item.value}%
                        <br></br>
                        -10%
                        <input 
                        type="range" 
                        min={-10} 
                        max={10} 
                        step={1}
                        value={item.value} 
                        onChange={(e) => updateTolerance(item.title, parseInt(e.target.value))}></input>
                        10%
                    </li>
                ))}
            </div>
        </Modal>}
        </>
    );
};

export default AdvancedSetting;