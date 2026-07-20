export interface TicketAnalytics {
    total_tickets: number;
    open_tickets: number;
    in_progress_tickets: number;
    resolved_tickets: number;
    tickets_by_priority: Record<string, number>;
    tickets_by_status: Record<string, number>;
}
