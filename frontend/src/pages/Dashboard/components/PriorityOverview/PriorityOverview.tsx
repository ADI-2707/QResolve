import Badge from "../../../../components/common/ui/Badge/Badge";
import Card from "../../../../components/common/ui/Card/Card";
import styles from "./PriorityOverview.module.css";

const variants = { CRITICAL: "danger", HIGH: "warning", MEDIUM: "info", LOW: "success" } as const;

const PriorityOverview = ({ priorities }: { priorities: Record<string, number> }) => <Card title="Priority overview">
    <div className={styles.grid}>
        {Object.entries(variants).map(([priority, variant]) => <div key={priority} className={styles.item}>
            <Badge variant={variant}>{priority.toLowerCase()}</Badge><span>{priorities[priority] ?? 0}</span>
        </div>)}
    </div>
</Card>;

export default PriorityOverview;
