import React, { useEffect, useLayoutEffect } from "react";
import SideBarLayout from "../../components/SideBarLayout/SideBarLayout";
import useStore from "../../components/store/store";
import SideBar from "./components/SideBar/SideBar";
import MainWindow from "./components/MainWindow/MainWindow";

const QualityControlMain = () => {
    const {autoPageDataFetch, appInfo} = useStore();

    useLayoutEffect(() => {
        const autoPageFetch = async() => {
            await autoPageDataFetch("app");
            await appInfo("qualitycontrol");
        };

        autoPageFetch();
    }, []);

    return (
        <SideBarLayout 
        taskName="Quality Control" 
        sideBarChildren={<SideBar></SideBar>} 
        mainWindowChildren={<MainWindow></MainWindow>}></SideBarLayout>
    );
};

export default QualityControlMain;