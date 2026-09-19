import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Loader from "./Loader";

export function ProtectedRoute() {
  const { status } = useAuth();
  if (status === "checking") return <Loader />;
  if (status === "unauthenticated") return <Navigate to="/login" replace />;
  return <Outlet />;
}

export function PublicOnlyRoute() {
  const { status } = useAuth();
  if (status === "checking") return <Loader />;
  if (status === "authenticated") return <Navigate to="/console" replace />;
  return <Outlet />;
}
