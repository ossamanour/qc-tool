import React, { useContext, useEffect, useState } from "react";
import ToggleSwitch from "../ToggleSwitch/ToggleSwitch";
import useStore from "../store/store";

const ChatBotToggle = () => {
    const {chatbotInUse, setChatbotInUse} = useStore();

    const onChange = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                '/api/chatbot/switch', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(chatbotInUse)});
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setChatbotInUse(data.chatbotInUse);
            } else {
                alert(data.errorMessage);
            };
        } catch(error) {
            console.log(error);
        };
    };

    return (
        <>
        <ToggleSwitch 
        label="ChatBot" 
        checked={chatbotInUse}
        onChange={onChange}
        ></ToggleSwitch>
        </>
    );
};

export default ChatBotToggle;