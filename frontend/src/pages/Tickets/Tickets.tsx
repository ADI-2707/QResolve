import { useState } from "react";
import Button from "../../components/common/ui/Button/Button";
import { useTickets } from "../../hooks/useTickets";
import type { TicketQuery } from "../../types/ticket";
import TicketFilters from "./components/TicketFilters/TicketFilters";
import TicketTable from "./components/TicketTable/TicketTable";
import styles from "./Tickets.module.css";

const PAGE_SIZE = 25;

const Tickets = () => {
    const [query, setQuery] = useState<TicketQuery>({ page: 1, page_size: PAGE_SIZE });
    const { tickets, totalItems, totalPages, loading, error } = useTickets(query);

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1>Tickets</h1>
                <p>Manage and analyze customer support tickets</p>
            </header>
            <TicketFilters onApply={(filters) => setQuery({ ...filters, page: 1, page_size: PAGE_SIZE })} />
            <TicketTable tickets={tickets} loading={loading} error={error} />
            {!loading && !error && totalItems > 0 && (
                <footer className={styles.pagination}>
                    <span>{totalItems} ticket{totalItems === 1 ? "" : "s"}</span>
                    <div>
                        <Button variant="secondary" onClick={() => setQuery((current) => ({ ...current, page: Math.max(1, (current.page || 1) - 1) }))}>Previous</Button>
                        <span>Page {query.page} of {totalPages}</span>
                        <Button variant="secondary" onClick={() => setQuery((current) => ({ ...current, page: Math.min(totalPages, (current.page || 1) + 1) }))}>Next</Button>
                    </div>
                </footer>
            )}
        </div>
    );
};

export default Tickets;
