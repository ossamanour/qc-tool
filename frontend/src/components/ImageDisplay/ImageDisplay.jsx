import React, { useEffect } from "react";
import { MapInteractionCSS } from "react-map-interaction";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronCircleLeft, faChevronCircleRight, faSearchMinus, faSearchPlus } from "@fortawesome/free-solid-svg-icons";
import logoImg from "../../assets/AIAEC-logo.png";
import useStore from "../store/store";
import Modal from "../Modal/Modal";
import "./ImageDisplay.css";

const ImageDisplay = ({switchPageDiv}) => {
    const {currentDisplay} = useStore();
    
    // const handlePreviousPage = () => {};

    // const handleNextPage = () => {};

    return (
        <>
        <div className="image-display-container">
            <div className="image-display-tool-div">
                {switchPageDiv}
                {/* <button className="icon_button" onClick={handlePreviousPage}>
                    <FontAwesomeIcon icon={faChevronCircleLeft} />
                </button>
                <button className="icon_button" onClick={handleNextPage}>
                    <FontAwesomeIcon icon={faChevronCircleRight} />
                </button> */}
            </div>
            <div className="image-display-window">
                <MapInteractionCSS
                showControls
                defaultValue={{
                scale: 1,
                translation: { x: 0, y: 0 }
                }}
                minScale={0.5}
                maxScale={3}
                translationBounds={{
                xMax: 400,
                yMax: 200
                }}
                plusBtnContents={<FontAwesomeIcon icon={faSearchPlus} />}
                minusBtnContents={<FontAwesomeIcon icon={faSearchMinus} />}
                // btnClass="icon_button"
                >
                {/* <img src={logoImg}></img> */}
                <img src={`/api/image/${currentDisplay}`} width="100%"></img>
                {/* {state.currentDisplay === "AIAEC-logo.png" ? 
                <img
                    src={logoImage} 
                    className="image-show"/> :
                <img 
                    src={'/api/images/'} 
                    alt="Switchable Image" 
                    width="100%" />} */}
                </MapInteractionCSS>
            </div>
        </div>
        
        </>
    );
};

export default ImageDisplay;