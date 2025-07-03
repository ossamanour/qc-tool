const createChatbotSlice = (set) => ({
    chatbotInUse: false, 
    setChatbotInUse: (newState) => set((state) => ({chatbotInUse: newState})),

    loadSessionInfo: false, 
    setLoadSessionInfo: (newState) => set((state) => ({loadSessionInfo: newState})),

    cityList: [], 
    setCityList: (newList) => set((state) => ({cityList: newList})), 

    selectedCity: "SCOTTSDALE",
    setSelectedCity: (newCity) => set((state) => ({selectedCity: newCity})),

    selectedZone: "", 
    setSelectedZone: (newZone) => set((state) => ({selectedZone: newZone})),

    useTool: false, 
    setUseTool: (newState) => set((state) => ({useTool: newState})),

    autoChatBotDataFetch: async() => {
        try {
            const response = await fetch(
                `/api/chatbot/data-fetch`, {
                    method: "POST", 
                    credentials: "include", 
                    headers: {"Content-Type": "application/json"}
                }); 
            if (!response.ok) {
                throw new Error(response.statusText);
            };
            const data = await response.json();
            console.log(data);
            if (data.status) {
                if (data.existInfo) {
                    set({
                        selectedZone: data.zone,
                        selectedCity: data.city, 
                        loadSessionInfo: true,
                    });
                } else {
                    set({
                        loadSessionInfo: false,
                        cityList: data.cityList,
                    })
                };
            } else {
                alert(data.errorMessage);
            };
        } catch (error) {
            console.log(error);
        };
    },
});

export default createChatbotSlice;