import React, { useEffect, useState } from "react";
import useStore from "../../../../components/store/store";

const KeynoteMatch = ({setComplete, setInformation, taskId}) => {
    const {singleKeynoteMatchFetch, keynoteNumber} = useStore();
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        const performMatching = async() => {
            let data;
            for (let i = 0; i < keynoteNumber; i++) {
                setCurrentIndex(i+1);
                data = await singleKeynoteMatchFetch(i);
                if (data.message) {
                    setInformation(taskId, data.message);
                }
            };
            setComplete();
        };

        performMatching();
    }, []);

    return (
        <div>
            <h3>Keynote Match</h3>
            <p>Total Keynote Number: {keynoteNumber}</p>
            <p>Matching in keynote {currentIndex}</p>
            <progress value={currentIndex} max={keynoteNumber}></progress>
        </div>
    );
}; 

export default KeynoteMatch;