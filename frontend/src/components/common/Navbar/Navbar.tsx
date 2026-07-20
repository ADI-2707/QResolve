import styles from "./Navbar.module.css";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../auth/useAuth";


const Navbar = () => {
    const { session, signOut } = useAuth();
    const navigate = useNavigate();

    const logout = () => {
        signOut();
        navigate("/login", { replace: true });
    };

    return (

        <header className={styles.navbar}>


            <h2>
                Support Dashboard
            </h2>


            <div className={styles.profile}>

                <span>{session?.organization_slug} · {session?.role.toLowerCase()}</span>
                <button type="button" onClick={logout}>Sign out</button>

            </div>


        </header>

    );

};


export default Navbar;
