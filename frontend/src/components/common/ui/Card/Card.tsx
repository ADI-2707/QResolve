import styles from "./Card.module.css";


interface CardProps {

    children: React.ReactNode;

    title?: string;

}


const Card = ({
    children,
    title
}:CardProps)=>{


    return (

        <section className={styles.card}>

            {
                title &&
                <h3 className={styles.title}>
                    {title}
                </h3>
            }


            <div>
                {children}
            </div>


        </section>

    );

};


export default Card;