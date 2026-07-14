import { Routes, Route } from "react-router-dom";

import Dashboard from "../pages/Dashboard";
import Tickets from "../pages/Tickets";
import Login from "../pages/Login";


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