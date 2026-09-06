## 🚀 Overview:

> **ClaimFlow AI** is an AI-powered expense claims management platform that turns messy receipt text into structured expense claims and manages the complete reimbursement workflow — from employee submission to manager approval and Finance payment.

### 💡 The Problem:

Expense reimbursement is often unnecessarily manual. Employees have to enter multiple fields from receipts, managers need to review claims, and Finance needs to prevent duplicate payments while keeping track of monthly spending.

**ClaimFlow AI brings the entire process into one streamlined workflow.**

### ✨ What ClaimFlow AI Does:

| 👤 Employee | 👨‍💼 Manager | 💰 Finance |
|---|---|---|
| Paste receipt text | Review team claims | Process approved claims |
| AI creates a claim | Approve or reject | Mark claims as paid |
| Review & correct details | Add review comments | Track monthly spending |
| Submit expenses | Cannot approve own claim | Monitor spending limits |
| Track claim status | View team claims | Analyze spending by category |

### 🤖 AI-Powered Receipt Processing:

Instead of manually entering expense details, employees can simply paste whatever is written on a receipt.

```text
Raw Receipt Text
       ↓
   🤖 AI Extraction
       ↓
   Structured Claim
       ↓
 ✏️ Review & Correct
       ↓
 🔍 Duplicate Check
       ↓
     Submit
```

## ✨ Key Features:

### 🤖 AI-Powered Receipt-to-Claim:

- Paste raw receipt text instead of manually filling multiple fields.
- Uses **Groq + GPT-OSS-120B** to extract structured expense information.
- Extracts merchant, date, amount, currency, category, and description.
- Generates a confidence score for the extraction.
- Creates the result as a **Draft Claim** for employee verification.

### ✏️ Review & Correction:

- Employees can review AI-generated claim details before submission.
- All extracted fields can be corrected when necessary.
- Claims remain editable while they are in **Draft** status.

### 🔍 Intelligent Duplicate Detection:

- Detects exact duplicate receipts using normalized text and hashing.
- Detects similar receipts even when the receipt is typed differently.
- Compares:
  - Receipt text similarity
  - Merchant
  - Amount
  - Expense date
- Assigns a duplicate status:
  - `NONE`
  - `POSSIBLE`
  - `LIKELY`
- Shows the related claim and similarity score when a potential duplicate is detected.

### 👤 Employee Expense Management:

- Create expense claims.
- Generate claims directly from receipt text.
- Edit draft claims.
- Submit claims for approval.
- Track claim status.
- Monitor unpaid expenses.
- View monthly spending against the assigned limit.

### 👨‍💼 Manager Review & Approval:

- View submitted claims from their team.
- Review employee expense details.
- Approve or reject claims.
- Add comments when rejecting a claim.
- Managers can submit their own expenses.
- Managers **cannot approve their own claims**.
- Managers can only review claims belonging to their assigned team.

### 💰 Finance Management:

- View approved claims awaiting payment.
- Process and mark claims as paid.
- Monitor monthly company spending.
- View spending by employee.
- Analyze spending by expense category.
- Track employee spending against monthly limits.
- Identify employees approaching or exceeding their limits.

### 🔐 Role-Based Access Control:

Three dedicated roles with separate permissions:

```text
EMPLOYEE  →  Submit & track expenses
MANAGER   →  Review & approve team expenses
FINANCE   →  Pay claims & monitor spending
```



## 🔄 Workflow:

ClaimFlow AI provides a complete expense reimbursement workflow that starts when an employee submits receipt information and ends when Finance marks the approved claim as paid.

```text
👤 Employee
     │
     │ Paste receipt text
     ▼
🤖 AI Receipt Extraction
     │
     │ Merchant • Date • Amount
     │ Currency • Category • Description
     ▼
📝 Draft Claim
     │
     │ Employee reviews and corrects
     ▼
🔍 Duplicate Detection
     │
     │ Text similarity • Hash
     │ Merchant • Amount • Date
     ▼
📤 Submit Claim
     │
     ▼
👨‍💼 Manager Review
     │
     ├──────────────► ❌ Reject
     │                    │
     │                    ▼
     │                REJECTED
     │
     ▼
✅ Approve
     │
     ▼
💰 Finance Payment Queue
     │
     │ Finance processes payment
     ▼
🟢 PAID
     │
     ▼
🔒 Final State
```



## 👥 User Roles:

ClaimFlow AI supports three distinct user roles, each with responsibilities aligned to the expense reimbursement workflow.

