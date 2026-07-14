import { Routes, Route } from "react-router-dom";

import Dashboard from "../pages/Dashboard/Dashboard.tsx";
import Tickets from "../pages/Tickets/Tickets.tsx";
import Login from "../pages/Login/Login.tsx";


function AppRoutes() {

    return (

        <Routes>

            <Route
                path="/"
                element={<Dashboard />}
            />

            <Route
                path="/tickets"
                element={<Tickets />}
            />

            <Route
                path="/login"
                element={<Login />}
            />

        </Routes>

    );

}

export default AppRoutes;