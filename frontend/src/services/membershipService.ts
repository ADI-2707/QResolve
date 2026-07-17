import api from "./api";
import type { Membership, InvitationResponse } from "../types/membership";

export const listMemberships = async (): Promise<Membership[]> => {
    const response = await api.get<Membership[]>("/memberships");
    return response.data;
};

export const changeMembershipRole = async (membershipId: string, role: string): Promise<Membership> => {
    const response = await api.patch<Membership>(`/memberships/${membershipId}/role`, { role });
    return response.data;
};

export const suspendMembership = async (membershipId: string): Promise<Membership> => {
    const response = await api.post<Membership>(`/memberships/${membershipId}/suspend`);
    return response.data;
};

export const activateMembership = async (membershipId: string): Promise<Membership> => {
    const response = await api.post<Membership>(`/memberships/${membershipId}/activate`);
    return response.data;
};

export const createInvitation = async (email: string, role: string): Promise<InvitationResponse> => {
    const response = await api.post<InvitationResponse>("/invitations", { email, role });
    return response.data;
};
