import api from "./api";
import type { BootstrapPayload, LoginPayload, Session } from "../types/auth";

export const login = async (payload: LoginPayload) => {
    const response = await api.post<Session>("/auth/login", payload);
    return response.data;
};

export const bootstrap = async (payload: BootstrapPayload) => {
    const response = await api.post<Session>("/auth/bootstrap", payload);
    return response.data;
};
