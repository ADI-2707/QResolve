import api from "./api";
import type { Comment } from "../types/comment";

export const listComments = async (ticketId: string): Promise<Comment[]> => {
    const response = await api.get<Comment[]>(`/tickets/${ticketId}/comments`);
    return response.data;
};

export const createComment = async (ticketId: string, content: string): Promise<Comment> => {
    const response = await api.post<Comment>(`/tickets/${ticketId}/comments`, { content });
    return response.data;
};
