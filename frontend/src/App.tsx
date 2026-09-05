import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import EmployeeDashboard from "./pages/EmployeeDashboard";
import ManagerDashboard from "./pages/ManagerDashboard";
import FinanceDashboard from "./pages/FinanceDashboard";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public route */}
        <Route
          path="/login"
          element={<Login />}
        />

        {/* Employee routes */}
        <Route
          element={
            <ProtectedRoute
              allowedRoles={["EMPLOYEE"]}
            />
          }
        >
          <Route
            path="/employee"
            element={<EmployeeDashboard />}
          />
        </Route>

        {/* Manager routes */}
        <Route
          element={
            <ProtectedRoute
              allowedRoles={["MANAGER"]}
            />
          }
        >
          <Route
            path="/manager"
            element={<ManagerDashboard />}
          />
        </Route>

        {/* Finance routes */}
        <Route
          element={
            <ProtectedRoute
              allowedRoles={["FINANCE"]}
            />
          }
        >
          <Route
            path="/finance"
            element={<FinanceDashboard />}
          />
        </Route>

        {/* Unknown routes */}
        <Route
          path="*"
          element={
            <Navigate
              to="/login"
              replace
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;