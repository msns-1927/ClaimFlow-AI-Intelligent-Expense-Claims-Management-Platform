export type UserRole = "EMPLOYEE" | "MANAGER" | "FINANCE";

export type ClaimStatus =
  | "DRAFT"
  | "SUBMITTED"
  | "APPROVED"
  | "REJECTED"
  | "PAID";

export type DuplicateStatus =
  | "NONE"
  | "POSSIBLE"
  | "LIKELY";

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  department: string | null;
  monthly_limit: number | null;
}

export interface Claim {
  id: number;
  claim_number: string;
  user_id: number;
  merchant: string;
  expense_date: string;
  amount: string;
  currency: string;
  category: string;
  description: string;
  status: ClaimStatus;
  duplicate_status: DuplicateStatus;
  duplicate_of_claim_id: number | null;
  duplicate_score: string | null;
  submitted_at: string | null;
  approved_at: string | null;
  rejected_at: string | null;
  paid_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface CategorySpend {
  category: string;
  amount: string;
}

export interface EmployeeSpend {
  user_id: number;
  employee_name: string;
  monthly_limit: string | null;
  total_spent: string;
  remaining_limit: string | null;
  limit_status: string;
}

export interface FinanceDashboard {
  month: string;
  total_spend: string;
  category_spend: CategorySpend[];
  employee_spend: EmployeeSpend[];
}


export interface ManagerClaim extends Claim {
  employee_name: string;
}