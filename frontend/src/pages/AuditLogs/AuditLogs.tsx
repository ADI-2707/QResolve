import { useCallback, useEffect, useState } from "react";
import Card from "../../components/common/ui/Card/Card";
import Button from "../../components/common/ui/Button/Button";
import { getAuditLogs } from "../../services/auditService";
import type { AuditLog } from "../../types/audit";
import styles from "./AuditLogs.module.css";

const PAGE_SIZE = 25;

const AuditLogs = () => {
    const [events, setEvents] = useState<AuditLog[]>([]);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [hasMore, setHasMore] = useState(false);

    const load = useCallback(async (p: number) => {
        setLoading(true);
        setError(null);
        try {
            const data = await getAuditLogs(p, PAGE_SIZE);
            setEvents(data.events);
            setHasMore(data.events.length === PAGE_SIZE);
        } catch {
            setError("Unable to load audit logs.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { void load(page); }, [load, page]);

    const formatAction = (action: string) =>
        action.replace(/_/g, " ").toLowerCase().replace(/^\w/, (c) => c.toUpperCase());

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1>Audit Logs</h1>
                <p>Security and activity log for your organization</p>
            </header>

            <Card title="Activity Events">
                {loading && <p className={styles.muted}>Loading events…</p>}
                {error && <p className={styles.error}>{error}</p>}
                {!loading && !error && events.length === 0 && (
                    <p className={styles.muted}>No audit events recorded yet.</p>
                )}
                {!loading && !error && events.length > 0 && (
                    <>
                        <div className={styles.table}>
                            <div className={styles.tableHeader}>
                                <span>Timestamp</span>
                                <span>Action</span>
                                <span>Entity Type</span>
                                <span>Entity</span>
                                <span>Actor</span>
                            </div>
                            {events.map((event) => (
                                <div key={event.id} className={styles.tableRow}>
                                    <span className={styles.timestamp}>
                                        {new Date(event.created_at).toLocaleString()}
                                    </span>
                                    <span className={styles.action}>{formatAction(event.action)}</span>
                                    <span className={styles.muted}>{event.entity_type}</span>
                                    <span className={styles.mono} title={event.entity_id}>
                                        {event.entity_id.slice(0, 8)}…
                                    </span>
                                    <span className={styles.mono} title={event.actor_id ?? "system"}>
                                        {event.actor_id ? `${event.actor_id.slice(0, 8)}…` : "system"}
                                    </span>
                                </div>
                            ))}
                        </div>
                        <footer className={styles.pagination}>
                            <Button
                                variant="secondary"
                                onClick={() => setPage((p) => Math.max(1, p - 1))}
                                disabled={page === 1}
                            >
                                Previous
                            </Button>
                            <span className={styles.muted}>Page {page}</span>
                            <Button
                                variant="secondary"
                                onClick={() => setPage((p) => p + 1)}
                                disabled={!hasMore}
                            >
                                Next
                            </Button>
                        </footer>
                    </>
                )}
            </Card>
        </div>
    );
};

export default AuditLogs;
