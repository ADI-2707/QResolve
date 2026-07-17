import api from "./api";
import type { AuditLogListResponse } from "../types/audit";

export const getAuditLogs = async (page = 1, pageSize = 25): Promise<AuditLogListResponse> => {
    const response = await api.get<AuditLogListResponse>("/audit", {
        params: { page, page_size: pageSize },
    });
    return response.data;
};
