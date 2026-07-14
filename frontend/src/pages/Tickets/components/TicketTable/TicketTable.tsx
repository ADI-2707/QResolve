import Badge from "../../../../components/common/ui/Badge/Badge";
import Card from "../../../../components/common/ui/Card/Card";

import styles from "./TicketTable.module.css";


const tickets = [

    {
        id:"QRS-1001",
        subject:"Unable to login",
        type:"Technical",
        priority:"High",
        status:"Open"
    },

    {
        id:"QRS-1002",
        subject:"Payment failed",
        type:"Billing",
        priority:"Critical",
        status:"Pending"
    },

    {
        id:"QRS-1003",
        subject:"Refund request",
        type:"Refund",
        priority:"Medium",
        status:"Closed"
    }

];


const TicketTable = () => {


    return (

        <Card title="Tickets">


            <div className={styles.table}>


                <div className={styles.header}>

                    <span>ID</span>

                    <span>Subject</span>

                    <span>Type</span>

                    <span>Priority</span>

                    <span>Status</span>


                </div>



                {
                    tickets.map((ticket)=>(


                        <div
                            key={ticket.id}
                            className={styles.row}
                        >

                            <span>
                                {ticket.id}
                            </span>


                            <span>
                                {ticket.subject}
                            </span>


                            <span>
                                {ticket.type}
                            </span>


                            <Badge
                                variant={
                                    ticket.priority==="Critical"
                                    ? "danger"
                                    :
                                    ticket.priority==="High"
                                    ? "warning"
                                    :
                                    "info"
                                }
                            >

                                {ticket.priority}

                            </Badge>


                            <span>
                                {ticket.status}
                            </span>


                        </div>


                    ))
                }


            </div>


        </Card>

    );

};


export default TicketTable;