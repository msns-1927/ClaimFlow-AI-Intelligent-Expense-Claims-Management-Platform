import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import type { Claim, User } from "../types";

const categories = [
  { value: "TRAVEL", label: "Travel" },
  { value: "MEALS", label: "Meals" },
  { value: "ACCOMMODATION", label: "Accommodation" },
  { value: "OFFICE_SUPPLIES", label: "Office Supplies" },
  { value: "TAXI_LOCAL_TRANSPORT", label: "Taxi / Local Transport" },
  { value: "CLIENT_EXPENSE", label: "Client Expense" },
  { value: "OTHER", label: "Other" },
];

function EmployeeDashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [claims, setClaims] = useState<Claim[]>([]);

  const [receiptText, setReceiptText] = useState("");
  const [loadingExtraction, setLoadingExtraction] = useState(false);
  const [saving, setSaving] = useState(false);

  const [editingClaim, setEditingClaim] = useState<Claim | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const [userResponse, claimsResponse] = await Promise.all([
        api.get<User>("/auth/me"),
        api.get<Claim[]>("/claims/my"),
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

      setError("Unable to load your claims.");
    }
  };

  const draftCount = useMemo(
    () => claims.filter((claim) => claim.status === "DRAFT").length,
    [claims]
  );

  const pendingCount = useMemo(
    () =>
      claims.filter(
        (claim) =>
          claim.status === "SUBMITTED" ||
          claim.status === "APPROVED"
      ).length,
    [claims]
  );

  const paidCount = useMemo(
    () => claims.filter((claim) => claim.status === "PAID").length,
    [claims]
  );

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  const extractReceipt = async () => {
    if (!receiptText.trim()) {
      setError("Please paste your receipt text first.");
      return;
    }

    setError("");
    setMessage("");
    setLoadingExtraction(true);

    try {
      const response = await api.post<Claim>(
        "/claims/from-receipt",
        {
          raw_text: receiptText,
        }
      );

      setEditingClaim(response.data);
      setMessage(
        "Receipt processed. Please review the extracted information before submitting."
      );

      setReceiptText("");
      await loadDashboard();
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Unable to process the receipt."
      );
    } finally {
      setLoadingExtraction(false);
    }
  };

  const updateEditingClaim = (
    field: keyof Claim,
    value: string
  ) => {
    if (!editingClaim) {
      return;
    }

    setEditingClaim({
      ...editingClaim,
      [field]: value,
    });
  };

  const saveDraft = async (event?: FormEvent) => {
    event?.preventDefault();

    if (!editingClaim) {
      return;
    }

    setError("");
    setMessage("");
    setSaving(true);

    try {
      const response = await api.put<Claim>(
        `/claims/${editingClaim.id}`,
        {
          merchant: editingClaim.merchant,
          expense_date: `${editingClaim.expense_date.slice(
            0,
            10
          )}T00:00:00`,
          amount: Number(editingClaim.amount),
          currency: editingClaim.currency,
          category: editingClaim.category,
          description: editingClaim.description,
        }
      );

      setEditingClaim(response.data);

      await loadDashboard();

      setMessage("Draft saved successfully.");
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Unable to save the claim."
      );
    } finally {
      setSaving(false);
    }
  };

  const submitClaim = async () => {
    if (!editingClaim) {
      return;
    }

    setError("");
    setMessage("");
    setSaving(true);

    try {
      // Save the latest edits before submitting.
      await api.put(
        `/claims/${editingClaim.id}`,
        {
          merchant: editingClaim.merchant,
          expense_date: `${editingClaim.expense_date.slice(
            0,
            10
          )}T00:00:00`,
          amount: Number(editingClaim.amount),
          currency: editingClaim.currency,
          category: editingClaim.category,
          description: editingClaim.description,
        }
      );

      const response = await api.post<Claim>(
        `/claims/${editingClaim.id}/submit`
      );

      setEditingClaim(null);
      await loadDashboard();

      setMessage(
        `${response.data.claim_number} submitted successfully.`
      );
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Unable to submit the claim."
      );
    } finally {
      setSaving(false);
    }
  };

  const editExistingDraft = (claim: Claim) => {
    if (claim.status !== "DRAFT") {
      return;
    }

    setEditingClaim(claim);
    setError("");
    setMessage("");
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
          word.charAt(0) + word.slice(1).toLowerCase()
      )
      .join(" ");
  };

  const formatStatus = (status: string) => {
    return status.charAt(0) + status.slice(1).toLowerCase();
  };

  return (
    <div className="dashboard-page">
      <header className="topbar">
        <div className="topbar-brand">
          <div className="brand-mark small">EC</div>

          <div>
            <strong>Expense Claims</strong>
            <span>Employee Portal</span>
          </div>
        </div>

        <div className="topbar-user">
          <div className="user-info">
            <strong>{user?.name || "Employee"}</strong>
            <span>{user?.department || "Employee"}</span>
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
          <div>
            <p className="eyebrow">MY EXPENSES</p>

            <h1>
              Welcome back{user ? `, ${user.name.split(" ")[0]}` : ""}
            </h1>

            <p>
              Create expense claims from your receipts and track
              reimbursement status.
            </p>
          </div>
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
            <span>Drafts</span>
            <strong>{draftCount}</strong>
            <small>Claims being prepared</small>
          </div>

          <div className="stat-card">
            <span>Pending</span>
            <strong>{pendingCount}</strong>
            <small>Under review or approved</small>
          </div>

          <div className="stat-card">
            <span>Paid</span>
            <strong>{paidCount}</strong>
            <small>Completed claims</small>
          </div>

          <div className="stat-card">
            <span>Monthly limit</span>
            <strong>
              {user?.monthly_limit != null
                ? formatCurrency(user.monthly_limit)
                : "—"}
            </strong>
            <small>Your configured limit</small>
          </div>
        </section>

        <section className="claim-creation-card">
          <div className="section-heading">
            <div>
              <p className="eyebrow">NEW CLAIM</p>
              <h2>Create from receipt</h2>
              <p>
                Paste whatever is written on your receipt. The system
                will extract the expense details for you.
              </p>
            </div>
          </div>

          <textarea
            className="receipt-input"
            placeholder={`Example:

swiggy
order 45821
05/09/26
food delivery
total rs 850`}
            value={receiptText}
            onChange={(event) =>
              setReceiptText(event.target.value)
            }
          />

          <div className="receipt-actions">
            <span>
              You don't need to enter six separate fields.
            </span>

            <button
              className="primary-button"
              onClick={extractReceipt}
              disabled={loadingExtraction}
            >
              {loadingExtraction
                ? "Extracting..."
                : "✨ Extract from Receipt"}
            </button>
          </div>
        </section>

        {editingClaim && (
          <section className="claim-creation-card review-card">
            <div className="section-heading">
              <div>
                <p className="eyebrow">REVIEW</p>
                <h2>Review extracted expense</h2>
                <p>
                  Check the information carefully. You can correct
                  anything before submitting.
                </p>
              </div>

              <span className="draft-badge">Draft</span>
            </div>

            {editingClaim.duplicate_status !== "NONE" && (
              <div className="duplicate-warning">
                <strong>⚠ Possible duplicate detected</strong>

                <p>
                  This receipt looks similar to an existing claim.
                  Review the duplicate information before submitting.
                </p>

                {editingClaim.duplicate_of_claim_id && (
                  <small>
                    Similar claim ID:{" "}
                    {editingClaim.duplicate_of_claim_id}
                    {editingClaim.duplicate_score
                      ? ` · Similarity ${editingClaim.duplicate_score}%`
                      : ""}
                  </small>
                )}
              </div>
            )}

            <form onSubmit={saveDraft}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Merchant</label>

                  <input
                    value={editingClaim.merchant}
                    onChange={(event) =>
                      updateEditingClaim(
                        "merchant",
                        event.target.value
                      )
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Expense date</label>

                  <input
                    type="date"
                    value={editingClaim.expense_date.slice(0, 10)}
                    onChange={(event) =>
                      updateEditingClaim(
                        "expense_date",
                        event.target.value
                      )
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Amount</label>

                  <input
                    type="number"
                    min="0.01"
                    step="0.01"
                    value={editingClaim.amount}
                    onChange={(event) =>
                      updateEditingClaim(
                        "amount",
                        event.target.value
                      )
                    }
                  />
                </div>

                <div className="form-group">
                  <label>Currency</label>

                  <input
                    value={editingClaim.currency}
                    onChange={(event) =>
                      updateEditingClaim(
                        "currency",
                        event.target.value.toUpperCase()
                      )
                    }
                    maxLength={3}
                  />
                </div>

                <div className="form-group">
                  <label>Category</label>

                  <select
                    value={editingClaim.category}
                    onChange={(event) =>
                      updateEditingClaim(
                        "category",
                        event.target.value
                      )
                    }
                  >
                    {categories.map((category) => (
                      <option
                        key={category.value}
                        value={category.value}
                      >
                        {category.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group full-width">
                  <label>Description</label>

                  <textarea
                    className="description-input"
                    value={editingClaim.description}
                    onChange={(event) =>
                      updateEditingClaim(
                        "description",
                        event.target.value
                      )
                    }
                  />
                </div>
              </div>

              <div className="review-actions">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setEditingClaim(null)}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="secondary-button"
                  disabled={saving}
                >
                  Save Draft
                </button>

                <button
                  type="button"
                  className="primary-button"
                  disabled={saving}
                  onClick={submitClaim}
                >
                  Submit Claim
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="claims-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">HISTORY</p>
              <h2>Your claims</h2>
            </div>
          </div>

          {claims.length === 0 ? (
            <div className="empty-state">
              <h3>No claims yet</h3>
              <p>
                Create your first claim by pasting your receipt above.
              </p>
            </div>
          ) : (
            <div className="claims-table-wrapper">
              <table className="claims-table">
                <thead>
                  <tr>
                    <th>Claim</th>
                    <th>Merchant</th>
                    <th>Date</th>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th></th>
                  </tr>
                </thead>

                <tbody>
                  {claims.map((claim) => (
                    <tr key={claim.id}>
                      <td>
                        <strong>{claim.claim_number}</strong>
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
                        <span
                          className={`status-badge status-${claim.status.toLowerCase()}`}
                        >
                          {formatStatus(claim.status)}
                        </span>
                      </td>

                      <td>
                        {claim.status === "DRAFT" && (
                          <button
                            className="table-action"
                            onClick={() =>
                              editExistingDraft(claim)
                            }
                          >
                            Edit
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default EmployeeDashboard;