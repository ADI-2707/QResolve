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
                    <span>Category</span>
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
                                {ticket.category.replace("_", " ")}
                            </span>


                            <Badge
                                variant={
                                    ticket.priority === "CRITICAL"
                                    ?
                                    "danger"
                                    :
                                    ticket.priority === "HIGH"
                                    ?
                                    "warning"
                                    :
                                    "info"
                                }
                            >

                                {ticket.priority.toLowerCase()}

                            </Badge>


                            <span>
                                {ticket.status.replace("_", " ").toLowerCase()}
                            </span>


                        </div>


                    ))
                }


            </div>


        </Card>

    );

};


export default TicketTable;
