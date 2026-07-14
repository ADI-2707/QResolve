import styles from "./Button.module.css";

interface ButtonProps {
    children: React.ReactNode;
    variant?: "primary" | "secondary" | "danger";
    type?: "button" | "submit" | "reset";
    onClick?: () => void;
}


const Button = ({
    children,
    variant = "primary",
    type = "button",
    onClick
}: ButtonProps) => {

    return (
        <button
            type={type}
            onClick={onClick}
            className={`${styles.button} ${styles[variant]}`}
        >
            {children}
        </button>
    );
};


export default Button;