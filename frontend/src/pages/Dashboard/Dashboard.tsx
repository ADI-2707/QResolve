import StatsCard from "./components/StatsCard/StatsCard";
import PriorityOverview from "./components/PriorityOverview/PriorityOverview";
import RecentTickets from "./components/RecentTickets/RecentTickets";

import styles from "./Dashboard.module.css";


const Dashboard = ()=>{


return (

<div className={styles.dashboard}>


<header className={styles.header}>

<h1 className={styles.title}>
Dashboard
</h1>

<p className={styles.subtitle}>
Support ticket intelligence overview
</p>

</header>



<section className={styles.stats}>


<StatsCard
title="Total Tickets"
value="8,469"
/>


<StatsCard
title="High Priority"
value="342"
/>


<StatsCard
title="Pending"
value="120"
/>


<StatsCard
title="Resolved"
value="7,890"
/>


</section>



<PriorityOverview/>


<RecentTickets/>


</div>

);


};


export default Dashboard;