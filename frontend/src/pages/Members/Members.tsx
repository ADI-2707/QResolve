import { type FormEvent, useCallback, useEffect, useState } from "react";
import axios from "axios";
import Button from "../../components/common/ui/Button/Button";
import Card from "../../components/common/ui/Card/Card";
import Badge from "../../components/common/ui/Badge/Badge";
import {
    listMemberships,
    changeMembershipRole,
    suspendMembership,
    activateMembership,
    createInvitation,
} from "../../services/membershipService";
import type { Membership, MembershipRole } from "../../types/membership";
import type { InvitationResponse } from "../../types/membership";
import styles from "./Members.module.css";

const requestError = (error: unknown) =>
    axios.isAxiosError(error) ? error.response?.data?.detail || "Request failed." : "Request failed.";

const roleVariant = (role: MembershipRole) => {
    if (role === "ORGANIZATION_ADMIN") return "danger" as const;
    if (role === "MANAGER") return "warning" as const;
    if (role === "AGENT") return "info" as const;
    return "info" as const;
};

const statusVariant = (status: Membership["status"]) => {
    if (status === "ACTIVE") return "success" as const;
    if (status === "SUSPENDED") return "danger" as const;
    if (status === "INVITED") return "warning" as const;
    return "info" as const;
};

const ROLES: MembershipRole[] = ["VIEWER", "AGENT", "MANAGER", "ORGANIZATION_ADMIN"];

const Members = () => {
    const [memberships, setMemberships] = useState<Membership[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [actionError, setActionError] = useState<string | null>(null);

    // Invite form state
    const [inviteEmail, setInviteEmail] = useState("");
    const [inviteRole, setInviteRole] = useState<MembershipRole>("AGENT");
    const [inviteResult, setInviteResult] = useState<InvitationResponse | null>(null);
    const [inviting, setInviting] = useState(false);

    const load = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            setMemberships(await listMemberships());
        } catch (e) {
            setError(requestError(e));
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { void load(); }, [load]);

    const runAction = async (action: () => Promise<Membership>) => {
        setActionError(null);
        try {
            await action();
            await load();
        } catch (e) {
            setActionError(requestError(e));
        }
    };

    const invite = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setActionError(null);
        setInviteResult(null);
        setInviting(true);
        try {
            const result = await createInvitation(inviteEmail, inviteRole);
            setInviteResult(result);
            setInviteEmail("");
            await load();
        } catch (e) {
            setActionError(requestError(e));
        } finally {
            setInviting(false);
        }
    };

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1>Members</h1>
                <p>Manage your organization's members and their access roles</p>
            </header>

            <Card title="Invite New Member">
                <form className={styles.inviteForm} onSubmit={invite}>
                    <div className={styles.formGroup}>
                        <label htmlFor="invite-email" className={styles.label}>Email address</label>
                        <input
                            id="invite-email"
                            type="email"
                            className={styles.input}
                            placeholder="colleague@company.com"
                            value={inviteEmail}
                            onChange={(e) => setInviteEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label htmlFor="invite-role" className={styles.label}>Role</label>
                        <select
                            id="invite-role"
                            className={styles.select}
                            value={inviteRole}
                            onChange={(e) => setInviteRole(e.target.value as MembershipRole)}
                        >
                            <option value="VIEWER">Viewer</option>
                            <option value="AGENT">Agent</option>
                            <option value="MANAGER">Manager</option>
                            <option value="ORGANIZATION_ADMIN">Organization Admin</option>
                        </select>
                    </div>
                    <div className={styles.formSubmit}>
                        <Button type="submit" disabled={inviting}>{inviting ? "Sending…" : "Send Invitation"}</Button>
                    </div>
                </form>

                {inviteResult && (
                    <div className={styles.tokenBox}>
                        <p className={styles.tokenLabel}>✅ Invitation created. Share this token with <strong>{inviteResult.email}</strong>:</p>
                        <code className={styles.token}>{inviteResult.invitation_token}</code>
                        <p className={styles.tokenHint}>They should use this token at <strong>/login</strong> → accept invitation flow.</p>
                    </div>
                )}
                {actionError && <p className={styles.error}>{actionError}</p>}
            </Card>

            <Card title="Organization Members">
                {loading && <p className={styles.muted}>Loading members…</p>}
                {error && <p className={styles.error}>{error}</p>}
                {!loading && !error && memberships.length === 0 && (
                    <p className={styles.muted}>No members found.</p>
                )}
                {!loading && !error && memberships.length > 0 && (
                    <div className={styles.table}>
                        <div className={styles.tableHeader}>
                            <span>User ID</span>
                            <span>Role</span>
                            <span>Status</span>
                            <span>Joined</span>
                            <span>Actions</span>
                        </div>
                        {memberships.map((m) => (
                            <div key={m.id} className={styles.tableRow}>
                                <span className={styles.userId} title={m.user_id}>{m.user_id.slice(0, 8)}…</span>
                                <span>
                                    <Badge variant={roleVariant(m.role)}>{m.role.replace("_", " ").toLowerCase()}</Badge>
                                </span>
                                <span>
                                    <Badge variant={statusVariant(m.status)}>{m.status.toLowerCase()}</Badge>
                                </span>
                                <span className={styles.muted}>
                                    {m.accepted_at ? new Date(m.accepted_at).toLocaleDateString() : "—"}
                                </span>
                                <span className={styles.actions}>
                                    {m.status === "ACTIVE" && (
                                        <>
                                            {ROLES.filter((r) => r !== m.role && r !== "PLATFORM_ADMIN").map((r) => (
                                                <Button
                                                    key={r}
                                                    variant="secondary"
                                                    onClick={() => void runAction(() => changeMembershipRole(m.id, r))}
                                                >
                                                    → {r.replace("_", " ").toLowerCase()}
                                                </Button>
                                            ))}
                                            <Button
                                                variant="secondary"
                                                onClick={() => void runAction(() => suspendMembership(m.id))}
                                            >
                                                Suspend
                                            </Button>
                                        </>
                                    )}
                                    {m.status === "SUSPENDED" && (
                                        <Button onClick={() => void runAction(() => activateMembership(m.id))}>
                                            Reactivate
                                        </Button>
                                    )}
                                </span>
                            </div>
                        ))}
                    </div>
                )}
            </Card>
        </div>
    );
};

export default Members;
