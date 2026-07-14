import Button from "../../../../components/common/ui/Button/Button";
import Input from "../../../../components/common/ui/Input/Input";
import styles from "./TicketFilters.module.css";


const TicketFilters = () => {


    return (

        <div className={styles.filters}>


            <Input
                placeholder="Search tickets..."
            />


            <select className={styles.select}>

                <option>
                    All Priorities
                </option>

                <option>
                    Critical
                </option>

                <option>
                    High
                </option>

                <option>
                    Medium
                </option>

                <option>
                    Low
                </option>

            </select>


            <select className={styles.select}>

                <option>
                    All Status
                </option>

                <option>
                    Open
                </option>

                <option>
                    Pending
                </option>

                <option>
                    Closed
                </option>

            </select>


            <Button>
                Filter
            </Button>


        </div>

    );

};


export default TicketFilters;