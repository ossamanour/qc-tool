import React, { useEffect, useState } from "react";
import useStore from "../../../../components/store/store";
import HardDutyPavement from "./HardDutyPavement";
import FireHydrant from "./FireHydrant";
import LightPole from "./LightPole";
import AdaRamp from "./AdaRamp";
import AdaSign from "./AdaSign";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faClock, faSpinner } from "@fortawesome/free-solid-svg-icons";

const PerformTasks = () => {
    const {submittedTasks} = useStore();

    const [taskInfoList, setTaskInfoList] = useState([
        {id: 0, name: "HD PAVEMENT", information: []}, 
        {id: 1, name: "FIRE HYDRANT", information: []}, 
        {id: 2, name: "LIGHT POLE", information: []}, 
        {id: 3, name: "ADA RAMP", information: []}, 
        {id: 4, name: "ADA SIGN", information: []}, 
    ]);

    const setTaskResults = (id, newData) => {
        newData.map((data, index) => {
            setTaskInfoList(prevList => prevList.map(
                task => task.id == id ? {...task, information: [...task.information, data]} : task
            ));
        })
        // setTaskInfoList(prevList => prevList.map(
        //     task => task.id == id ? {...task, information: [...task.information, newData]} : task
        // ));
    };

    const [taskList, setTaskList] = useState([
        {id: 0, name: "HD PAVEMENT", status: 0,
            component: <HardDutyPavement 
            setComplete={() => setStatus(0, 1)} 
            setInformation={setTaskResults} 
            taskId={0} />
        },
        {id: 1, name: "FIRE HYDRANT", status: 0, 
            component: <FireHydrant 
            setComplete={() => setStatus(1, 1)} 
            setInformation={setTaskResults} 
            taskId={1} />
        },
        {id: 2, name: "LIGHT POLE", status: 0, 
            component: <LightPole 
            setComplete={() => setStatus(2, 1)} 
            setInformation={setTaskResults} 
            taskId={2} />
        },
        {id: 3, name: "ADA RAMP", status: 0, 
            component: <AdaRamp 
            setComplete={() => setStatus(3, 1)} 
            setInformation={setTaskResults} 
            taskId={3} />
        },
        {id: 4, name: "ADA SIGN", status: 0, 
            component: <AdaSign 
            setComplete={() => setStatus(4, 1)} 
            setInformation={setTaskResults} 
            taskId={4} />
        }, 
    ]);
      
    const setStatus = (id, newStatus) => {
        setTaskList(prevList => prevList.map(task => task.id == id ? {...task, status: newStatus} : task))
    };

    const toDisplay = taskList.filter(
        task => task.status === 0 && submittedTasks.includes(task.name));

    const infoDisplay = taskInfoList.filter(info => submittedTasks.includes(info.name));

    return (
        <>
        <h2>Cost Estimate</h2>
        {infoDisplay.map((info, index) => (
            <div key={index}>
                <h3>{info.name} {"\u00A0"}
                    {toDisplay.length > 0 && info.name === toDisplay[0].name ? 
                        <FontAwesomeIcon icon={faSpinner} className="fa-spin" style={{height: "15px"}} /> : <>
                    {taskList.filter(task => task.name === info.name)[0].status === 0 ? 
                        <FontAwesomeIcon icon={faClock} style={{height: "15px"}}/> : 
                        <FontAwesomeIcon icon={faCheck} style={{height: "15px"}}/>
                    }
                    </>
                    }
                </h3>
                {info.information.map((results, index1) => (
                    <li key={index1}>{results}</li>
                ))}
            </div>
        ))}
        {/* {taskInfoList.map((info, index) => (
            <div key={index}>
            {info.information.map((results, index1) => (
                <li key={index1}>{results.message}</li>
            ))}
            </div>
        ))} */}
        {/* <span>{toDisplay.length}</span> */}
        {toDisplay.length > 0 ? toDisplay[0].component : <></>}
        </>
    );
};

export default PerformTasks;