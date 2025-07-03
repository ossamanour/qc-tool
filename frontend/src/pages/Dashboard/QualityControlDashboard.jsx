import React, { useEffect } from "react";
import SideBarLayout from "../../components/SideBarLayout/SideBarLayout";
import useStore from "../../components/store/store";
import SideBar from "./components/SideBar/SideBar";
import MainWindow from "./components/MainWindow/MainWindow";

const QualityControlDashboard = () => {
    const {autoPageDataFetch, initializeApp} = useStore();

    useEffect(() => {
        const autoPageFetch = async() => {
            await autoPageDataFetch("dashboard");
            await initializeApp("qualitycontrol");
        };
        
        autoPageFetch();
    }, []);
    return (
        <SideBarLayout
        taskName="Quality Control" 
        sideBarChildren={<SideBar navigateTo="/qualitycontrol/main"></SideBar>} 
        mainWindowChildren={<MainWindow></MainWindow>}></SideBarLayout>
    );
};

export default QualityControlDashboard;