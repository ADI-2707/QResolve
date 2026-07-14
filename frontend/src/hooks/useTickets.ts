import { useEffect, useState } from "react";

import {
    getTickets
} from "../services/ticketService";

import type {
    Ticket
} from "../types/ticket";


const useTickets = () => {


    const [tickets, setTickets] =
        useState<Ticket[]>([]);


    const [loading, setLoading] =
        useState(true);


    const [error, setError] =
        useState<string | null>(null);



    useEffect(()=>{


        const fetchTickets = async()=>{


            try {

                setLoading(true);


                const data =
                await getTickets();


                setTickets(data);


            }

            catch(error){


                setError(
                    "Failed to load tickets"
                );


            }

            finally {


                setLoading(false);


            }


        };


        fetchTickets();


    },[]);



    return {

        tickets,

        loading,

        error

    };


};


export default useTickets;