import Badge from "../../../../components/common/ui/Badge/Badge";
import Card from "../../../../components/common/ui/Card/Card";

import styles from "./RecentTickets.module.css";


const tickets=[

    {
        id:"QRS-1001",
        title:"Login issue",
        priority:"High"
    },

    {
        id:"QRS-1002",
        title:"Payment failed",
        priority:"Critical"
    }

];


const RecentTickets = ()=>{


return (

<Card title="Recent Tickets">


<div className={styles.table}>


{
tickets.map(ticket=>(

<div
key={ticket.id}
className={styles.row}
>

<span>
{ticket.id}
</span>


<span>
{ticket.title}
</span>


<Badge variant={
ticket.priority==="Critical"
?"danger"
:"warning"
}>
{ticket.priority}
</Badge>


</div>

))

}


</div>


</Card>

);


};


export default RecentTickets;