| Role | Responsibilities |
|---|---|
| 👤 **Employee** | Create expense claims, paste receipt text for AI extraction, review and correct claim details, submit claims, and track claim/payment status. |
| 👨‍💼 **Manager** | Submit their own expense claims, review claims submitted by their team, approve or reject claims, and provide rejection comments. Managers cannot approve their own claims. |
| 💰 **Finance** | View approved claims awaiting payment, process and mark claims as paid, monitor monthly spending, analyze spending by category, and track employee spending against monthly limits. |

### 🔐 Role-Based Access:

```text
👤 EMPLOYEE
   └── Create & track own claims

👨‍💼 MANAGER
   └── Review & approve/reject team claims
   └── Submit own claims

💰 FINANCE
   └── Process payments
   └── Monitor company spending
   └── Track monthly limits
```


## 🔍 Duplicate Detection:

ClaimFlow AI includes an intelligent duplicate detection system designed to help prevent the same receipt from being submitted and reimbursed more than once.

The system handles both **exact duplicates** and receipts that contain the same expense information but are **typed slightly differently**.

```text
New Receipt
     │
     ▼
🧹 Text Normalization
     │
     ▼
🔐 SHA-256 Hash Check
     │
     ├── Exact Match ──────────► 🔴 LIKELY
     │
     ▼
📊 Similarity Analysis
     │
     ├── Receipt Text Similarity
     ├── Merchant
     ├── Amount
     └── Expense Date
     │
     ▼
🎯 Duplicate Score
     │
     ├── < 60  ───────────────► 🟢 NONE
     ├── 60–84 ───────────────► 🟡 POSSIBLE
     └── ≥ 85  ───────────────► 🔴 LIKELY
```


## 🤖 AI Receipt Extraction:

ClaimFlow AI lets employees create expense claims by simply pasting the text from their receipt instead of manually entering multiple expense fields.

The application sends the raw receipt text to **Groq**, using **OpenAI GPT-OSS-120B**, which converts the unstructured receipt information into structured claim data. The AI extracts the **merchant, expense date, amount, currency, expense category, description, and extraction confidence** while handling badly formatted text, abbreviations, misspellings, missing labels, and different date formats.

The AI is instructed not to invent information that is not supported by the receipt and to classify the expense into one of the application's predefined categories.

The extracted information is returned as a **Draft Claim** and shown to the employee before submission. The employee can review and correct the AI-generated details and then submit the claim for manager review.

```text
🧾 Receipt Text
      ↓
🤖 Groq AI
      ↓
🧠 GPT-OSS-120B
      ↓
📋 Structured Expense Claim
      ↓
👤 Employee Reviews & Corrects
      ↓
📤 Submit for Manager Review
```


## 🔄 Claim Lifecycle:

ClaimFlow AI follows a controlled claim lifecycle that manages an expense from creation through final payment.

```text
📝 DRAFT
   │
   │ Employee reviews and submits
   ▼
📤 SUBMITTED
   │
   │ Manager reviews
   ├───────────────► ❌ REJECTED
   │
   │ Approved
   ▼
✅ APPROVED
   │
   │ Finance processes payment
   ▼
💰 PAID
   │
   ▼
🔒 FINAL
```

## 🛠️ Tech Stack:

| Layer | Technology | Purpose |
|---|---|---|
| 🎨 Frontend | **React** | Interactive user interface |
| 📘 Frontend Language | **TypeScript** | Type-safe frontend development |
| ⚡ Frontend Tooling | **Vite** | Fast development and production builds |
| 🐍 Backend | **Python** | Backend application development |
| 🚀 API Framework | **FastAPI** | REST API and backend services |
| 🗄️ ORM | **SQLAlchemy** | Database models and database operations |
| 🐘 Database | **PostgreSQL** | Persistent application data storage |
| 🤖 AI Provider | **Groq** | AI inference for receipt extraction |
| 🧠 AI Model | **GPT-OSS-120B** | Converts unstructured receipt text into structured claim data |
| 🔐 Authentication | **JWT** | Secure user authentication and session authorization |
| 🔑 Password Security | **bcrypt** | Password hashing |
| 📚 API Documentation | **FastAPI Swagger / OpenAPI** | Interactive API documentation |
| 🔧 Version Control | **Git & GitHub** | Source control and project hosting |



## 🏗️ Architecture:

ClaimFlow AI follows a **three-layer architecture** with a React frontend, FastAPI backend, and PostgreSQL database, with Groq AI integrated into the backend for receipt extraction.

