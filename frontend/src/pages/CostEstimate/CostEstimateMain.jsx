import React, { useLayoutEffect } from "react";
import SideBarLayout from "../../components/SideBarLayout/SideBarLayout";
import useStore from "../../components/store/store";
import SideBar from "./components/SideBar/SideBar";
import MainWindow from "./components/MainWindow/MainWindow";

const CostEstimateMain = () => {
    const {autoPageDataFetch, appInfo} = useStore();

    useLayoutEffect(() => {
        const autoPageFetch = async() => {
            await autoPageDataFetch("app");
            await appInfo("costestimate");
        };

        autoPageFetch();
    }, []);

    return (
        <SideBarLayout 
        taskName="Cost Estimate" 
        sideBarChildren={<SideBar></SideBar>} 
        mainWindowChildren={<MainWindow></MainWindow>}></SideBarLayout>
    );
};

export default CostEstimateMain;