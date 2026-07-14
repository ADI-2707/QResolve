import { Outlet } from "react-router-dom";

import Sidebar from "../../components/common/Sidebar/Sidebar";
import Navbar from "../../components/common/Navbar/Navbar";

import styles from "./MainLayout.module.css";


const MainLayout = () => {

    return (

        <div className={styles.layout}>

            <Sidebar />


            <div className={styles.content}>

                <Navbar />


                <main className={styles.main}>

                    <Outlet />

                </main>


            </div>


        </div>

    );

};


export default MainLayout;