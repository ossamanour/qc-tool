import React, { useEffect, useState } from "react";
import useStore from "../store/store";4
import "./ChatBotInterface.css";
import { useLayoutEffect } from "react";

const ChatBotInfoPanel = () => {
    const {loadSessionInfo, cityList, selectedCity, setSelectedCity, selectedZone, setSelectedZone, useTool, setUseTool, autoChatBotDataFetch} = useStore();
    const [getZoneFromLocation, setGetZoneFromLocation] = useState(true);
    const [infoType, setInfoType] = useState("ADDRESS");
    const [address, setAddress] = useState("");
    const [apn, setApn] = useState("");
    // const [selectedZone, setSelectedZone] = useState("");
    const [startFetch, setStartFetch] = useState(true);
    const [zoneList, setZoneList] = useState([]);
    // const [useTool, setUseTool] = useState(false);

    useLayoutEffect(() => {
        autoChatBotDataFetch();
    }, []);

    useEffect(() => {
        const fetchZoneList = async() => {
            if (!getZoneFromLocation) {
                try {
                    const response = await fetch(
                        `/api/chatbot/fetch-zone-list`, {
                            method: "POST", 
                            credentials: "include", 
                            headers: {"Content-Type": "application/json"}, 
                            body: JSON.stringify(selectedCity),
                        }); 
                    if (!response.ok) {
                        throw new Error(response.statusText);
                    }
                    const data = await response.json();
                    console.log(data);
                    if (data.status) {
                        setZoneList(data.zoneList)
                    } else {
                        alert(data.errorMessage);
                    };
                } catch (error) {
                    console.log(error);
                };
            } else {
                setSelectedZone("");
            };
        };

        fetchZoneList();
    }, [selectedCity, getZoneFromLocation]);

    const fetchZone = async(event) => {
        event.preventDefault();

        const sendData = {
            "city": selectedCity,
            "infoType": infoType, 
            "address": address, 
            "apn": apn,
        };

        try {
            const response = await fetch(
                `/api/chatbot/zone-fetch`, {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(sendData),
                }); 
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setSelectedZone(data.zone);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <div className="info-container">
        {loadSessionInfo ? <>
            <section className="info-sub-form">
                Information for current session: 
                <br></br>
                City: {`\u00A0`} {selectedCity}
                <br></br>
                Zone: {"\u00A0"} {selectedZone}
            </section>
        </> : <>
            <section className="info-sub-form">
                City
                <br></br>
                <select 
                className="info-select" 
                value={selectedCity} 
                onChange={(event) => setSelectedCity(event.target.value)}>
                    {cityList.map((city, index) => (
                        <option key={index} value={city}>
                            {city}
                        </option>
                    ))}
                </select>
            </section>
            {/* <hr className="horizontal-line"></hr> */}
            {getZoneFromLocation ? 
            <section className="info-sub-form">
                Location Information
                <select 
                className="info-select" 
                value={infoType} 
                onChange={(event) => setInfoType(event.target.value)}>
                    <option value="ADDRESS">ADDRESS</option>
                    <option value="APN">APN</option>
                </select>
                {infoType === "ADDRESS" ? <div>
                    Input Address 
                    <textarea 
                    className= "info-input" 
                    type="text" 
                    placeholder="Input Address" 
                    value={address} 
                    onChange={(event) => setAddress(event.target.value)}></textarea>
                </div> : <div>
                    Input APN 
                    <textarea 
                    className= "info-input" 
                    type="text" 
                    placeholder="Input APN" 
                    value={apn} 
                    onChange={(event) => setApn(event.target.value)}></textarea>
                </div>}
                <button
                onClick={fetchZone}>
                    Detect Zone
                </button>
                {selectedZone === "" ? 
                <div></div> : <div>
                    {selectedZone}
                </div>}
            </section> : <section className="info-sub-form">
                Zone
                <select 
                className="info-select" 
                value={selectedZone} 
                onChange={(event) => setSelectedZone(event.target.value)}>
                    <option value="">Select Zone</option>
                    {zoneList.map((zone, index) => (
                        <option key={index} value={zone}>{zone}</option>
                    ))}
                </select>
            </section>
            }
            <button onClick={() => setGetZoneFromLocation(!getZoneFromLocation)}>
                {getZoneFromLocation ? "Select Zone" : "Detect Zone from Location"}
            </button>
        </>}
            
            
            <br></br>
            <hr className="horizontal-line"></hr>

            <fieldset className="tool-field">
                <legend>ChatBot Tool</legend>
                <label className="tool-checkbox">
                    <input
                    type="checkbox" 
                    checked={useTool} 
                    onChange={() => setUseTool(!useTool)}></input>
                    AEC Chat +
                </label>
            </fieldset>
        </div>
    );
};

export default ChatBotInfoPanel;