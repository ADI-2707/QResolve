import { Routes, Route } from "react-router-dom";


import MainLayout from "../layouts/MainLayout/MainLayout";


import Dashboard from "../pages/Dashboard/Dashboard";
import Tickets from "../pages/Tickets/Tickets";
import Login from "../pages/Login/Login";
import Members from "../pages/Members/Members";
import AuditLogs from "../pages/AuditLogs/AuditLogs";
import ProtectedRoute from "./ProtectedRoute";


function AppRoutes() {


    return (

        <Routes>


            <Route
                path="/login"
                element={<Login />}
            />


            <Route element={<ProtectedRoute />}>
                <Route path="/" element={<MainLayout />}>

                <Route
                    index
                    element={<Dashboard />}
                />


                <Route
                    path="tickets"
                    element={<Tickets />}
                />

                <Route
                    path="members"
                    element={<Members />}
                />

                <Route
                    path="audit"
                    element={<AuditLogs />}
                />

                </Route>
            </Route>


        </Routes>

    );

}


export default AppRoutes;
