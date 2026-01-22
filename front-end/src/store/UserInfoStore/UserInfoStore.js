import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useUserInfoStore = create(
    persist(
        (set) => ({
            user: null,
            username: "",
            email: "",
            userId: null,

            accessToken: null,
            refreshToken: null,

            isAuthenticated: false,

            setUser: (userData) => set({
                user: userData,
                username: userData?.username || "",
                email: userData?.email || "",
                userId: userData?.id || null,
                isAuthenticated: true,
            }),

            setTokens: (access, refresh) => {
                set({
                    accessToken: access,
                    refreshToken: refresh,
                });

                if (access) localStorage.setItem("token", access);
                if (refresh) localStorage.setItem("refresh", refresh);
            },

            login: (userData, tokens) => {
                set({
                    user: userData,
                    username: userData?.username || "",
                    email: userData?.email || "",
                    userId: userData?.id || null,
                    accessToken: tokens.access,
                    refreshToken: tokens.refresh,
                    isAuthenticated: true,
                });

                // Store tokens in localStorage
                localStorage.setItem("token", tokens.access);
                localStorage.setItem("refresh", tokens.refresh);
            },

            logout: () => {
                set({
                    user: null,
                    username: "",
                    email: "",
                    userId: null,
                    accessToken: null,
                    refreshToken: null,
                    isAuthenticated: false,
                });

                // Clear localStorage
                localStorage.removeItem("token");
                localStorage.removeItem("refresh");
            },

            // Legacy setters for backward compatibility
            setUserName: (username) => set({ username }),
            setUserEmail: (email) => set({ email }),
        }),
        {
            name: "user-storage", // localStorage key
            partialize: (state) => ({
                user: state.user,
                username: state.username,
                email: state.email,
                userId: state.userId,
                accessToken: state.accessToken,
                refreshToken: state.refreshToken,
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);