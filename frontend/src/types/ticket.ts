export type TicketPriority =

    | "Critical"
    | "High"
    | "Medium"
    | "Low";



export type TicketStatus =

    | "Open"
    | "Pending"
    | "Closed";



export interface Ticket {


    id:string;


    subject:string;


    description:string;


    type:string;


    priority:TicketPriority;


    status:TicketStatus;


    createdAt:string;

}