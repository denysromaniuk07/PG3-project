import { create } from "zustand"


export const useUserInfoStore = create((set) => ({
    username: "",
    email: "",
    setUserName: (username) => set({ username: username }),
    setUserEmail: (email) => set({email: email}) 
}))