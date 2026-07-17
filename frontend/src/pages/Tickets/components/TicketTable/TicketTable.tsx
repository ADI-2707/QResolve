import Badge from "../../../../components/common/ui/Badge/Badge";
import Card from "../../../../components/common/ui/Card/Card";
import type { Ticket } from "../../../../types/ticket";
import styles from "./TicketTable.module.css";

interface TicketTableProps {
    tickets: Ticket[];
    loading: boolean;
    error: string | null;
}

const priorityVariant = (priority: Ticket["priority"]) => {
    if (priority === "CRITICAL") return "danger" as const;
    if (priority === "HIGH") return "warning" as const;
    if (priority === "LOW") return "success" as const;
    return "info" as const;
};

const TicketTable = ({ tickets, loading, error }: TicketTableProps) => {
    if (loading) return <Card title="Tickets">Loading tickets…</Card>;
    if (error) return <Card title="Tickets">{error}</Card>;
    if (!tickets.length) return <Card title="Tickets">No tickets match these filters.</Card>;

    return (
        <Card title="Tickets">
            <div className={styles.table}>
                <div className={styles.header}>
                    <span>Subject</span><span>Category</span><span>Priority</span><span>Status</span><span>Updated</span>
                </div>
                {tickets.map((ticket) => (
                    <div key={ticket.id} className={styles.row}>
                        <span>{ticket.subject}</span>
                        <span>{ticket.category.replace("_", " ").toLowerCase()}</span>
                        <Badge variant={priorityVariant(ticket.priority)}>{ticket.priority.toLowerCase()}</Badge>
                        <span>{ticket.status.replace("_", " ").toLowerCase()}</span>
                        <span>{new Date(ticket.updated_at).toLocaleDateString()}</span>
                    </div>
                ))}
            </div>
        </Card>
    );
};

export default TicketTable;
