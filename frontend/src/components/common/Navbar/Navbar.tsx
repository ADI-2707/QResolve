import styles from "./Navbar.module.css";


const Navbar = () => {
  return (
    <header className={styles.navbar}>

      <h1 className={styles.logo}>
        QResolve
      </h1>


      <div className={styles.actions}>

        <button className={styles.notification}>
          Notifications
        </button>


        <div className={styles.avatar}>
          U
        </div>

      </div>

    </header>
  );
};


export default Navbar;