```text
                         ┌──────────────────────────┐
                         │       👤 USERS           │
                         │                          │
                         │ Employee • Manager       │
                         │ Finance                  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🎨 FRONTEND — React                          │
│                         TypeScript + Vite                        │
│                                                                 │
│  Login  •  Employee Dashboard  •  Manager Dashboard             │
│                 •  Finance Dashboard                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ REST API / JSON
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🚀 BACKEND — FastAPI                         │
│                            Python                               │
│                                                                 │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────────────┐  │
│  │ Authentication│  │ Claims API   │   │ Authorization       │  │
│  │ & JWT         │  │              │   │ & Role Control      │  │
│  └─────────────┘   └──────────────┘   └─────────────────────┘  │
│                                                                 │
│  ┌──────────────────┐       ┌───────────────────────────────┐  │
│  │ 🤖 Receipt       │       │ 🔍 Duplicate Detection        │  │
│  │    Extraction    │       │                               │  │
│  └────────┬─────────┘       └───────────────────────────────┘  │
│           │                                                     │
│           ▼                                                     │
│      🌐 Groq API                                                │
│      GPT-OSS-120B                                                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ SQLAlchemy
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🐘 PostgreSQL                                │
│                                                                 │
│   users  •  claims  •  receipts  •  claim_reviews               │
│                         •  audit_logs                            │
└─────────────────────────────────────────────────────────────────┘
```


## 🗄️ Database Design:

ClaimFlow AI uses **PostgreSQL** as its relational database, with **SQLAlchemy** as the ORM. The database is designed around users, expense claims, receipts, reviews, and audit history.

```text
┌──────────────────────┐
│        USERS         │
├──────────────────────┤
│ id (PK)              │
│ name                 │
│ email                │
│ password_hash        │
│ role                 │
│ manager_id (FK)      │◄──────────┐
│ department           │           │
│ monthly_limit        │           │
│ is_active            │           │
│ created_at           │           │
│ updated_at           │           │
└──────────┬───────────┘           │
           │                       │
           │ 1:N                   │
           ▼                       │
┌──────────────────────┐           │
│       CLAIMS         │           │
├──────────────────────┤           │
│ id (PK)              │           │
│ claim_number         │           │
│ user_id (FK)         │           │
│ merchant             │           │
│ expense_date         │           │
│ amount               │           │
│ currency             │           │
│ category             │           │
│ description          │           │
│ status               │           │
│ duplicate_status     │           │
│ duplicate_of_claim_id│───────────┘
│ duplicate_score      │
│ submitted_at         │
│ approved_at          │
│ rejected_at          │
│ paid_at              │
│ created_at           │
│ updated_at           │
└───────┬──────────────┘
        │
        ├─────────────── 1:1 ───────────────┐
        │                                    │
        ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│      RECEIPTS        │          │    CLAIM_REVIEWS     │
├──────────────────────┤          ├──────────────────────┤
│ id (PK)              │          │ id (PK)              │
│ claim_id (FK)        │          │ claim_id (FK)        │
│ raw_text             │          │ reviewer_id (FK)     │
│ extracted_data       │          │ action                │
│ extraction_confidence│          │ comment               │
│ normalized_text      │          │ created_at            │
│ text_hash            │          └──────────────────────┘
│ created_at           │
└──────────────────────┘

        CLAIMS
           │
           │ 1:N
           ▼
┌──────────────────────┐
│     AUDIT_LOGS       │
├──────────────────────┤
│ id (PK)              │
│ claim_id (FK)        │
│ actor_id (FK)        │
│ event_type           │
│ old_value            │
│ new_value            │
│ created_at            │
└──────────────────────┘
```

### 🔗 Key Relationships:
```
User
 ├── manages → Users
 └── owns → Claims

Claim
 ├── has → Receipt
 ├── has → Reviews
 └── has → Audit Logs

Review
 └── belongs to → Reviewer (User)

Audit Log
 └── belongs to → Actor (User)

Claim
 └── can reference → Another Claim
                    (Duplicate)
```


## 📁 Project Structure

```text
claimflow-ai/
│
├── 📂 backend/
│   │
│   ├── 📂 app/
│   │   ├── 📂 api/
│   │   │   ├── auth.py
│   │   │   └── claims.py
│   │   │
│   │   ├── 📂 core/
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   │
│   │   ├── 📂 database/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   ├── seed.py
│   │   │   └── reset_demo_data.py
│   │   │
│   │   ├── 📂 models/
│   │   │   ├── user.py
│   │   │   ├── claim.py
│   │   │   ├── receipt.py
│   │   │   ├── review.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── 📂 schemas/
│   │   │   ├── auth.py
│   │   │   └── claim.py
│   │   │
│   │   ├── 📂 services/
│   │   │   ├── receipt_extractor.py
│   │   │   └── duplicate_detector.py
│   │   │
│   │   └── main.py
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── 📂 frontend/
│   │
│   ├── 📂 public/
│   │
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   └── ProtectedRoute.tsx
│   │   │
│   │   ├── 📂 pages/
│   │   │   ├── Login.tsx
│   │   │   ├── EmployeeDashboard.tsx
│   │   │   ├── ManagerDashboard.tsx
│   │   │   └── FinanceDashboard.tsx
│   │   │
│   │   ├── 📂 services/
│   │   │   └── api.ts
│   │   │
│   │   ├── 📂 types/
│   │   │   └── index.ts
│   │   │
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── 📄 .gitignore
├── 📄 requirements.txt
└── 📄 README.md
```

