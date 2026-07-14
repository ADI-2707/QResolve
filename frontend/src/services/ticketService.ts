import api from "./api";

import type {
    Ticket
} from "../types/ticket";



export const getTickets = async()=>{


    try {

        const response =
        await api.get<Ticket[]>(
            "/tickets"
        );


        return response.data;


    }

    catch(error){


        return [

            {
                id:"QRS-1001",
                subject:"Unable to login",
                description:"User cannot access account",
                type:"Technical",
                priority:"High",
                status:"Open",
                createdAt:"2026-07-14"
            },

            {
                id:"QRS-1002",
                subject:"Payment failed",
                description:"Transaction error",
                type:"Billing",
                priority:"Critical",
                status:"Pending",
                createdAt:"2026-07-14"
            }

        ];

    }


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