import React, { useState, useRef, useEffect } from "react";
import ChatBotAvatar from "./ChatBotAvatar";
import ChatBotInterface from "../ChatBotInterface/ChatBotInterface";
import "./ChatBotEngine.css"

const ChatBotEngine = ({ children }) => {
    const wrapperRef = useRef(null);
    useOutsideAlerter(wrapperRef);
    const [chatWinVisible, setChatWinVisible] = useState(false);
    const [renderChatbot, setRenderChatbot] = useState(false);

    function useOutsideAlerter(ref) {
        useEffect(() => {
            function handleClickOutside(event) {
                if (ref.current && !ref.current.contains(event.target)) {
                    setChatWinVisible(false)
                    setRenderChatbot(false)
                }
            }
            document.addEventListener("mousedown", handleClickOutside);
            return () => {
                document.removeEventListener("mousedown", handleClickOutside);
            };
        }, [ref]);
    }

    const onClick = () => {
        setChatWinVisible(true);
        setRenderChatbot(true);
    };

    return (
        <>
        <div ref={wrapperRef}>
            {chatWinVisible ? <div className="chatbot-window">
                {renderChatbot && 
                <ChatBotInterface></ChatBotInterface>}
            </div> : <div></div>}

            <ChatBotAvatar 
            onClick={onClick}></ChatBotAvatar>
        </div>
        </>
    );
};

export default ChatBotEngine; 