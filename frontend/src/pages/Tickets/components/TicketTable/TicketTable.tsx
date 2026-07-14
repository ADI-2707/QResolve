import Badge from "../../../../components/common/ui/Badge/Badge";
import Card from "../../../../components/common/ui/Card/Card";

import useTickets from "../../../../hooks/useTickets";

import styles from "./TicketTable.module.css";


const TicketTable = () => {


    const {
        tickets,
        loading,
        error
    } = useTickets();



    if(loading){

        return (

            <Card title="Tickets">

                Loading tickets...

            </Card>

        );

    }



    if(error){

        return (

            <Card title="Tickets">

                {error}

            </Card>

        );

    }



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
                                    ticket.priority === "Critical"
                                    ?
                                    "danger"
                                    :
                                    ticket.priority === "High"
                                    ?
                                    "warning"
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