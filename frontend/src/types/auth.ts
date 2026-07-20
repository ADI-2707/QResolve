export interface LoginPayload {
    organization_slug: string;
    email: string;
    password: string;
}

export interface BootstrapPayload {
    organization_name: string;
    first_name: string;
    last_name: string;
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
