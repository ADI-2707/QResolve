import { useState } from "react";
import type { FormEvent } from "react";
import axios from "axios";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/useAuth";
import { login } from "../../services/authService";
import styles from "./Login.module.css";

const Login = () => {
    const { session, signIn } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [organizationSlug, setOrganizationSlug] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    if (session) return <Navigate to="/" replace />;

    const submit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);
        setIsSubmitting(true);

        try {
            const nextSession = await login({
                organization_slug: organizationSlug.trim(),
                email: email.trim(),
                password,
            });
            signIn(nextSession);
            const destination = (location.state as { from?: string } | null)?.from || "/";
            navigate(destination, { replace: true });
        } catch (requestError) {
            setError(axios.isAxiosError(requestError)
                ? requestError.response?.data?.detail || "Unable to sign in. Check your credentials and try again."
                : "Unable to sign in. Please try again.");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <main className={styles.page}>
            <form className={styles.card} onSubmit={submit}>
                <p className={styles.eyebrow}>QResolve</p>
                <h1>Sign in to your workspace</h1>
                <p className={styles.help}>Use the organization slug and account credentials supplied by your administrator.</p>

                <label>
                    Organization slug
                    <input value={organizationSlug} onChange={(event) => setOrganizationSlug(event.target.value)} autoComplete="organization" required />
                </label>
                <label>
                    Email address
                    <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="email" required />
                </label>
                <label>
                    Password
                    <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required />
                </label>

                {error && <p className={styles.error} role="alert">{error}</p>}
                <button type="submit" disabled={isSubmitting}>{isSubmitting ? "Signing in…" : "Sign in"}</button>
            </form>
        </main>
    );
};

export default Login;
