import api from "./api";
import type { LoginPayload, Session } from "../types/auth";

export const login = async (payload: LoginPayload) => {
    const response = await api.post<Session>("/auth/login", payload);
    return response.data;
};
