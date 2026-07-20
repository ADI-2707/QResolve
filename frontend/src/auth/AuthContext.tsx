import { createContext, useMemo, useState } from "react";
import type { PropsWithChildren } from "react";
import type { Session } from "../types/auth";

const SESSION_KEY = "qresolve.session";
const TOKEN_KEY = "qresolve.access_token";

interface AuthContextValue {
    session: Session | null;
    signIn: (session: Session) => void;
    signOut: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const readSession = (): Session | null => {
    const serializedSession = localStorage.getItem(SESSION_KEY);
    if (!serializedSession) return null;

    try {
        return JSON.parse(serializedSession) as Session;
    } catch {
        localStorage.removeItem(SESSION_KEY);
        localStorage.removeItem(TOKEN_KEY);
        return null;
    }
};

export const AuthProvider = ({ children }: PropsWithChildren) => {
    const [session, setSession] = useState<Session | null>(readSession);
    const value = useMemo<AuthContextValue>(() => ({
        session,
        signIn: (nextSession) => {
            localStorage.setItem(SESSION_KEY, JSON.stringify(nextSession));
            localStorage.setItem(TOKEN_KEY, nextSession.access_token);
            setSession(nextSession);
        },
        signOut: () => {
            localStorage.removeItem(SESSION_KEY);
            localStorage.removeItem(TOKEN_KEY);
            setSession(null);
        },
    }), [session]);

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export { AuthContext };
