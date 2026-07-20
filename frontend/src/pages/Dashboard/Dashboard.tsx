import { useEffect, useState } from "react";
import StatsCard from "./components/StatsCard/StatsCard";
import PriorityOverview from "./components/PriorityOverview/PriorityOverview";
import RecentTickets from "./components/RecentTickets/RecentTickets";
import { getTicketAnalytics } from "../../services/analyticsService";
import { getTickets } from "../../services/ticketService";
import type { TicketAnalytics } from "../../types/analytics";
import type { Ticket } from "../../types/ticket";
import styles from "./Dashboard.module.css";

const Dashboard = () => {
    const [analytics, setAnalytics] = useState<TicketAnalytics | null>(null);
    const [recentTickets, setRecentTickets] = useState<Ticket[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                const [overview, tickets] = await Promise.all([getTicketAnalytics(), getTickets({ page: 1, page_size: 5 })]);
                setAnalytics(overview);
                setRecentTickets(tickets.tickets);
            } catch {
                setError("Unable to load the dashboard.");
            }
        };
        void loadDashboard();
    }, []);

    return <div className={styles.dashboard}>
        <header className={styles.header}><h1 className={styles.title}>Dashboard</h1><p className={styles.subtitle}>Support ticket intelligence overview</p></header>
        {error && <p>{error}</p>}
        <section className={styles.stats}>
            <StatsCard title="Total tickets" value={analytics?.total_tickets ?? "—"} />
            <StatsCard title="Open tickets" value={analytics?.open_tickets ?? "—"} />
            <StatsCard title="In progress" value={analytics?.in_progress_tickets ?? "—"} />
            <StatsCard title="Resolved" value={analytics?.resolved_tickets ?? "—"} />
        </section>
        <PriorityOverview priorities={analytics?.tickets_by_priority ?? {}} />
        <RecentTickets tickets={recentTickets} />
    </div>;
};

export default Dashboard;
