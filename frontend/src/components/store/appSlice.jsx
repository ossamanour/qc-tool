const createAppSlice = (set) => ({
    currentApp: "",
    setCurrentApp: (newApp) => set((state) => ({currentApp: newApp})),
    
    currentSession: {}, 
    setCurrentSession: (newSession) => set((state) => ({currentSession: newSession})), 

    currentPage: 0, 
    setCurrentPage: (newPage) => set((state) => ({currentPage: newPage})), 

    currentDisplay: "AIAEC-logo.png", 
    setCurrentDisplay: (newDisplay) => set((state) => ({currentDisplay: newDisplay})), 

    submittedTasks: [], 
    setSubmittedTasks: (newTasks) => set((state) => ({submittedTasks: newTasks})),

    keynoteNumber: 0,
    setKeynoteNumber: (newNumber) => set((state) => ({keynoteNumber: newNumber})), 

    taskLog: [], 
    setTaskLog: (newLog) => set((state) => ({taskLog: [...state.taskLog, newLog]})),
    
    initializeApp: async(appName) => {
        const sendData = {"currentApp": appName}
        try {
            const response = await fetch(
                `/api/load/initialize_app`, {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(sendData)
                }); 
            if (!response.ok) {
                throw new Error(response.statusText); 
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                set({
                    currentApp: appName, 
                    currentSession: {}, 
                    currentPage: 0, 
                    currentDisplay: "AIAEC-logo.png", 
                    submittedTasks: [], 
                    taskLog: [],
                });
            };
        } catch (error) {
            console.log(error);
        };
    },

    appInfo: async(appName) => {
        const sendData = {"currentApp": appName}
        try {
            const response = await fetch(
                `/api/load/app_info`, {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}, 
                    body: JSON.stringify(sendData)
                }); 
            if (!response.ok) {
                throw new Error(response.statusText); 
            }
            const data = await response.json();
            console.log(data);
            if (data.status) {
                set({
                    currentApp: appName,
                    currentSession: data.currentSession,  
                    currentPage: data.currentPage,
                    currentDisplay: data.currentDisplay
                });
            };
        } catch (error) {
            console.log(error);
        };
    },

    moduleFetchData: async(moduleName) => {
        try {
            const response = await fetch(
                `/api/module/${moduleName}`, {
                method: "POST", 
                credentials: "include", 
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            console.log(data);
            if (data.currentDisplay) {
                set({currentDisplay: data.currentDisplay});
            } else {
                console.log("no display");
            };
            return data;
        } catch (error) {
            console.log(error);
        };
    },

    singleKeynoteMatchFetch: async(keynoteIndex) => {
        try {
            const response = await fetch(`/api/module/keynote-match/${keynoteIndex}`, {
                method: "POST", 
                credentials: "include", 
                headers: {"Content-Type": "application/json"}});
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.currentDisplay) {
                set({currentDisplay: data.currentDisplay});
            } else {
                console.log("no display");
            };
            return data;
            // setProgress(currentIndex/keynoteNum);
            // console.log(currentIndex/keynoteNum)
        } catch(error) {
            console.log(error);
        };
    },
});

export default createAppSlice;