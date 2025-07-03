import React, { useEffect, useRef, useState } from "react";
import Layout from "../Layout/Layout";
import SplitPane from "../reactSplitPane/SplitPane";
import "./SideBarLayout.css";


const SideBarLayout = ({ taskName, sideBarChildren, mainWindowChildren }) => {
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);
    const [sideBarOpen, setSideBarOpen] = useState(true);

    useEffect(() => {
        const handleResize = () => {
            setWindowWidth(window.innerWidth);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);
    
    return (
        <Layout taskName={taskName}>
            <SplitPane
            style={{top: "2em", overflow: "auto", bottom: "2em"}} 
            split="vertical"
            size={sideBarOpen ? "20%" : 0}
            defaultSize={"20%"} 
            height={"inherit"}
            minSize={Math.trunc(windowWidth*0.2)} 
            maxSize={Math.trunc(windowWidth*0.3)}
            pane1ClassName="sidebar-pane" 
            pane2ClassName="mainwin-pane">
                <>{sideBarOpen && sideBarChildren}</>
                <>
                <button 
                className="sidebar-button"
                onClick={() => setSideBarOpen(!sideBarOpen)}>
                    {sideBarOpen ? '\u2B9C' : '\u2B9E'}
                </button>
                {mainWindowChildren}
                </>
            </SplitPane>
        </Layout>
    );
};

export default SideBarLayout; 