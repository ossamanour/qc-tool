import React, { useContext, useState, useEffect } from "react";
import { createRoot } from "react-dom/client";

const ParentWindow = ({ funcBeforeOpen, children, title, icon }) => {

    const openNewWindow = async() => {
        if (funcBeforeOpen) {
            const data = await funcBeforeOpen();
            if (!data) {
                return;
            };
        }

        // create a popup window
        const newWindow = window.open("", "_blank", "width=500, height=300");
        const cssLink = document.createElement("link")
        cssLink.rel = "stylesheet"
        cssLink.type = "text/css"
        cssLink.href = "./ParentWindow.css"
        newWindow.document.head.appendChild(cssLink);
        newWindow.document.body.innerHTML = `
        <html>
            <head>
                <title>${title}</title>
                <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">
            </head>
            <body>
                <div id="root"></div>
            </body>
        </html>
        `;


        // add linstener

        // let app = document.querySelector("../App");
        // let compStyles = window.getComputedStyle(app);
        // const el = newWindow.document.getElementById("root")
        // el.style = compStyles
        
        const closeWindow = () => {
            console.log("close")
            newWindow.close();
        };
        
        // add children components in the new window
        if (newWindow) {
            createRoot(newWindow.document.getElementById("root")).render(
                // <GlobalStateContext.Provider value={{state, dispatch}}>
                <>
                    {React.Children.map(children, child => {
                        if (React.isValidElement(child)) {
                            return React.cloneElement(child, {onClose: closeWindow})
                        }
                        return child;
                    } )}
                </>
                // </GlobalStateContext.Provider>
            )

            // newWindow.document.addEventListener("mousemove", (event) => {
            //     console.log('Mouse position:', event.clientX, event.clientY);
            // })
        }
    }

    return (
        <>
        <button onClick={openNewWindow}>
            {icon}
        </button>
        </>
    )
};

export default ParentWindow;