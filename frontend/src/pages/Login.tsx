import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import type { User } from "../types";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      // Step 1: Login and receive JWT
      const loginResponse = await api.post("/auth/login", {
        email,
        password,
      });

      const token = loginResponse.data.access_token;

      localStorage.setItem("access_token", token);

      // Step 2: Get the logged-in user's role
      const userResponse = await api.get<User>("/auth/me");

      const user = userResponse.data;

      localStorage.setItem("user", JSON.stringify(user));

      // Step 3: Send user to the correct dashboard
      if (user.role === "EMPLOYEE") {
        navigate("/employee");
      } else if (user.role === "MANAGER") {
        navigate("/manager");
      } else if (user.role === "FINANCE") {
        navigate("/finance");
      } else {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        setError("Your account does not have a valid application role.");
        }
    } catch (error: any) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");

      if (error.response?.status === 401) {
        setError("Invalid email or password.");
      } else {
        setError(
          "Unable to connect to the server. Please make sure the backend is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <div className="brand-mark">EC</div>

          <h1>Expense Claims</h1>

          <p>
            Submit, review and manage employee expenses.
          </p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email</label>

            <input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>

            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <div className="demo-accounts">
          <p>Demo accounts</p>

          <span>Employee</span>
          <small>arjun.kumar@example.com</small>

          <span>Manager</span>
          <small>rahul.mehta@example.com</small>

          <span>Finance</span>
          <small>rohit.verma@example.com</small>
        </div>
      </div>
    </div>
  );
}

export default Login;