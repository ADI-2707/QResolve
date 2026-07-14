import api from "./api";

import type {
    Ticket
} from "../types/ticket";



export const getTickets = async()=>{


    const response =
    await api.get<Ticket[]>(
        "/tickets"
    );


    return response.data;

};



export const getTicketById = async(
    id:string
)=>{


    const response =
    await api.get<Ticket>(
        `/tickets/${id}`
    );


    return response.data;

};



export const createTicket = async(
    ticket:Partial<Ticket>
)=>{


    const response =
    await api.post<Ticket>(
        "/tickets",
        ticket
    );


    return response.data;

};