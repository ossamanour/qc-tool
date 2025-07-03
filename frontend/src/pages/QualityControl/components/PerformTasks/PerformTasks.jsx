import React, { useState } from "react";
import useStore from "../../../../components/store/store";
import Zoning from "./Zoning";
import Dimension from "./Dimension";
import Keynote from "./Keynote";
import KeynoteMatch from "./KeynoteMatch";
import Parking from "./Parking";
import ParkingQualityControl from "./ParkingQualityControl";
import Height from "./Height";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faClock, faSpinner } from "@fortawesome/free-solid-svg-icons";

const PerformTasks = () => {
    const {submittedTasks} = useStore();

    const [taskInfoList, setTaskInfoList]  = useState([
        {id: 0, name: "ZONING", information: []}, 
        {id: 1, name: "DIMENSION", information: []}, 
        {id: 2, name: "KEYNOTE MATCH", information: []}, 
        {id: 3, name: "MATCHING", information: []}, 
        {id: 4, name: "PARKING", information: []}, 
        {id: 5, name: "PARKING QUALITY CONTROL", information: []},
        {id: 6, name: "BUILDING HEIGHT", information: []},
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

    // const setTaskResults = (id, newData) => {
    //     setTaskInfoList(prevList => prevList.map(
    //         task => task.id == id ? {...task, information: task.information.push(newData)} : task
    //     ));
    // };

    const [taskList, setTaskList] = useState([
        {id: 0, name: "ZONING", status: 0, 
            component: <Zoning 
            setComplete={() => setStatus(0, 1)} 
            setInformation={setTaskResults} 
            taskId={0} />,
            information: []
        }, 
        {id: 1, name: "DIMENSION", status: 0, 
            component: <Dimension 
            setComplete={() => setStatus(1, 1)} 
            setInformation={setTaskResults} 
            taskId={1} />,
            information: []
        },
        {id: 2, name: "KEYNOTE MATCH", status: 0, 
            component: <Keynote 
            setComplete={() => setStatus(2, 1)} 
            setInformation={(setTaskResults)} 
            taskId={2} />,
            information: []
        },
        {id: 3, name: "MATCHING", status: 0, 
            component: <KeynoteMatch 
            setComplete={() => setStatus(3, 1)} 
            setInformation={setTaskResults} 
            taskId={3} />,
            information: []
        },
        {id: 4, name: "PARKING", status: 0, 
            component: <Parking 
            setComplete={() => setStatus(4, 1)} 
            setInformation={setTaskResults} 
            taskId={4} />,
            information: []
        }, 
        {id: 5, name: "PARKING QUALITY CONTROL", status: 0, 
            component: <ParkingQualityControl 
            setComplete={() => setStatus(5, 1)} 
            setInformation={setTaskResults} 
            taskId={5} />,
            information: []
        },
        {id: 6, name: "BUILDING HEIGHT", status: 0, 
            component: <Height 
            setComplete={() => setStatus(6, 1)} 
            setInformation={setTaskResults} 
            taskId={6} />,
            information: []
        }
    ]);

    const setStatus = (id, newStatus) => {
        setTaskList(prevList => prevList.map(task => task.id == id ? {...task, status: newStatus} : task))
    };

    const toDisplay = taskList.filter(
        task => task.status === 0 && submittedTasks.includes(task.name));

    // const toDisplayInfo = taskInfoList.filter(
    //     task => submittedTasks.includes(task.name)
    // );
    // const taskInfoDisplay = taskList.filter(task => submittedTasks.includes(task.name));

    const infoDisplay = taskInfoList.filter(info => submittedTasks.includes(info.name));

    return (
        <>
        <h2>Quality Control</h2>
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
        {/* {taskInfoDisplay.map((info, index) => (
            <div key={index}>
                <h3>{info.name}</h3>
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