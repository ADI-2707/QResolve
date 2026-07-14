import styles from "./Input.module.css";


interface InputProps {

    placeholder?: string;

    value?: string;

    onChange?:
    (event:React.ChangeEvent<HTMLInputElement>)=>void;

    type?:string;

}


const Input = ({
    placeholder,
    value,
    onChange,
    type="text"

}:InputProps)=>{


    return (

        <input

            className={styles.input}

            type={type}

            placeholder={placeholder}

            value={value}

            onChange={onChange}

        />

    );

};


export default Input;