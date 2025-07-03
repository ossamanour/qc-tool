import React, { useState } from "react";
import botImage from "../../assets/BOT_icon.png"
import "./ChatBotAvatar.css";

const ChatBotAvatar = ({ onClick }) => {
    const [isHovered, SetIsHovered] = useState(false);

    return (
        <>
        {isHovered && <div className="hello-message">
            Hi, it's Chatbot!
            </div>}

        <div 
        onMouseEnter={() => SetIsHovered(true)}
        onMouseLeave={() => SetIsHovered(false)} 
        onClick={() => onClick()}
        className="avator-button" 
        style={{
            backgroundImage: `url(${botImage})`, 
            backgroundSize: "60px"
        }}>
        </div>
        </>
    );
};

export default ChatBotAvatar;