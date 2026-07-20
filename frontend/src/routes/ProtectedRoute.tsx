import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../auth/useAuth";

const ProtectedRoute = () => {
    const { session } = useAuth();
    const location = useLocation();
    return session ? <Outlet /> : <Navigate to="/login" replace state={{ from: location.pathname }} />;
};

export default ProtectedRoute;
