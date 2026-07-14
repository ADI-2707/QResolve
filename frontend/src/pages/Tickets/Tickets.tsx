import TicketFilters from "./components/TicketFilters/TicketFilters";
import TicketTable from "./components/TicketTable/TicketTable";

import styles from "./Tickets.module.css";


const Tickets = () => {


    return (

        <div className={styles.page}>


            <header className={styles.header}>

                <h1>
                    Tickets
                </h1>

                <p>
                    Manage and analyze customer support tickets
                </p>

            </header>



            <TicketFilters />


            <TicketTable />


        </div>

    );

};


export default Tickets;