### 🧩 Backend Structure

| Directory / File | Purpose |
|---|---|
| `api/` | FastAPI REST API endpoints for authentication and expense claims |
| `core/` | Authentication, JWT security, and role-based authorization |
| `database/` | Database connection, initialization, demo-data seeding, and reset utilities |
| `models/` | SQLAlchemy database models |
| `schemas/` | Pydantic request and response schemas |
| `services/` | Business services including AI receipt extraction and duplicate detection |
| `main.py` | FastAPI application entry point |

### 🎨 Frontend Structure

| Directory / File | Purpose |
|---|---|
| `components/` | Reusable React components such as protected routes |
| `pages/` | Role-specific application screens |
| `services/` | API communication with the FastAPI backend |
| `types/` | TypeScript interfaces and application types |
| `App.tsx` | Application routing |
| `App.css` | Application-wide component styling |
| `index.css` | Global styling |
| `main.tsx` | React application entry point |

### 🔧 Core Services:

```
receipt_extractor.py
        ↓
🤖 Groq / GPT-OSS-120B
        ↓
Structured Claim Data

duplicate_detector.py
        ↓
🧹 Normalization
        ↓
🔐 Hash Comparison
        ↓
📊 Similarity Analysis
        ↓
Duplicate Status + Score
```


## 🚀 Local Setup:

Follow the steps below to run **ClaimFlow AI** locally.

### 📋 Prerequisites:

Make sure the following are installed:

- **Python 3.12+**
- **Node.js 18+**
- **PostgreSQL 17+**
- **Git**
- A **Groq API key**

---

### 1. 📥 Clone the Repository:

```bash
git clone https://github.com/msns-1927/ClaimFlow-AI-Intelligent-Expense-Claims-Management-Platform.git
cd ClaimFlow-AI-Intelligent-Expense-Claims-Management-Platform
```

### 2. 🐍 Backend Setup:

Create and activate a Python virtual environment from the project root.

Windows PowerShell:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:
```
pip install -r backend/requirements.txt
```

### 3. 🗄️ Database Setup:

Create a PostgreSQL database named:
``` 
expense_claims
 ```

Create the backend environment file:
```
backend/.env
```

Add the required configuration:
```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5433/expense_claims
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secure_secret_key
```
> Update the PostgreSQL host, port, username, password, and database name according to your local PostgreSQL configuration.


### 4. 🌱 Seed Demo Data:

Navigate to the backend directory:
```
cd backend
```

With the virtual environment activated, run:

``` 
python -m app.database.seed
 ```

The seed script creates the demo users and supporting data used to demonstrate the application.


### 5. 🚀 Start the Backend:

From the `backend` directory, start the FastAPI server:

