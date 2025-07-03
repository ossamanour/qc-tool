import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDownload, faFilePdf, faSpinner } from "@fortawesome/free-solid-svg-icons";
import Modal from "../Modal/Modal";
import CheckboxSelector from "../CheckboxSelector/CheckboxSelector";
import useStore from "../store/store";

const ReportGenerator = () => {
    const [modalOpen, setModalOpen] = useState(false);
    const [pdfUrl, setPdfUrl] = useState("");
    const [inProcess, setInProcess] = useState(false);
    const {currentApp} = useStore();
    const [taskList, setTaskList] = useState([]);
    const [selectedTasks, setSelectedTasks] = useState([]);
    const [downloadModalOpen, setDownloadModalOpen] = useState(false);
    const [downloadOptions, setDownloadOptions] = useState([
        {label: "report only", value: "report", checked: false}, 
        {label: "report & appendices in separate PDF files", value: "separate", checked: false}, 
        {label: "report & appendices in one PDF file", value: "combine", checked: false}
    ]);
    const [cedownloadOptions, setCEDownloadOptions] = useState([
        {label: "report only", value: "report", checked: false}, 
        {label: "report & site plans in separate PDF files", value: "separate", checked: false}, 
        {label: "report & site plans in one PDF file", value: "combine", checked: false}
    ]);
    const [selecetedDownloadOptions, setSelctedDownloadOptions] = useState([]);

    const reportTaskSelect = async(event) => {
        event.preventDefault();

        try {
            const response = await fetch(`/api/report/${currentApp}_tasklist`); 
            if (!response.ok) {
                throw new Error(response.statusText); 
            }
            const data = await response.json();
            console.log(data);
            setTaskList(data.taskList);
            setModalOpen(true);
        } catch (error) {
            console.log(error);
        };
    };
    
    const generateReport = async(event) => {
        setInProcess(true);
        event.preventDefault();

        const sendData = selectedTasks.map(task => task.value);
        try {
            const response = await fetch(
                `/api/report/${currentApp}_generate`, {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(sendData)
                }); 
            if (!response.ok) {
                throw new Error(response.statusText); 
            }
            const blob = await response.blob();
            const pdfBlobUrl = URL.createObjectURL(blob);
            setPdfUrl(pdfBlobUrl);
            setModalOpen(false);
            setSelectedTasks([]);
            setInProcess(false);
            alert("Report Generated.")
        } catch (error) {
            console.log(error);
            setInProcess(false);
        };
    };

    const viewReport = () => {
        event.preventDefault()

        const url = `/api/report/view/${currentApp}.pdf`
        window.open(url, "_blank");
    };

    const downloadReport = async(event) => {
        setInProcess(true);
        event.preventDefault();

        // const sendData = selecetedDownloadOptions.map(option => option.value);
        const sendData = selecetedDownloadOptions[0].value;
        try {
            const response = await fetch(
                `/api/report/${currentApp}_download/${sendData}`, {
                    method: "GET", 
                    responseType: "blob"
                }); 
            if (!response.ok) {
                throw new Error(response.statusText); 
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            if (sendData === "report") {
                console.log(sendData)
                link.setAttribute('download', 'report.pdf'); 
            } 
            if (sendData === "separate") {
                console.log(sendData)
                link.setAttribute('download', 'report.zip'); 
            }
            if (sendData === "combine") {
                console.log(sendData);
                link.setAttribute('download', 'combine_report.pdf'); 
            }
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            alert("Downloaded Done!");
            setInProcess(false);
            setDownloadModalOpen(false);
            setSelctedDownloadOptions([]);
        } catch (error) {
            console.log(error);
            setInProcess(false);
        };
    };

    return (
        <div>
            <span>Generate Report {"\u00A0"}</span>
            <br></br>
            <button
            onClick={reportTaskSelect}>
                <FontAwesomeIcon icon={faFilePdf} />
            </button>
            {modalOpen && <Modal onClose={(e) => setModalOpen(false)}>
                <div>
                    <CheckboxSelector
                    title={currentApp === "qualitycontrol" ? 
                        "Select the tasks to be included in the report" : 
                        "Click button to generate report"
                    }
                    optionList={taskList} 
                    setOptionList={setTaskList} 
                    selectedOptions={selectedTasks} 
                    setSelectedOptions={setSelectedTasks} 
                    direction={"column"}></CheckboxSelector>  
                    <button onClick={generateReport}>
                        Submit
                    </button>
                    {inProcess ? <FontAwesomeIcon icon={faSpinner} className="fa-spin" /> : <></>}
                </div>
            </Modal>}    
            <button onClick={() => viewReport(`${currentApp}.pdf`)}>view</button>
            <button onClick={(e) => setDownloadModalOpen(true)}>
                <FontAwesomeIcon icon={faDownload} />
            </button>
            {downloadModalOpen && <Modal onClose={(e) => setDownloadModalOpen(false)}>
                <div>
                    <CheckboxSelector
                    title={"Select files to be downloaded"} 
                    optionList={currentApp === "qualitycontrol" ? 
                        downloadOptions : cedownloadOptions} 
                    setOptionList={currentApp === "qualitycontrol" ? 
                        setDownloadOptions : setCEDownloadOptions} 
                    selectedOptions={selecetedDownloadOptions} 
                    setSelectedOptions={setSelctedDownloadOptions} 
                    direction={"column"} 
                    singleChoice={true}></CheckboxSelector>
                    <button onClick={downloadReport}>
                        Submit
                    </button>
                    {inProcess ? <FontAwesomeIcon icon={faSpinner} className="fa-spin" /> : <></>}
                </div>    
            </Modal>}
        </div>
    );
};

export default ReportGenerator;