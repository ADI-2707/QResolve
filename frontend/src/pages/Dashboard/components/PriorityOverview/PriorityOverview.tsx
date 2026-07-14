import Badge from "../../../../components/common/ui/Badge/Badge";
import Card from "../../../../components/common/ui/Card/Card";

import styles from "./PriorityOverview.module.css";


const priorities = [

    {
        name:"Critical",
        count:12,
        type:"danger"
    },

    {
        name:"High",
        count:34,
        type:"warning"
    },

    {
        name:"Medium",
        count:56,
        type:"info"
    },

    {
        name:"Low",
        count:78,
        type:"success"
    }

];


const PriorityOverview = ()=>{


    return (

        <Card title="Priority Overview">


            <div className={styles.grid}>


                {
                    priorities.map((priority)=>(


                        <div
                            key={priority.name}
                            className={styles.item}
                        >

                            <Badge variant={priority.type as any}>
                                {priority.name}
                            </Badge>


                            <span>
                                {priority.count}
                            </span>


                        </div>


                    ))
                }


            </div>


        </Card>

    );

};


export default PriorityOverview;