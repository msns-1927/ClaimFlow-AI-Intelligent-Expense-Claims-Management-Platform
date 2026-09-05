import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import type {
  Claim,
  FinanceDashboard as FinanceDashboardData,
  User,
} from "../types";

function FinanceDashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [dashboard, setDashboard] =
    useState<FinanceDashboardData | null>(null);
  const [pendingClaims, setPendingClaims] =
    useState<Claim[]>([]);

  const [loading, setLoading] = useState(true);
  const [payingClaim, setPayingClaim] =
    useState<number | null>(null);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const [
        userResponse,
        dashboardResponse,
        pendingResponse,
      ] = await Promise.all([
        api.get<User>("/auth/me"),
        api.get<FinanceDashboardData>(
          "/claims/finance/dashboard"
        ),
        api.get<Claim[]>("/claims/finance/pending"),
      ]);

      setUser(userResponse.data);
      setDashboard(dashboardResponse.data);
      setPendingClaims(pendingResponse.data);
    } catch (err: any) {
      if (err.response?.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        navigate("/login");
        return;
      }

      setError(
        err.response?.data?.detail ||
          "Unable to load the Finance dashboard."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  const payClaim = async (claim: Claim) => {
    setPayingClaim(claim.id);
    setError("");
    setMessage("");

    try {
      const response = await api.post<Claim>(
        `/claims/${claim.id}/pay`
      );

      setMessage(
        `${response.data.claim_number} has been marked as paid.`
      );

      await loadDashboard();
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Unable to process the payment."
      );
    } finally {
      setPayingClaim(null);
    }
  };

  const formatCurrency = (
    amount: string | number
  ) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    }).format(Number(amount));
  };

  const formatCategory = (category: string) => {
    return category
      .split("_")
      .map(
        (word) =>
          word.charAt(0) +
          word.slice(1).toLowerCase()
      )
      .join(" ");
  };

  const getLimitClass = (status: string) => {
    if (status === "EXCEEDED") {
      return "limit-exceeded";
    }

    if (status === "NEAR_LIMIT") {
      return "limit-near";
    }

    return "limit-within";
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="loading-screen">
          Loading Finance dashboard...
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <header className="topbar">
        <div className="topbar-brand">
          <div className="brand-mark small">
            EC
          </div>

          <div>
            <strong>Expense Claims</strong>
            <span>Finance Portal</span>
          </div>
        </div>

        <div className="topbar-user">
          <div className="user-info">
            <strong>
              {user?.name || "Finance"}
            </strong>

            <span>
              {user?.department || "Finance"}
            </span>
          </div>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-container">
        <section className="welcome-section">
          <p className="eyebrow">
            FINANCE OVERVIEW
          </p>

          <h1>
            Monthly expenses
          </h1>

          <p>
            Monitor company spending, employee limits,
            and reimbursement payments.
          </p>
        </section>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {message && (
          <div className="alert alert-success">
            {message}
          </div>
        )}

        <section className="stats-grid">
          <div className="stat-card">
            <span>
              {dashboard?.month || "Current month"} spend
            </span>

            <strong>
              {formatCurrency(
                dashboard?.total_spend || 0
              )}
            </strong>

            <small>
              Actual paid expenses
            </small>
          </div>

          <div className="stat-card">
            <span>
              Awaiting payment
            </span>

            <strong>
              {pendingClaims.length}
            </strong>

            <small>
              Approved claims
            </small>
          </div>

          <div className="stat-card">
            <span>
              Payment value
            </span>

            <strong>
              {formatCurrency(
                pendingClaims.reduce(
                  (sum, claim) =>
                    sum + Number(claim.amount),
                  0
                )
              )}
            </strong>

            <small>
              Ready for reimbursement
            </small>
          </div>

          <div className="stat-card">
            <span>
              Limit alerts
            </span>

            <strong>
              {dashboard?.employee_spend.filter(
                (employee) =>
                  employee.limit_status ===
                    "NEAR_LIMIT" ||
                  employee.limit_status ===
                    "EXCEEDED"
              ).length || 0}
            </strong>

            <small>
              Near or over monthly limit
            </small>
          </div>
        </section>

        <section className="finance-grid">
          <div className="claims-section">
            <div className="section-heading">
              <div>
                <p className="eyebrow">
                  SPENDING
                </p>

                <h2>
                  Spend by category
                </h2>
              </div>
            </div>

            {dashboard?.category_spend.length === 0 ? (
              <div className="empty-state">
                <p>
                  No paid expenses this month.
                </p>
              </div>
            ) : (
              <div className="category-list">
                {dashboard?.category_spend.map(
                  (item) => {
                    const percentage =
                      dashboard.total_spend === "0"
                        ? 0
                        : (Number(item.amount) /
                            Number(
                              dashboard.total_spend
                            )) *
                          100;

                    return (
                      <div
                        className="category-row"
                        key={item.category}
                      >
                        <div className="category-info">
                          <strong>
                            {formatCategory(
                              item.category
                            )}
                          </strong>

                          <span>
                            {formatCurrency(
                              item.amount
                            )}
                          </span>
                        </div>

                        <div className="progress-track">
                          <div
                            className="progress-bar"
                            style={{
                              width: `${Math.min(
                                percentage,
                                100
                              )}%`,
                            }}
                          />
                        </div>
                      </div>
                    );
                  }
                )}
              </div>
            )}
          </div>

          <div className="claims-section">
            <div className="section-heading">
              <div>
                <p className="eyebrow">
                  PAYOUT QUEUE
                </p>

                <h2>
                  Approved claims
                </h2>
              </div>
            </div>

            {pendingClaims.length === 0 ? (
              <div className="empty-state">
                <h3>
                  Nothing to pay
                </h3>

                <p>
                  Approved claims will appear here.
                </p>
              </div>
            ) : (
              <div className="payment-list">
                {pendingClaims.map(
                  (claim) => (
                    <div
                      className="payment-row"
                      key={claim.id}
                    >
                      <div>
                        <strong>
                          {claim.claim_number}
                        </strong>

                        <span>
                          {claim.merchant}
                        </span>
                      </div>

                      <div className="payment-amount">
                        <strong>
                          {formatCurrency(
                            claim.amount
                          )}
                        </strong>

                        <button
                          className="primary-button"
                          disabled={
                            payingClaim ===
                            claim.id
                          }
                          onClick={() =>
                            payClaim(claim)
                          }
                        >
                          {payingClaim ===
                          claim.id
                            ? "Paying..."
                            : "Mark Paid"}
                        </button>
                      </div>
                    </div>
                  )
                )}
              </div>
            )}
          </div>
        </section>

        <section className="claims-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">
                MONTHLY CONTROL
              </p>

              <h2>
                Employee spending
              </h2>

              <p>
                Track actual paid spending against
                each employee's monthly limit.
              </p>
            </div>
          </div>

          <div className="claims-table-wrapper">
            <table className="claims-table">
              <thead>
                <tr>
                  <th>
                    Employee
                  </th>

                  <th>
                    Monthly limit
                  </th>

                  <th>
                    Spent
                  </th>

                  <th>
                    Remaining
                  </th>

                  <th>
                    Status
                  </th>
                </tr>
              </thead>

              <tbody>
                {dashboard?.employee_spend.map(
                  (employee) => (
                    <tr key={employee.user_id}>
                      <td>
                        <strong>
                          {employee.employee_name}
                        </strong>
                      </td>

                      <td>
                        {employee.monthly_limit
                          ? formatCurrency(
                              employee.monthly_limit
                            )
                          : "—"}
                      </td>

                      <td>
                        <strong>
                          {formatCurrency(
                            employee.total_spent
                          )}
                        </strong>
                      </td>

                      <td>
                        {employee.remaining_limit
                          ? formatCurrency(
                              employee.remaining_limit
                            )
                          : "—"}
                      </td>

                      <td>
                        <span
                          className={`limit-badge ${getLimitClass(
                            employee.limit_status
                          )}`}
                        >
                          {employee.limit_status
                            .replace("_", " ")}
                        </span>
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default FinanceDashboard;