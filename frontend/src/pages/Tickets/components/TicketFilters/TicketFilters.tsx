import { useState } from "react";
import type { FormEvent } from "react";
import Button from "../../../../components/common/ui/Button/Button";
import Input from "../../../../components/common/ui/Input/Input";
import type { TicketPriority, TicketStatus } from "../../../../types/ticket";
import styles from "./TicketFilters.module.css";

interface TicketFiltersProps {
    onApply: (filters: { search?: string; priority?: TicketPriority; status?: TicketStatus }) => void;
}

const TicketFilters = ({ onApply }: TicketFiltersProps) => {
    const [search, setSearch] = useState("");
    const [priority, setPriority] = useState("");
    const [status, setStatus] = useState("");

    const submit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        onApply({
            search: search.trim() || undefined,
            priority: priority ? priority as TicketPriority : undefined,
            status: status ? status as TicketStatus : undefined,
        });
    };

    return (
        <form className={styles.filters} onSubmit={submit}>
            <Input placeholder="Search tickets..." value={search} onChange={(event) => setSearch(event.target.value)} />
            <select className={styles.select} value={priority} onChange={(event) => setPriority(event.target.value)}>
                <option value="">All priorities</option>
                <option value="CRITICAL">Critical</option>
                <option value="HIGH">High</option>
                <option value="MEDIUM">Medium</option>
                <option value="LOW">Low</option>
            </select>
            <select className={styles.select} value={status} onChange={(event) => setStatus(event.target.value)}>
                <option value="">All statuses</option>
                <option value="OPEN">Open</option>
                <option value="IN_PROGRESS">In progress</option>
                <option value="RESOLVED">Resolved</option>
                <option value="CLOSED">Closed</option>
            </select>
            <Button type="submit">Apply filters</Button>
        </form>
    );
};

export default TicketFilters;