```
uvicorn app.main:app --reload
```
The API will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```


### 6. 🎨 Frontend Setup:

Open a new terminal and navigate to the frontend:

```
cd frontend
```
Install the frontend dependencies:

```
npm install
```
Start the Vite development server:

```
npm run dev
```
Vite will display the local frontend URL in the terminal, typically:

```
http://localhost:5173
```
> If Vite selects another available port, use the URL displayed in the terminal.


### 7. 🔐 Login:

Use one of the available demo accounts from the **Demo Accounts** section to access the application.

```
Employee → Employee Dashboard
Manager  → Manager Dashboard
Finance  → Finance Dashboard
```

### 8. 🛑 Stop the Application:

To stop either development server, press:

```
Ctrl + C
```
The backend and frontend run independently, so both development servers should remain running while using the application locally.


## 🌐 Live Demo & Deployment:

ClaimFlow AI is deployed using **Render** with separate services for the frontend, backend API, and PostgreSQL database.

### 🚀 Live Application:

**Frontend:**

https://claimflow-frontend.onrender.com

The frontend provides the complete role-based application interface for Employees, Managers, and Finance users.

---

### ⚙️ Backend API:

https://claimflow-backend.onrender.com

The backend is powered by **FastAPI** and provides the REST API used by the frontend.

---

### 📚 Interactive API Documentation:

https://claimflow-backend.onrender.com/docs

FastAPI Swagger UI provides interactive documentation for the available API endpoints.

---

### ❤️ Backend Health Check:

https://claimflow-backend.onrender.com/health

The health endpoint verifies that the backend is running and connected to the PostgreSQL database.

Expected response:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

### ☁️ Deployment Architecture:

                    👤 Users
                       │
                       ▼
        ┌─────────────────────────────┐
        │     React + TypeScript      │
        │        Vite Frontend        │
        │           Render            │
        └──────────────┬──────────────┘
                       │
                       │ REST API / JSON
                       ▼
        ┌─────────────────────────────┐
        │       Python + FastAPI      │
        │        Backend API          │
        │           Render            │
        └──────────┬─────────┬────────┘
                   │         │
                   │         │
                   ▼         ▼
        ┌──────────────┐   ┌──────────────┐
        │ PostgreSQL   │   │   Groq API   │
        │    Render    │   │ GPT-OSS-120B │
        └──────────────┘   └──────────────┘

### 🔧 Deployment Configuration:

| Component | Platform           | Purpose                                    |
| --------- | ------------------ | ------------------------------------------ |
| Frontend  | Render Static Site | React + TypeScript + Vite application      |
| Backend   | Render Web Service | FastAPI REST API                           |
| Database  | Render PostgreSQL  | Persistent application data                |
| AI        | Groq API           | Receipt text extraction using GPT-OSS-120B |

> The deployed application uses environment variables for database credentials, the Groq API key, and JWT secret management. No secrets are committed to the repository.


## 🔐 Environment Variables

ClaimFlow AI uses environment variables for database credentials, AI API access, and application security configuration.

Create the following file locally:

```text
backend/.env
```
Add:
```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5433/expense_claims
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secure_secret_key
```

### Variables:
| Variable |	Description |
| --- | --- |
| `DATABASE_URL` |	PostgreSQL connection string used by the backend |
| `GROQ_API_KEY`	| API key used to access Groq for AI-powered receipt extraction |
| `SECRET_KEY` |	Secret key used to sign and validate JWT authentication tokens |


### ⚠️ Security:

Never commit the actual `.env` file to GitHub.

The repository includes:

```
backend/.env.example
```
with placeholder values that show the required configuration without exposing secrets.

```
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5433/expense_claims
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=replace_with_a_secure_random_secret
```
The real `backend/.env` file is excluded from version control through `.gitignore`.


## 🔌 API Overview:

ClaimFlow AI provides a REST API through the FastAPI backend for authentication, expense claims, manager reviews, and Finance operations.

### Authentication:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/login` | Authenticate a user and return a JWT token |
| `GET` | `/api/auth/me` | Get the currently authenticated user's details |

### Claims:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/claims` | Create a claim draft manually |
| `POST` | `/api/claims/from-receipt` | Extract receipt details using AI and create a claim draft |
| `GET` | `/api/claims/my` | View the current user's claims |
| `PUT` | `/api/claims/{claim_id}` | Edit a claim while it is in `DRAFT` status |
| `POST` | `/api/claims/{claim_id}/submit` | Submit a draft claim for manager review |

### Manager Review:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/claims/team` | View submitted claims from the manager's team |
| `POST` | `/api/claims/{claim_id}/approve` | Approve a submitted team claim |
| `POST` | `/api/claims/{claim_id}/reject` | Reject a submitted team claim |

Managers cannot approve their own claims.

### Finance:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/finance/dashboard` | View monthly spending, employee limits, category spending, and limit alerts |
| `GET` | `/api/finance/pending` | View approved claims awaiting payment |
| `POST` | `/api/finance/{claim_id}/pay` | Mark an approved claim as paid |

Payment is simulated as part of the application rather than connected to a real payment provider.

### Health Check:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check whether the backend and database are available |

### Interactive API Documentation:

FastAPI provides interactive API documentation through Swagger UI:

```text
http://localhost:8000/docs
```

The OpenAPI specification is available at:

```
http://localhost:8000/openapi.json
```


## 🔐 Security & Authorization:

ClaimFlow AI implements authentication and role-based authorization to ensure that users can only access actions appropriate to their role.

### Authentication:

- Users authenticate through the `/api/auth/login` endpoint.
- Successful login returns a **JWT (JSON Web Token)**.
- Protected API requests require a valid JWT.
- The current user's identity and role are obtained from the authenticated token.
- JWT tokens are signed using a server-side `SECRET_KEY` stored in environment variables.
- Tokens use the **HS256** signing algorithm and have a limited expiration time.

### Password Security:

- User passwords are not stored as plain text.
- Passwords are securely hashed using **bcrypt** before being stored in the database.
- During login, the provided password is verified against the stored password hash.

### Role-Based Authorization:

The application supports three roles:

| Role | Main Permissions |
|---|---|
| `EMPLOYEE` | Create, edit, submit, and view their own claims |
| `MANAGER` | Review, approve, and reject claims belonging to their team |
| `FINANCE` | View spending information and process approved claims for payment |

Authorization checks are enforced on the backend using role-based dependencies rather than relying only on frontend route protection.

### Claim Ownership & Lifecycle Protection:

