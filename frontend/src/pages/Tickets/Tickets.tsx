import { type FormEvent, useState } from "react";
import axios from "axios";
import Button from "../../components/common/ui/Button/Button";
import Card from "../../components/common/ui/Card/Card";
import { useTickets } from "../../hooks/useTickets";
import { claimTicket, createTicket, resolveTicket } from "../../services/ticketService";
import type { TicketCategory, TicketPriority, TicketQuery } from "../../types/ticket";
import TicketFilters from "./components/TicketFilters/TicketFilters";
import TicketTable from "./components/TicketTable/TicketTable";
import styles from "./Tickets.module.css";

const PAGE_SIZE = 25;
const requestError = (error: unknown) => axios.isAxiosError(error) ? error.response?.data?.detail || "Request failed." : "Request failed.";

const Tickets = () => {
    const [query, setQuery] = useState<TicketQuery>({ page: 1, page_size: PAGE_SIZE });
    const { tickets, totalItems, totalPages, loading, error, reload } = useTickets(query);
    const [subject, setSubject] = useState("");
    const [description, setDescription] = useState("");
    const [priority, setPriority] = useState<TicketPriority>("MEDIUM");
    const [category, setCategory] = useState<TicketCategory>("OTHER");
    const [actionError, setActionError] = useState<string | null>(null);

    const create = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setActionError(null);
        try {
            await createTicket({ subject, description, priority, category });
            setSubject("");
            setDescription("");
            reload();
        } catch (request) {
            setActionError(requestError(request));
        }
    };
    
    const runAction = async (action: (id: string) => Promise<unknown>, id: string) => {
        setActionError(null);
        try {
            await action(id);
            reload();
        } catch (request) {
            setActionError(requestError(request));
        }
    };

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1>Tickets</h1>
                <p>Manage and analyze customer support tickets</p>
            </header>

            <Card title="Create Support Ticket">
                <form className={styles.createForm} onSubmit={create}>
                    <div className={styles.formGroup}>
                        <label htmlFor="ticket-subject" className={styles.label}>Subject</label>
                        <input
                            id="ticket-subject"
                            className={styles.input}
                            placeholder="Brief summary of the issue..."
                            value={subject}
                            onChange={(event) => setSubject(event.target.value)}
                            minLength={3}
                            required
                        />
                    </div>
                    
                    <div className={styles.formGroup}>
                        <label htmlFor="ticket-description" className={styles.label}>Description</label>
                        <textarea
                            id="ticket-description"
                            className={styles.textarea}
                            placeholder="Please explain the problem in detail, including steps to reproduce..."
                            value={description}
                            onChange={(event) => setDescription(event.target.value)}
                            minLength={10}
                            required
                            rows={3}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <div className={styles.formGroup}>
                            <label htmlFor="ticket-priority" className={styles.label}>Priority</label>
                            <select
                                id="ticket-priority"
                                className={styles.select}
                                value={priority}
                                onChange={(event) => setPriority(event.target.value as TicketPriority)}
                            >
                                <option value="LOW">Low</option>
                                <option value="MEDIUM">Medium</option>
                                <option value="HIGH">High</option>
                                <option value="CRITICAL">Critical</option>
                            </select>
                        </div>

                        <div className={styles.formGroup}>
                            <label htmlFor="ticket-category" className={styles.label}>Category</label>
                            <select
                                id="ticket-category"
                                className={styles.select}
                                value={category}
                                onChange={(event) => setCategory(event.target.value as TicketCategory)}
                            >
                                <option value="OTHER">Other</option>
                                <option value="TECHNICAL">Technical</option>
                                <option value="BILLING">Billing</option>
                                <option value="ACCOUNT">Account</option>
                                <option value="BUG">Bug</option>
                                <option value="FEATURE_REQUEST">Feature request</option>
                            </select>
                        </div>

                        <div className={styles.formSubmit}>
                            <Button type="submit">Create Ticket</Button>
                        </div>
                    </div>
                </form>
                {actionError && <p className={styles.error}>{actionError}</p>}
            </Card>

            <TicketFilters onApply={(filters) => setQuery({ ...filters, page: 1, page_size: PAGE_SIZE })} />

            <TicketTable
                tickets={tickets}
                loading={loading}
                error={error}
                onClaim={(id) => void runAction(claimTicket, id)}
                onResolve={(id) => void runAction(resolveTicket, id)}
            />

            {!loading && !error && totalItems > 0 && (
                <footer className={styles.pagination}>
                    <span>{totalItems} ticket{totalItems === 1 ? "" : "s"}</span>
                    <div>
                        <Button
                            variant="secondary"
                            onClick={() => setQuery((current) => ({ ...current, page: Math.max(1, (current.page || 1) - 1) }))}
                        >
                            Previous
                        </Button>
                        <span>Page {query.page} of {totalPages}</span>
                        <Button
                            variant="secondary"
                            onClick={() => setQuery((current) => ({ ...current, page: Math.min(totalPages, (current.page || 1) + 1) }))}
                        >
                            Next
                        </Button>
                    </div>
                </footer>
            )}
        </div>
    );
};

export default Tickets;
