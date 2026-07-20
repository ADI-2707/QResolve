export type TicketPriority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type TicketStatus = "OPEN" | "IN_PROGRESS" | "RESOLVED" | "CLOSED" | "ARCHIVED";
export type TicketCategory = "TECHNICAL" | "BILLING" | "ACCOUNT" | "FEATURE_REQUEST" | "BUG" | "OTHER";

export interface Ticket {
    id: string;
    organization_id: string;
    created_by: string;
    assigned_to: string | null;
    department_id: string | null;
    subject: string;
    description: string;
    priority: TicketPriority;
    status: TicketStatus;
    category: TicketCategory;
    created_at: string;
    updated_at: string;
    archived_at: string | null;
    resolved_at: string | null;
}

export interface TicketListResponse {
    tickets: Ticket[];
    page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
}

export interface TicketQuery {
    page?: number;
    page_size?: number;
    status?: TicketStatus;
    priority?: TicketPriority;
    search?: string;
}
