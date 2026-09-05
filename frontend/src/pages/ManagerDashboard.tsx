import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import type { Claim, ManagerClaim, User } from "../types";

function ManagerDashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [claims, setClaims] = useState<ManagerClaim[]>([]);

  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const [selectedClaim, setSelectedClaim] = useState<Claim | null>(null);
  const [comment, setComment] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const [userResponse, claimsResponse] = await Promise.all([
        api.get<User>("/auth/me"),
        api.get<ManagerClaim[]>("/claims/team"),
      ]);

      setUser(userResponse.data);
      setClaims(claimsResponse.data);
    } catch (err: any) {
      if (err.response?.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        navigate("/login");
        return;
      }

      setError(
        err.response?.data?.detail ||
          "Unable to load your team's claims."
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

  const openReview = (claim: Claim) => {
    setSelectedClaim(claim);
    setComment("");
    setError("");
    setMessage("");
  };

  const closeReview = () => {
    setSelectedClaim(null);
    setComment("");
  };

  const reviewClaim = async (
    action: "approve" | "reject"
  ) => {
    if (!selectedClaim) {
      return;
    }

    if (
      action === "reject" &&
      !comment.trim()
    ) {
      setError("Please provide a reason for rejecting the claim.");
      return;
    }

    setActionLoading(selectedClaim.id);
    setError("");
    setMessage("");

    try {
      const response = await api.post<Claim>(
        `/claims/${selectedClaim.id}/${action}`,
        {
          comment: comment.trim() || null,
        }
      );

      setMessage(
        `${response.data.claim_number} has been ${action === "approve" ? "approved" : "rejected"}.`
      );

      closeReview();
      await loadDashboard();
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          `Unable to ${action} the claim.`
      );
    } finally {
      setActionLoading(null);
    }
  };

  const formatCurrency = (amount: string | number) => {
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

  const totalPending = claims.reduce(
    (sum, claim) => sum + Number(claim.amount),
    0
  );

  return (
    <div className="dashboard-page">
      <header className="topbar">
        <div className="topbar-brand">
          <div className="brand-mark small">EC</div>

          <div>
            <strong>Expense Claims</strong>
            <span>Manager Portal</span>
          </div>
        </div>

        <div className="topbar-user">
          <div className="user-info">
            <strong>{user?.name || "Manager"}</strong>
            <span>{user?.department || "Manager"}</span>
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
          <p className="eyebrow">TEAM REVIEW</p>

          <h1>
            Welcome back
            {user ? `, ${user.name.split(" ")[0]}` : ""}
          </h1>

          <p>
            Review expense claims submitted by your team.
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
            <span>Claims awaiting review</span>
            <strong>{claims.length}</strong>
            <small>Submitted by your team</small>
          </div>

          <div className="stat-card">
            <span>Pending amount</span>
            <strong>
              {formatCurrency(totalPending)}
            </strong>
            <small>Total awaiting your decision</small>
          </div>

          <div className="stat-card">
            <span>Department</span>
            <strong>
              {user?.department || "—"}
            </strong>
            <small>Your team</small>
          </div>

          <div className="stat-card">
            <span>Role</span>
            <strong>Manager</strong>
            <small>Team claim reviewer</small>
          </div>
        </section>

        <section className="claims-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">REVIEW QUEUE</p>
              <h2>Claims awaiting approval</h2>
              <p>
                You can only review claims submitted by your
                direct team members.
              </p>
            </div>
          </div>

          {loading ? (
            <div className="empty-state">
              <h3>Loading claims...</h3>
            </div>
          ) : claims.length === 0 ? (
            <div className="empty-state">
              <h3>No claims awaiting review</h3>
              <p>
                Your team's submitted claims will appear here.
              </p>
            </div>
          ) : (
            <div className="claims-table-wrapper">
              <table className="claims-table">
                <thead>
                  <tr>
                    <th>Claim</th>
                    <th>Employee</th>
                    <th>Merchant</th>
                    <th>Date</th>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Duplicate</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  {claims.map((claim) => (
                    <tr key={claim.id}>
                      <td>
                        <strong>
                          {claim.claim_number}
                        </strong>
                      </td>

                      <td>
                        <strong>{claim.employee_name}</strong>
                      </td>

                      <td>{claim.merchant}</td>

                      <td>
                        {claim.expense_date.slice(0, 10)}
                      </td>

                      <td>
                        {formatCategory(claim.category)}
                      </td>

                      <td>
                        <strong>
                          {formatCurrency(claim.amount)}
                        </strong>
                      </td>

                      <td>
                        {claim.duplicate_status === "NONE" ? (
                          <span className="status-badge status-paid">
                            Clear
                          </span>
                        ) : (
                          <span className="status-badge status-rejected">
                            {claim.duplicate_status}
                          </span>
                        )}
                      </td>

                      <td>
                        <button
                          className="primary-button table-review-button"
                          onClick={() => openReview(claim)}
                        >
                          Review
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {selectedClaim && (
          <div className="modal-backdrop">
            <div className="review-modal">
              <div className="modal-header">
                <div>
                  <p className="eyebrow">CLAIM REVIEW</p>

                  <h2>
                    {selectedClaim.claim_number}
                  </h2>
                </div>

                <button
                  className="modal-close"
                  onClick={closeReview}
                >
                  ×
                </button>
              </div>

              <div className="claim-detail-grid">
                <div>
                  <span>Merchant</span>
                  <strong>
                    {selectedClaim.merchant}
                  </strong>
                </div>

                <div>
                  <span>Amount</span>
                  <strong>
                    {formatCurrency(
                      selectedClaim.amount
                    )}
                  </strong>
                </div>

                <div>
                  <span>Date</span>
                  <strong>
                    {selectedClaim.expense_date.slice(0, 10)}
                  </strong>
                </div>

                <div>
                  <span>Category</span>
                  <strong>
                    {formatCategory(
                      selectedClaim.category
                    )}
                  </strong>
                </div>
              </div>

              <div className="claim-description">
                <span>Description</span>
                <p>{selectedClaim.description}</p>
              </div>

              {selectedClaim.duplicate_status !== "NONE" && (
                <div className="duplicate-warning">
                  <strong>
                    ⚠ Duplicate warning
                  </strong>

                  <p>
                    This claim has been flagged as{" "}
                    {selectedClaim.duplicate_status.toLowerCase()}.
                  </p>

                  {selectedClaim.duplicate_of_claim_id && (
                    <small>
                      Similar to claim #
                      {selectedClaim.duplicate_of_claim_id}
                      {selectedClaim.duplicate_score
                        ? ` · ${selectedClaim.duplicate_score}% similarity`
                        : ""}
                    </small>
                  )}
                </div>
              )}

              <div className="form-group">
                <label>
                  Review comment
                </label>

                <textarea
                  className="description-input"
                  placeholder="Add a comment. A rejection requires a reason."
                  value={comment}
                  onChange={(event) =>
                    setComment(event.target.value)
                  }
                />
              </div>

              <div className="review-actions">
                <button
                  className="secondary-button"
                  onClick={closeReview}
                  disabled={actionLoading !== null}
                >
                  Cancel
                </button>

                <button
                  className="reject-button"
                  onClick={() =>
                    reviewClaim("reject")
                  }
                  disabled={actionLoading !== null}
                >
                  {actionLoading === selectedClaim.id
                    ? "Processing..."
                    : "Reject"}
                </button>

                <button
                  className="primary-button"
                  onClick={() =>
                    reviewClaim("approve")
                  }
                  disabled={actionLoading !== null}
                >
                  {actionLoading === selectedClaim.id
                    ? "Processing..."
                    : "Approve"}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default ManagerDashboard;