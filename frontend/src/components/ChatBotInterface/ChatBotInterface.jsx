import React from "react";
import useStore from "../store/store";
import ChatBotInfoPanel from "./ChatBotInfoPanel";
import ChatBotChatPanel from "./ChatBotChatPanel";
import "./ChatBotInterface.css";

const ChatBotInterface = () => {
   
    return (
        <div className="main-container">
            <div className="left-container">
                <ChatBotInfoPanel></ChatBotInfoPanel>
            </div>
            <div className="right-container">
                <ChatBotChatPanel></ChatBotChatPanel>
            </div>
        </div>
    );
};

export default ChatBotInterface;