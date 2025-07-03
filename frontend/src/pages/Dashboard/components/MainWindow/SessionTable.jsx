import React from "react";
import { useNavigate } from "react-router-dom";
import useStore from "../../../../components/store/store";

const SessionTable = () => {
    const {sessionList, setSessionList, currentApp} = useStore();
    const navigate = useNavigate();

    const onClickLoad = async(session) => {
        try {
            const response = await fetch(
                '/api/session/load', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(session)
                });
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                navigate(`/${currentApp}/main`)
                // setSessionList(data.sessionList);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    const onClickShare = async(session) => {};

    const onClickDelete = async(session) => {
        try {
            const response = await fetch(
                '/api/session/soft-delete', {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(session)
                });
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                setSessionList(data.sessionList);
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    };

    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>Session Name</th>
                        <th>Input File</th>
                        <th>Created Time</th>
                        <th>Modified Time</th>
                        <th></th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {sessionList.map((session, index) => (
                        <tr key={index}>
                            <td>{session.sessionName}</td>
                            <td>{session.filename}</td>
                            <td>{session.createdTime}</td>
                            <td>{session.modifiedTime}</td>
                            <td><button onClick={() => onClickLoad(session)}>Load</button></td>
                            {/* <td><button onClick={() => onClickShare(session)}>Share</button></td> */}
                            <td><button onClick={() => onClickDelete(session)}>Delete</button></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default SessionTable;