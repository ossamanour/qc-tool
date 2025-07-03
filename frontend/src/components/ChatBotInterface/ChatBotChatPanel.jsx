import React, { useState } from "react";
import botImage from "../../assets/BOT_icon.png";
import userImage from "../../assets/user.png";
import useStore from "../store/store";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSpinner, faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import "./ChatBotInterface.css";

const ChatBotChatPanel = () => {
    const {selectedCity, selectedZone, useTool} = useStore();
    const [message, setMessage] = useState("");
    const [conversation, setConversation] = useState([]);

    const handleSubmit = async() => {
        event.preventDefault(); 

        if (!message) return;

        setConversation(prevConv => [...prevConv, {role: "user", content: message}]);
        setConversation(prevConv => [...prevConv, {role: "chatbot", content: "dummyFlag"}]);

        const sendData = {
            "city": selectedCity, 
            "zone": selectedZone, 
            "message": message, 
            "useTool": useTool, 
        };

        setMessage("");
        scrollTo(0, 1e10);

        try {
            const response = await fetch(
                '/api/chatbot/get-response', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(sendData)});
            if (!response.ok) {
                throw new Error(response.statusText)
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setConversation(prevConv => prevConv.slice(0, -1));
                setConversation(prevConv => [...prevConv, {role: "chatbot", content: data["result"]}])
            } else {
                // alert(data.errorMessage);
                setConversation(prevConv => prevConv.slice(0, -1));
                setConversation(prevConv => [...prevConv, {role: "error", content: data["errorMessage"]}])
            };
        } catch (error) {
            console.log(error);
        };
    };

    const handleKeyDown = (event, message) => {
        if (event.key === "Enter" && event.ctrlKey) {
            event.preventDefault();
            handleSubmit(event, message);
        };
    };

    return (
        <div className="chat-container">
            <section className="conversation-container">
                {conversation.map((message, index) => (
                    <p key={index} 
                    className={`conversation-${message.role}`}>
                        <img 
                        className="profile-image" 
                        src={message.role == "user" ? userImage : botImage}></img>
                        <span className="content">
                            {message.content == "dummyFlag" ? 
                            <FontAwesomeIcon icon={faSpinner} className="fa-spin"/> : 
                            message.content}
                        </span>
                    </p>
                ))}
            </section>
            <form 
            action="" 
            onSubmit={(event) => handleSubmit(event, message)}
            className="submit-form">
                <textarea 
                className="input-box" 
                type="text" 
                name="message" 
                value={message} 
                placeholder="Type in question, Ctrl+Enter to submit..." 
                onChange={(event) => setMessage(event.target.value)} 
                onKeyDown={(event) => handleKeyDown(event, message)}></textarea>
                {"\u00A0"}
                <button className="submit-button">
                    <FontAwesomeIcon icon={faPaperPlane} />
                </button>
            </form>
        </div>
    );
};

export default ChatBotChatPanel;