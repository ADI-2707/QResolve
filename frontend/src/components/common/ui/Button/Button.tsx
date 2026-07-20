import styles from "./Button.module.css";

interface ButtonProps {
    children: React.ReactNode;
    variant?: "primary" | "secondary" | "danger";
    type?: "button" | "submit" | "reset";
    onClick?: () => void;
    disabled?: boolean;
}


const Button = ({
    children,
    variant = "primary",
    type = "button",
    onClick,
    disabled = false,
}: ButtonProps) => {

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`${styles.button} ${styles[variant]}`}
        >
            {children}
        </button>
    );
};


export default Button;