The backend also validates claim ownership and status before performing sensitive operations.

Examples:

- Employees can edit only their own `DRAFT` claims.
- Submitted claims cannot be edited by the employee.
- Managers can review only claims belonging to their team.
- Managers cannot approve or reject their own claims.
- Only submitted claims can be approved or rejected.
- Finance can pay claims that have reached the appropriate approved state.
- Once a claim is marked `PAID`, it cannot move backward in the claim lifecycle.

### Environment & Secret Management:

Sensitive configuration is stored in environment variables:

```text
DATABASE_URL
GROQ_API_KEY
SECRET_KEY
```
> The actual `.env` file is excluded from Git using `.gitignore`, while `backend/.env.example` provides placeholder configuration for setup.



## 🧠 Decisions & Assumptions:

The assignment leaves several implementation details open, so the following decisions were made to keep the system practical, testable, and within the requested scope.

### Technology Decisions:

- **Frontend:** React with TypeScript and Vite for a responsive role-based web interface.
- **Backend:** Python with FastAPI to provide a structured REST API and automatic OpenAPI documentation.
- **Database:** PostgreSQL for persistent storage of users, claims, receipts, reviews, and audit information.
- **ORM:** SQLAlchemy for database interaction and model management.
- **AI:** Groq API using `openai/gpt-oss-120b` for extracting structured expense information from receipt text.
- **Authentication:** JWT-based authentication with bcrypt password hashing.
- **Development & Validation:** The application was tested through the implemented frontend and backend workflows.

### Expense & Claim Assumptions:

- Expenses are represented in **INR** by default when the receipt indicates Indian currency.
- A claim contains structured information such as merchant, date, amount, category, and description after receipt extraction.
- Users can review and correct AI-extracted information before submitting the claim.
- Claims begin as `DRAFT` and must be explicitly submitted before manager review.
- A submitted claim cannot be edited by the employee.
- A paid claim is considered permanently completed and cannot move backward in the lifecycle.
- Payment is **simulated** rather than integrated with a real banking or payment provider, as permitted by the assignment.

### Role & Approval Assumptions:

- Every employee can belong to a manager through the `manager_id` relationship.
- Managers can review claims submitted by members of their assigned team.
- A manager cannot approve or reject their own claim.
- The demo hierarchy assumes **Anita Rao** can approve claims submitted by managers **Rahul Mehta** and **Priya Sharma**.
- Finance is treated as a separate role responsible for payment processing and monthly spending visibility.

### Duplicate Detection Assumptions:

The assignment states that duplicate receipts may appear on the same day or weeks later and may contain slightly different wording.

To handle this:

- Receipt text is normalized before comparison.
- Exact normalized receipt text is detected using a SHA-256 hash.
- Similar receipts are compared using text similarity together with merchant, amount, and expense date.
- The duplicate score uses:
  - **70%** receipt-text similarity
  - **15%** merchant similarity
  - **10%** amount match
  - **5%** date match
- Scores of **85 or higher** are classified as `LIKELY`.
- Scores from **60 to below 85** are classified as `POSSIBLE`.
- Lower scores are treated as `NONE`.
- Rejected claims are excluded from duplicate comparisons.

### AI Extraction Assumptions:

- The AI is instructed not to invent missing receipt information.
- The model extracts only the fields required to create an expense claim.
- The extracted result is presented to the user before submission.
- Users can correct extracted information before submitting the claim.
- AI extraction confidence is stored with the receipt data.
- The initial implementation accepts **receipt text** rather than direct image/OCR input.

### Demo Data Assumptions:

Because the assignment does not provide production data, realistic demo data was created to demonstrate the complete workflow.

The demo dataset includes:

- Multiple employees, managers, and a Finance user.
- Claims across different expense categories.
- Draft, submitted, approved, rejected, and paid claims.
- A badly written receipt.
- Duplicate receipts with slightly different wording.
- An employee whose spending is close to their monthly limit.
- Manager claims requiring approval from another manager.


## 🤖 AI Tools Used:

AI was used during the development of ClaimFlow AI and is disclosed here as required by the assignment.

### Groq API — Application AI Feature:

**Purpose:** AI-powered receipt text extraction.

Groq is integrated into the backend to process receipt text and convert unstructured receipt information into structured claim data.

The application uses:

```text
Model: openai/gpt-oss-120b
```
The AI extraction workflow:

- User pastes the receipt text.
- The backend sends the text to the Groq API.
- The model extracts relevant expense information.
- The response is validated against the expected structured format.
- The extracted information is shown to the user.
- The user can correct the information before submitting the claim.

The extracted fields include:

- Merchant
- Expense date
- Amount
- Currency
- Expense category
- Description
- Extraction confidence

