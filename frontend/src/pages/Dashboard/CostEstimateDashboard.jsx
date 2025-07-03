import React, { useEffect } from "react";
import SideBarLayout from "../../components/SideBarLayout/SideBarLayout";
import useStore from "../../components/store/store";
import SideBar from "./components/SideBar/SideBar";
import MainWindow from "./components/MainWindow/MainWindow";

const CostEstimateDashboard = () => {
    const {autoPageDataFetch, initializeApp} = useStore();

    useEffect(() => {
        const autoPageFetch = async() => {
            await autoPageDataFetch("dashboard");
            await initializeApp("costestimate");
        };
        
        autoPageFetch();
    }, []);

    return (
        <SideBarLayout
        taskName="Cost Estimate" 
        sideBarChildren={<SideBar navigateTo="/costestimate/main"></SideBar>} 
        mainWindowChildren={<MainWindow></MainWindow>}></SideBarLayout>
    );
};

export default CostEstimateDashboard;