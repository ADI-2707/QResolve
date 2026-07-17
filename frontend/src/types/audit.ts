export interface AuditLog {
    id: string;
    actor_id: string | null;
    action: string;
    entity_type: string;
    entity_id: string;
    metadata: Record<string, unknown> | null;
    created_at: string;
}

export interface AuditLogListResponse {
    events: AuditLog[];
    page: number;
    page_size: number;
}
