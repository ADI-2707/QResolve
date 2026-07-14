import styles from "./Navbar.module.css";


const Navbar = () => {


    return (

        <header className={styles.navbar}>


            <h2>
                Support Dashboard
            </h2>


            <div className={styles.profile}>

                Admin

            </div>


        </header>

    );

};


export default Navbar;