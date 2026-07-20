import { NavLink } from "react-router-dom";

import styles from "./Sidebar.module.css";


const Sidebar = () => {


    const links = [

        {
            label:"Dashboard",
            path:"/"
        },

        {
            label:"Tickets",
            path:"/tickets"
        },

        {
            label:"Members",
            path:"/members"
        },

        {
            label:"Audit Logs",
            path:"/audit"
        }

    ];


    return (

        <aside className={styles.sidebar}>


            <div className={styles.logo}>
                QResolve
            </div>


            <nav className={styles.navigation}>

                {
                    links.map((link)=>(

                        <NavLink
                            key={link.path}
                            to={link.path}
                            className={({isActive}) =>
                                isActive
                                ? styles.active
                                : styles.link
                            }
                        >

                            {link.label}

                        </NavLink>

                    ))
                }


            </nav>


        </aside>

    );

};


export default Sidebar;