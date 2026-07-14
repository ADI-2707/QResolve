import Card from "../../../../components/common/ui/Card/Card";

import styles from "./StatsCard.module.css";


interface StatsCardProps {

    title:string;

    value:string | number;

    description?:string;

}


const StatsCard = ({
    title,
    value,
    description
}:StatsCardProps)=>{


    return (

        <Card>

            <div className={styles.container}>

                <p className={styles.title}>
                    {title}
                </p>


                <h2 className={styles.value}>
                    {value}
                </h2>


                {
                    description &&
                    <p className={styles.description}>
                        {description}
                    </p>
                }

            </div>

        </Card>

    );

};


export default StatsCard;