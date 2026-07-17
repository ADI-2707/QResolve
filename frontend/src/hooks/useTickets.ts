import { useCallback, useEffect, useState } from "react";
import { getTickets } from "../services/ticketService";
import type { Ticket, TicketQuery } from "../types/ticket";

export const useTickets = (query: TicketQuery) => {
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [totalItems, setTotalItems] = useState(0);
    const [totalPages, setTotalPages] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [reloadKey, setReloadKey] = useState(0);

    useEffect(() => {
        const fetchTickets = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await getTickets(query);
                setTickets(data.tickets);
                setTotalItems(data.total_items);
                setTotalPages(data.total_pages);
            } catch {
                setError("Failed to load tickets. Please try again.");
            } finally {
                setLoading(false);
            }
        };

        void fetchTickets();
    }, [query, reloadKey]);

    const reload = useCallback(() => setReloadKey((current) => current + 1), []);
    return { tickets, totalItems, totalPages, loading, error, reload };
};
