import React, { useEffect, useRef, useState } from "react";
import SplitPane from "../../../../components/reactSplitPane/SplitPane";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleDoubleDown, faAngleDoubleUp, faChevronCircleLeft, faChevronCircleRight, faSearchMinus, faSearchPlus } from "@fortawesome/free-solid-svg-icons";
import ImageDisplay from "../../../../components/ImageDisplay/ImageDisplay";
import LogModule from "../../../../components/LogModule/LogModule";
import useStore from "../../../../components/store/store";
import "./MainWindow.css";

const MainWindow = () => {
    const [parentHeight, setParentHeight] = useState(0);
    const [logTabOpen, setLogTabOpen] = useState(true);
    const parentRef = useRef(null);
    const {currentSession, currentPage, setCurrentPage, setCurrentDisplay} = useStore();

    useEffect(() => {
        const handleResize = () => {
            if (parentRef.current) {
                setParentHeight(parentRef.current.offsetHeight);
            };
        }
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    const handlePreviousPage = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(
                '/api/image/previous_page', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}});
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setCurrentPage(data.currentPage);
                setCurrentDisplay(data.currentDisplay);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    const handleNextPage = async(event) => {
        event.preventDefault();
        
        try {
            const response = await fetch(
                '/api/image/next_page', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}});
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setCurrentPage(data.currentPage);
                setCurrentDisplay(data.currentDisplay);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <div ref={parentRef}>
            <SplitPane 
            split="horizontal" 
            size={logTabOpen ? "80%" : "100%"} 
            defaultSize={"80%"} 
            minSize={Math.trunc(parentHeight*0.6)} 
            maxSize={Math.trunc(parentHeight*1)}
            pane1ClassName="display-pane" 
            pane2ClassName="log-pane">
                <>
                <ImageDisplay switchPageDiv={
                    <>
                    <button onClick={handlePreviousPage}>
                        <FontAwesomeIcon icon={faChevronCircleLeft} />
                    </button>
                    <span className="page-box">{` ${currentPage}/${currentSession["total_page"]} `}</span>
                    <button onClick={handleNextPage}>
                        <FontAwesomeIcon icon={faChevronCircleRight} />
                    </button>
                    </>
                }></ImageDisplay>
                <button 
                className="logtab-button" 
                onClick={() => setLogTabOpen(!logTabOpen)}>
                    Logs {"\u00A0"} 
                    <FontAwesomeIcon icon={logTabOpen ? faAngleDoubleDown : faAngleDoubleUp} />
                </button>
                </>
                <>
                <LogModule></LogModule>
                </>
            </SplitPane>
        </div>
    );
};

export default MainWindow;