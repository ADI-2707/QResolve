export interface LoginPayload {
    organization_slug: string;
    email: string;
    password: string;
}

export interface Session {
    access_token: string;
    token_type: "bearer";
    organization_id: string;
    organization_slug: string;
    role: string;
}
