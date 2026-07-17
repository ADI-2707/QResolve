import api from "./api";
import type { Ticket, TicketListResponse, TicketQuery } from "../types/ticket";

export const getTickets = async (query: TicketQuery = {}) => {
    const response = await api.get<TicketListResponse>("/tickets", { params: query });
    return response.data;
};

export const getTicketById = async (id: string) => {
    const response = await api.get<Ticket>(`/tickets/${id}`);
    return response.data;
};

export const createTicket = async (ticket: Pick<Ticket, "subject" | "description" | "priority" | "category">) => {
    const response = await api.post<Ticket>("/tickets", ticket);
    return response.data;
};

export const claimTicket = async (ticketId: string) => {
    const response = await api.post<Ticket>(`/tickets/${ticketId}/claim`);
    return response.data;
};

export const resolveTicket = async (ticketId: string) => {
    const response = await api.post<Ticket>(`/tickets/${ticketId}/resolve`);
    return response.data;
};
