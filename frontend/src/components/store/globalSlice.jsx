const createGlobalSlice = (set) => ({
    isAuthenticated: false, 
    setIsAuthenticated: (newState) => set((state) => ({isAuthenticated: newState})), 

    username: "", 
    setUsername: (newName) => set((state) => ({username: newName})), 

    testMode: true, 
    setTestMode: (newState) => set((state) => ({testMode: newState})),

    sessionList: [], 
    setSessionList: (newList) => set((state) => ({sessionList: newList})),

    autoPageDataFetch: async(pageName) => {
        try {
            const response = await fetch(
                `/api/load/${pageName}`, {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}
                }); 
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            const data = await response.json();
            console.log(data);
            if (data.isAuthenticated) {
                set({isAuthenticated: data.isAuthenticated, 
                     username: data.username})
            } else {
                set({isAuthenticated: data.isAuthenticated, 
                    username: ""})
            }
            if (pageName === "dashboard") {
                set({sessionList: data.sessionList});
            }
        } catch (error) {
            console.log(error)
        };
    },

});

export default createGlobalSlice;