The AI is explicitly instructed not to invent information that is not present in the receipt text.


### ChatGPT:
- Used as a development assistant for:
  - Architecture and implementation planning
  - Backend and frontend development guidance
  - Debugging and resolving implementation issues
  - API and database design discussions
  - Test-case and edge-case analysis
  - README and documentation refinement
  - Deployment troubleshooting

### Human Review:
- AI-generated suggestions and code were reviewed, tested, modified, and integrated manually.
- Application behavior was validated through functional testing, including authentication, claim lifecycle, duplicate detection, role-based authorization, manager approval/rejection, finance payment, monthly limits, and deployment checks.



## 🧪 Testing & Validation:

The application was validated by testing the main business workflows and role-based access rules across the Employee, Manager, and Finance flows.

### Functional Validation:

The following scenarios were tested:

| Test Area | Validation |
|---|---|
| Employee claim creation | Employee can create a claim and save it as a draft |
| Claim editing | Draft claims can be edited by their owner |
| Submitted claim protection | Submitted claims cannot be edited |
| AI receipt extraction | Receipt text is converted into structured claim information |
| Duplicate detection | Exact and similar receipt entries are detected |
| Claim submission | Draft claims can be submitted for manager review |
| Manager review | Managers can view claims belonging to their team |
| Manager approval | Valid submitted team claims can be approved |
| Manager rejection | Managers can reject submitted team claims |
| Self-approval prevention | Managers cannot approve their own claims |
| Finance payment | Approved claims can be marked as paid |
| Claim lifecycle | Paid claims cannot move backward |
| Monthly spending | Employee spending is calculated against monthly limits |
| Limit alerts | Employees approaching their monthly limit are identified |
| Role protection | Restricted endpoints reject unauthorized roles |
| Manager hierarchy | Manager-to-team relationships are respected |

### AI Extraction Validation:

Receipt extraction was tested using realistic receipt text, including poorly formatted or badly written receipts.

The extraction flow was checked to ensure that:

- Relevant receipt information is converted into structured fields.
- The extracted claim is created as a draft.
- Users can review the extracted information before submission.
- Users can correct the extracted information.
- The extraction confidence is stored with the receipt.

### Duplicate Detection Validation:

Duplicate detection was tested with:

- The same receipt submitted more than once.
- The same receipt represented using slightly different wording.
- Receipt entries with matching merchant, amount, and date.
- Receipts occurring on different dates.

The resulting duplicate classification and score were verified against the implemented similarity rules.

### Build Validation:

The frontend production build was also validated using:

```bash
npm run build
```
The backend was verified to start successfully and connect to the configured PostgreSQL database.

### Validation Approach:

Testing focused on the core requirements of the assignment rather than exhaustive automated test coverage. The main goal was to verify that the complete claim lifecycle works correctly:
```
Receipt / Manual Entry
        ↓
      Draft
        ↓
    Submitted
        ↓
Manager Review
   ↙         ↘
Rejected    Approved
                ↓
              Paid
```


## ⚠️ Known Limitations:

The current version focuses on delivering the core expense-claim workflow within the assignment scope. The following areas could be improved in a production-ready version.

### 🧾 Receipt Image Upload:

- The current AI extraction flow accepts pasted receipt text.
- Direct receipt photo/screenshot upload and OCR are not implemented.
- Adding image upload with OCR would make receipt capture more convenient.

### 💳 Payment Processing:

- Finance payment is simulated within the application.
- No real banking, payroll, or payment-provider integration is implemented.

### 🧪 Automated Testing:

- The project was validated through functional workflow testing.
- A comprehensive automated test suite with unit, integration, and end-to-end tests is not currently included.

### 🔐 Production Security Hardening:

The application includes JWT authentication, bcrypt password hashing, role-based authorization, and environment-based secret management.

For a production-scale deployment, additional measures would be appropriate, including:

- HTTPS enforcement and security headers
- Rate limiting
- Token/session hardening
- Secret rotation
- More extensive security monitoring
- Production-grade logging and alerting

### 🤖 AI Extraction Accuracy:

- AI extraction depends on the quality and clarity of the receipt text.
- Poorly written or incomplete receipts may result in incorrect or incomplete extraction.
- The application therefore allows users to review and correct extracted information before submission.

### 🔍 Duplicate Detection:

- Duplicate detection is similarity-based and therefore cannot guarantee that every duplicate expense will be identified.
- Very different descriptions of the same receipt may produce a lower similarity score.
- The current approach is designed to flag suspicious duplicates for review rather than provide a mathematically perfect duplicate guarantee.

### ☁️ Deployment:

- The application is currently deployed on Render for demonstration and evaluation.
- The deployment uses managed PostgreSQL and separate frontend/backend services.
- A production-scale deployment would require additional infrastructure configuration, monitoring, scaling, backup, disaster-recovery, and security controls.
- Free-tier hosting may also have resource and availability limitations compared with production infrastructure.



