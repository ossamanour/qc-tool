import React from "react";
import useStore from "../store/store";

const LogModule = () => {
    const {taskLog} = useStore();

    return (
        <ul>
        {taskLog.map((log, index) => (
            <li key={index}>{log}</li>
        ))}
        </ul>
    );
};

export default LogModule;
