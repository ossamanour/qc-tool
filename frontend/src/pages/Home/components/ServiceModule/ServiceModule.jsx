import React from "react";
import { useNavigate } from "react-router-dom";
import QualControlImage from "../../../../assets/Home-QualControl.jpg";
import CostEstimateImage from "../../../../assets/Home-CostEstimate.jpg";
import ChatBotImage from "../../../../assets/Home-ChatBot.jpg";
import InteractImage from "../../../../assets/Home-Interact.jpg";
import useStore from "../../../../components/store/store";
import "./ServiceModule.css";

const ServiceModule = () => {
    const {isAuthenticated, imageInteractTool} = useStore();
    const navigator = useNavigate();

    const QualControlOnClick = () => {
        if (!isAuthenticated) {
            alert("Login before you can use Quality Control tool.")
        } else {
            navigator(`/qualitycontrol/dashboard`);
        };
    };

    const ChatBotOnClick = () => {
        // if (!isAuthenticated) {
        //     alert("Login before you can use Chatbot tool.")
        // } else {
        //     navigator(``);
        // };
        window.open('https://mango-forest-0b57b761e.6.azurestaticapps.net/login', '_blank', 'noopener,noreferrer')
        // window.location.href = 'https://mango-forest-0b57b761e.6.azurestaticapps.net/login';
    };
    
    const CostEstimateOnClick = () => {
        if (!isAuthenticated) {
            alert("Login before you can use Cost Estimate tool.")
        } else {
            navigator(`/costestimate/dashboard`);
        };
    };

    const ImageInteractOnClick = () => {
        if (!isAuthenticated) {
            alert("Login before you can use Image Interact tool.");
        } else {
            navigator(`/imageinteract`);
        };
    }


    return (
        <section className="title">
            <h2>Services</h2>
            <div className="task-row">
                {/* <div className="task-item" onClick={ChatBotOnClick}> 
                    <img src={ChatBotImage} className="task-image"></img>
                    <p className="task-name">AEC ChatBot</p>
                </div> */}
                <div className="task-item" onClick={QualControlOnClick}>
                    <img src={QualControlImage} className="task-image"></img>
                    <p className="task-name">Quality Control</p>
                </div>
                <div className="task-item" onClick={CostEstimateOnClick}>
                    <img src={CostEstimateImage} className="task-image"></img>
                    <p className="task-name">Cost Estimate</p>
                </div>
            </div>
            {imageInteractTool && 
            <div className="task-row">
                <div className="task-item" onClick={ImageInteractOnClick}>
                    <img src={InteractImage} className="task-image"></img>
                    <p className="task-name">Image Interact Tool</p>
                </div>
            </div>
            }
        </section>
    );
};

export default ServiceModule;