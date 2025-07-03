import React from "react";
import ParentWindow from "../../../../components/ParentWindow/ParentWindow";
import PerformTasks from "./PerformTasks";
import useStore from "../../../../components/store/store";

const PerformTasksParent = ({ buttonIcon }) => {
    const {submittedTasks, setSubmittedTasks} = useStore();

    const performTasksSubmit = async() => {
        const sendData = {"submittedTasks": submittedTasks};
        try {
            const response = await fetch(
                '/api/task/submit', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(sendData)});
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setSubmittedTasks(data.todoTasks);
            } else {
                alert(data.errorMessage);
            };
            return data;
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <ParentWindow
        funcBeforeOpen={performTasksSubmit} 
        icon={buttonIcon}>
            <PerformTasks></PerformTasks>
        </ParentWindow>
    );
};

export default PerformTasksParent;