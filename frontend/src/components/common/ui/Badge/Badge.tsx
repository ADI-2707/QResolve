import styles from "./Badge.module.css";


interface BadgeProps {

    children:React.ReactNode;

    variant?:
    "success" |
    "warning" |
    "danger" |
    "info";

}


const Badge = ({
    children,
    variant="info"
}:BadgeProps)=>{


    return (

        <span
            className={`${styles.badge} ${styles[variant]}`}
        >
            {children}
        </span>

    );

};


export default Badge;