## 🚀 Future Improvements:

### What I'd Build With One More Week:

If I had another week to continue developing ClaimFlow AI, I would prioritize the following improvements:

### 1. 🧾 Receipt Image & OCR Support

- Allow users to upload receipt photos and screenshots.
- Add OCR to extract text automatically from images.
- Preserve the original receipt image alongside the claim for auditing.
- Support PDF receipt uploads.

### 2. 🤖 Improve AI Extraction

- Build an evaluation dataset containing different receipt formats.
- Measure extraction accuracy across merchants and receipt layouts.
- Add confidence-based review workflows for low-confidence extractions.
- Improve handling of multilingual receipts and unusual formats.

### 3. 🔍 Smarter Duplicate Detection

- Introduce semantic similarity alongside the existing text-based approach.
- Compare historical expense patterns.
- Improve detection of receipts with significantly different wording.
- Provide clearer explanations for why a claim was flagged as a potential duplicate.

### 4. 🔔 Workflow Notifications

- Add email or in-app notifications for:
  - Claim submission
  - Approval
  - Rejection
  - Payment
- Provide clearer claim-status history to employees and managers.

### 5. 💰 Finance & Reporting

- Add historical spending trends.
- Add department-level and category-level reporting.
- Support CSV/PDF report exports.
- Add configurable budget thresholds and alerts.
- Provide richer Finance analytics.

### 6. 🧪 Automated Testing & CI/CD

- Add unit tests for core business logic.
- Add API integration tests.
- Add frontend and end-to-end tests.
- Configure CI/CD to automatically run validation on every pull request.

### 7. 🔐 Production Hardening

- Add rate limiting and stronger session controls.
- Introduce centralized logging and monitoring.
- Add automated database backups and recovery procedures.
- Improve secret rotation and production security controls.
- Add stronger observability and alerting.

### 8. 📱 User Experience

- Improve mobile responsiveness.
- Add advanced filtering, sorting, and pagination.
- Improve accessibility.
- Provide clearer explanations for AI confidence and duplicate warnings.

---

## 🔮 Longer-Term Future Improvements:

Beyond the one-week development plan, the platform could eventually be extended with:

- Configurable multi-level approval workflows.
- Department- and amount-based approval rules.
- Accounting or payroll integrations.
- Batch receipt processing.
- Automated anomaly and fraud detection.
- More advanced financial forecasting and spending analysis.
- Scalable background processing for AI and OCR workloads.


## 👤 Author:

**Siva Narayana Muppidi**

B.Tech — Artificial Intelligence & Data Science

- 💻 GitHub: https://github.com/msns-1927
- 🔗 LinkedIn: https://www.linkedin.com/in/siva-narayana-muppidi-413259230/



## Screenshots:

### Login:
Role-based login for Employees, Managers, and Finance users.

<p align="center">
<img width="900" alt="Screenshot 2026-09-06 125811" src="https://github.com/user-attachments/assets/135d18ab-3ff8-48d1-a6d9-334bdb61ec44" />
</p>


### Employee Dashboard:
Employees can create claims manually or paste unstructured receipt text for AI-powered extraction.

<p align="center">
<img width="900" alt="Screenshot 2026-09-05 102316" src="https://github.com/user-attachments/assets/921a1974-ab26-4bde-bd0e-947dbef1334e" />
</p>



### AI Receipt Extraction
The system converts unstructured receipt text into structured claim information that the employee can review and correct before submission.

<p align="center">
<img width="900" alt="Screenshot 2026-09-05 102330" src="https://github.com/user-attachments/assets/6d416d76-9816-43eb-8b35-fde41b6d1d21" />
</p>



### Duplicate Receipt Detection
The system detects potential duplicate claims even when the same receipt is entered with slightly different wording.

<p align="center">
<img width="900" alt="Screenshot 2026-09-05 111835" src="https://github.com/user-attachments/assets/ac741d2d-f645-4ca9-8731-8ab57ff2d799" />
</p>


### Manager Dashboard
Managers can review team claims and approve or reject them. Managers cannot approve their own claims.

<p align="center">
<img width="900" alt="Screenshot 2026-09-05 134828" src="https://github.com/user-attachments/assets/b7f05a33-5c67-4c83-8317-b7702c6312de" />
</p>


### Finance Dashboard
Finance can monitor monthly spending, employee limits, categories, approved claims, and mark approved claims as paid.

<p align="center">
<img width="900" alt="Screenshot 2026-09-05 103856" src="https://github.com/user-attachments/assets/ff91051b-5bbe-4ec1-9ceb-1f88c178d17f" />
</p>


