import Badge from "../../../../components/common/ui/Badge/Badge";
import Card from "../../../../components/common/ui/Card/Card";
import type { Ticket } from "../../../../types/ticket";
import styles from "./RecentTickets.module.css";

const RecentTickets = ({ tickets }: { tickets: Ticket[] }) => <Card title="Recent tickets">
    <div className={styles.table}>{tickets.length ? tickets.map((ticket) => <div key={ticket.id} className={styles.row}>
        <span>{ticket.subject}</span><span>{ticket.status.replace("_", " ").toLowerCase()}</span>
        <Badge variant={ticket.priority === "CRITICAL" ? "danger" : ticket.priority === "HIGH" ? "warning" : "info"}>{ticket.priority.toLowerCase()}</Badge>
    </div>) : <span>No recent tickets.</span>}</div>
</Card>;

export default RecentTickets;
