import api from "./api";
import type { TicketAnalytics } from "../types/analytics";

export const getTicketAnalytics = async () => {
    const response = await api.get<TicketAnalytics>("/analytics/tickets/overview");
    return response.data;
};
