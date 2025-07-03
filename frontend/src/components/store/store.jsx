import { create } from "zustand";
import createGlobalSlice from "./globalSlice";
import createAppSlice from "./appSlice";
import createChatbotSlice from "./chatbotSlice";
import createDevUseSlice from "./devUseSlice";

const useStore = create((...a) => ({
    ...createGlobalSlice(...a), 
    ...createAppSlice(...a), 
    ...createChatbotSlice(...a),
    ...createDevUseSlice(...a),
}))

export default useStore;