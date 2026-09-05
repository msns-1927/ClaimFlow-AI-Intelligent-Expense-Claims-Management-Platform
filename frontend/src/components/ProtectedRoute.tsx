import { Navigate, Outlet } from "react-router-dom";

import type { UserRole } from "../types";

interface ProtectedRouteProps {
  allowedRoles?: UserRole[];
}

function ProtectedRoute({
  allowedRoles,
}: ProtectedRouteProps) {
  const token = localStorage.getItem("access_token");
  const storedUser = localStorage.getItem("user");

  if (!token || !storedUser) {
    return <Navigate to="/login" replace />;
  }

  try {
    const user = JSON.parse(storedUser);

    if (
      allowedRoles &&
      !allowedRoles.includes(user.role as UserRole)
    ) {
      if (user.role === "EMPLOYEE") {
        return <Navigate to="/employee" replace />;
      }

      if (user.role === "MANAGER") {
        return <Navigate to="/manager" replace />;
      }

      if (user.role === "FINANCE") {
        return <Navigate to="/finance" replace />;
      }

      return <Navigate to="/login" replace />;
    }

    return <Outlet />;
  } catch {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    return <Navigate to="/login" replace />;
  }
}

export default ProtectedRoute;