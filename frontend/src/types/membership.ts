export type MembershipRole = "PLATFORM_ADMIN" | "ORGANIZATION_ADMIN" | "MANAGER" | "AGENT" | "VIEWER";
export type MembershipStatus = "INVITED" | "ACTIVE" | "SUSPENDED" | "ARCHIVED";

export interface Membership {
    id: string;
    organization_id: string;
    user_id: string;
    role: MembershipRole;
    status: MembershipStatus;
    created_at: string;
    accepted_at: string | null;
}

export interface InvitationResponse {
    id: string;
    email: string;
    role: MembershipRole;
    expires_at: string;
    invitation_token: string;
}
