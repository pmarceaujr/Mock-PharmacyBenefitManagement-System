# Mock-PharmacyBenefitManagement-System - Complete Setup Guide (Part 1 of 5)

## What I Built

A mock-up of a PBM (Pharmacy Benefits Manager) platform using:

- Flask REST API backend
- PostgreSQL database with advanced features
- AWS cloud infrastructure
- Comprehensive test coverage
- React 18 with Vite
- TypeScript
- Tailwind CSS (modern styling)
- shadcn/ui (beautiful components)
- Recharts (data visualization)
- React Router (SPA routing)
- Axios (API calls)
- React Query (data fetching)
- Full documentation

---

## PART 1: MY TOOLS & ENVIRONMENT SETUP

### Step 1: Install Python 3.11

**macOS:**

```bash
brew install python@3.11
python3.11 --version
# Expected output: Python 3.11.x
```

**Ubuntu/Debian Linux:**

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
python3.11 --version
```

**Windows:**

1. Visit https://www.python.org/downloads/
2. Download Python 3.11.x installer
3. Run installer
4. **CRITICAL:** Check "Add Python to PATH"
5. Click "Install Now"
6. Open Command Prompt and verify:

```cmd
python --version
```

---

### Step 2: Install PostgreSQL 15

**macOS:**

```bash
brew install postgresql@15
brew services start postgresql@15
psql --version
# Expected output: psql (PostgreSQL) 15.x
```

**Ubuntu/Debian Linux:**

```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
psql --version
```

**Windows:**

1. Visit https://www.postgresql.org/download/windows/
2. Download PostgreSQL 15 installer
3. Run installer
4. **IMPORTANT:** Write down the password you set for 'postgres' user
5. Keep default port: 5432
6. Finish installation

---

### Step 3: Install Git

**macOS:**

```bash
brew install git
git --version
```

**Ubuntu/Debian Linux:**

```bash
sudo apt install git
git --version
```

**Windows:**

1. Visit https://git-scm.com/download/win
2. Download installer
3. Use all default settings
4. Verify in Command Prompt:

```cmd
git --version
```

---

### Step 4: Install AWS CLI

**macOS:**

```bash
brew install awscli
aws --version
```

**Ubuntu/Debian Linux:**

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

**Windows:**

1. Visit https://aws.amazon.com/cli/
2. Download AWS CLI MSI installer
3. Run installer
4. Verify:

```cmd
aws --version
```

---

### Step 5: Install Terraform

**macOS:**

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform --version
```

**Ubuntu/Debian Linux:**

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install terraform
terraform --version
```

**Windows:**

1. Visit https://www.terraform.io/downloads
2. Download Windows 64-bit zip
3. Extract to `C:\terraform`
4. Add to PATH:
    - Right-click "This PC" → Properties
    - Advanced system settings
    - Environment Variables
    - Under "System variables", find "Path"
    - Click "Edit" → "New"
    - Add `C:\terraform`
    - Click OK on all windows
5. Open NEW Command Prompt and verify:

```cmd
terraform --version
```

---

### Step 6: Install VS Code (Highly Recommended)

1. Visit https://code.visualstudio.com/
2. Download for your OS
3. Install with defaults
4. Open VS Code
5. Click Extensions icon (left sidebar) or press Ctrl+Shift+X
6. Install these extensions:
    - **Python** by Microsoft
    - **PostgreSQL** by Chris Kolkman
    - **Terraform** by HashiCorp
    - **GitLens** by GitKraken

---

### Step 7: Install Node.js and npm

**macOS:**

```bash
# Install using Homebrew
brew install node

# Verify installation
node --version  # Should show v18.x.x or higher
npm --version   # Should show v9.x.x or higher
```

**Ubuntu/Debian Linux:**

```bash
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

**Windows:**

1. Visit https://nodejs.org/
2. Download "LTS" version (18.x or higher)
3. Run installer with default settings
4. Open Command Prompt and verify:

```cmd
node --version
npm --version
```

## PART 2: HOW I INITIALIZED MY PROJECT

### Step 7: Create Project Directory

Open Terminal (macOS/Linux) or Command Prompt (Windows):

```bash
# Navigate to home directory
cd ~

# Create projects folder
mkdir projects
cd projects

# Create project
mkdir Mock-PharmacyBenefitManagement-System
cd Mock-PharmacyBenefitManagement-System

```

---

### Step 8: Create repo on GitHub

1. Goto git.com
2. Login to your GitHub account
3. Create a new repo
    - **NOTE:** Select python template for .gitignore
4. Clone your repo

```bash
git clone https://github.com/YourUserName/YourCustomGitHubRepo.git
```

---

### Step 9: Create Directory Structure

```bash
# Make sure you're in frontend directory
pwd  # Should show: .../Mock-PharmacyBenefitManagement-System/frontend

# Create all backend directories at once
mkdir -p backend/app/models
mkdir -p backend/app/routes
mkdir -p backend/app/services
mkdir -p backend/app/utils
mkdir -p backend/tests/unit
mkdir -p backend/tests/integration
mkdir -p backend/migrations
mkdir -p terraform/modules/networking
mkdir -p terraform/modules/database
mkdir -p terraform/modules/compute
mkdir -p terraform/modules/storage
mkdir -p terraform/environments/dev
mkdir -p terraform/environments/prod
mkdir -p scripts
mkdir -p docs

# Make sure you're in project root directory
pwd  # Should show: .../Mock-PharmacyBenefitManagement-System

# Create  frontend directory
mkdir -p frontend

```

**Windows users:** If `mkdir -p` doesn't work: Create same struture using mkdir:

```cmd
mkdir backend\app\models
mkdir backend\app\routes
mkdir backend\app\services
mkdir backend\app\utils
mkdir backend\tests\unit
mkdir backend\tests\integration
mkdir backend\migrations
mkdir terraform\modules\networking
mkdir terraform\modules\database
mkdir terraform\modules\compute
mkdir terraform\modules\storage
mkdir terraform\environments\dev
mkdir terraform\environments\prod
mkdir scripts
mkdir docs
mkdir frontend
```

**Verify Structure:**

```bash
# Install tree (if not already)
# macOS: brew install tree
# Ubuntu: sudo apt install tree
# Windows: use File Explorer

tree -L 2
```

You should see:

```
.
├── backend
│   ├── app
│   ├── migrations
│   ├── scripts
│   └── tests
├── docs
├── terraform
│   ├── environments
│   └── modules
└── frontend


```

---

### Step 10: Setup Python Virtual Environment

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Your prompt should now show (venv) at the start
# Example: (venv) user@computer:~/projects/Mock-PharmacyBenefitManagement-System/backend$
```

---

### Step 11: Create requirements.txt

# Make sure you're in backend directory with venv activated

Creat a file named: requirements.txt

Copy and Paste the following into you requirements.txt file

```
# Web Framework
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5

# Database
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23

# Environment
python-dotenv==1.0.0

# Serialization/Validation
marshmallow==3.20.1
flask-marshmallow==0.15.0
marshmallow-sqlalchemy==0.29.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-flask==1.3.0
pytest-mock==3.12.0

# Data Generation
Faker==20.1.0

# AWS
boto3==1.34.8

# Utilities
python-dateutil==2.8.2

# API Documentation
flask-swagger-ui==4.11.1

# Production Server
gunicorn==21.2.0
```

---

### Step 12: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies (will take 2-5 minutes)
pip install -r requirements.txt

# Verify installation
pip list
```

You should see all packages listed. If any fail:

```bash
# Try installing problematic package individually
pip install <package-name>
```

---

## PART 3: DATABASE SETUP

### Step 13: Create PostgreSQL Database

#### Connect to PostgreSQL

**macOS/Linux:**

```bash
# Try this first
sudo -u postgres psql

# If that fails, try
psql postgres
```

**Windows:**

```cmd
# Open Command Prompt as Administrator
cd "C:\Program Files\PostgreSQL\15\bin"
psql -U postgres
# Enter the password you set during installation
```

You should see: `postgres=#`

---

#### Run Database Setup Commands

Copy and paste these commands one at a time:

```sql
-- Create database
CREATE DATABASE pharmacybenmgr;

-- Create user
CREATE USER pbm_user WITH PASSWORD 'dev_password_123';

-- Grant database privileges
GRANT ALL PRIVILEGES ON DATABASE pharmacybenmgr TO pbm_user;

-- Connect to new database
\c pharmacybenmgr

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO pbm_user;

-- Verify connection
SELECT current_database();

-- Exit
\q
```

**Expected Output:**

- `CREATE DATABASE`
- `CREATE ROLE`
- `GRANT`
- `You are now connected to database "pharmacybenmgr"`
- `GRANT`
- ` pharmacybenmgr`

---

### Step 14: Test Database Connection

```bash
# Test connection
psql -U pbm_user -d pharmacybenmgr -h localhost

# Password: dev_password_123

# You should see: pharmacybenmgr=>

# List tables (should be empty for now)
\dt

# Exit
\q
```

If connection fails:

1. Check PostgreSQL is running: `pg_isready`
2. Verify password: `dev_password_123`
3. Check if port 5432 is open: `netstat -an | grep 5432`

---

### Step 15: Create Environment Configuration

1. Create a Config directory in backend
2. Create a file named .env
3. Copy the follwing into the .env file

```bash
# Flask Configuration
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# Database Configuration
DATABASE_URL=postgresql://pbm_user:dev_password_123@localhost:5432/pharmacybenmgr

# AWS Configuration (fill later)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=

# Application Settings
ITEMS_PER_PAGE=20
MAX_UPLOAD_SIZE=10485760

```

**Verify .env file:**

```bash
cat .env
# Should display all the configuration
```

---

## PART 4: VERIFY BACKEND SETUP

### Step 16: Final Verification Checklist

Run each command and verify output:

```bash
# 1. Python version
python3.11 --version
# Expected: Python 3.11.x

# 2. PostgreSQL version
psql --version
# Expected: psql (PostgreSQL) 15.x

# 3. Git version
git --version
# Expected: git version 2.x.x

# 4. AWS CLI version
aws --version
# Expected: aws-cli/2.x.x

# 5. Terraform version
terraform --version
# Expected: Terraform v1.x.x

# 6. Virtual environment activated
which python
# Expected: /path/to/Mock-PharmacyBenefitManagement-System/backend/venv/bin/python

# 7. Packages installed
pip list | grep Flask
# Should show Flask and Flask-related packages

# 8. Database connection
psql -U pbm_user -d pharmacybenmgr -h localhost -c "SELECT version();"
# Should show PostgreSQL version info
```

**All checks passed?** ✅ ASll the prerequisites are now satisfied

**Any checks failed?** ❌ Go back to the relevant step and troubleshoot.

---

## PART 5: FRONTEND SETUP

### Step 16: Verify Backend is Running

1. Before building frontend, ensure backend API is accessible:
    - In a separate terminal, navigate to backend

```bash
cd ~/projects/Mock-PharmacyBenefitManagement-System/backend
# activate .vevn

# Start backend server
python run.py

# Should see:
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.12:5000
Press CTRL+C to quit
 * Restarting with stat

# In a new terminal
curl http://localhost:5000/health

# Expected response:
{
  "message": "the Mock-PBM System API is healthy, maybe not wealthy, but very wise",
  "status": "running"
}
```

---

### Step 17: Create React Application

1. Create Vite + React + TypeScript Project

```bash
# Navigate to project root
cd ~/projects/Mock-PharmacyBenefitManagement-System

# Create React app with Vite
npm create vite@latest frontend -- --template react-ts

# IF prompted:  Install with npm and start now?
# Select:  Yes

# You'll see:
◇  Installing dependencies with npm...

added 176 packages, and audited 177 packages in 10s

45 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
│
◇  Starting dev server...

> frontend@0.0.0 dev
> vite


  VITE v7.3.1  ready in 1288 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

```bash
# Navigate to frontend directory
cd frontend

# Install base dependencies
npm install

# This will take 1-2 minutes

# You should see: added XXX packages
```

### Step 18: Install Additional Packages

1. UI Framework and Components

```bash
npm install -D tailwindcss@3 postcss autoprefixer
npm install @radix-ui/react-slot @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install @radix-ui/react-select @radix-ui/react-label @radix-ui/react-tabs
npm install class-variance-authority clsx tailwind-merge

# Routing (for SPA)
npm install react-router-dom

# Data Fetching and State Management
npm install @tanstack/react-query axios

# Charts and Visualization
npm install recharts

# Icons
npm install lucide-react

# Form Handling
npm install react-hook-form zod @hookform/resolvers

# Date Handling
npm install date-fns

# Development Dependencies
npm install -D @types/node
```

### Step 19: Configure Tailwind CSS

1. Initialize Tailwind

```bash
# Still in frontend directory
npx tailwindcss init -p

# This will create:
# Created Tailwind CSS config file: tailwind.config.js
# Created PostCSS config file: postcss.config.js
```

### Step 20: Update Directory Structure

```bash
# Make sure you're in frontend directory
pwd  # Should show: .../Mock-PharmacyBenefitManagement-System/frontend

# Create  frontend directory
mkdir -p frontend/src/components/ui
mkdir -p frontend/src/components/charts
mkdir -p frontend/src/components/claims
mkdir -p frontend/src/components/members
mkdir -p frontend/src/components/dashboard
mkdir -p frontend/src/components/layout
mkdir -p frontend/src/pages
mkdir -p frontend/src/services
mkdir -p frontend/src/hooks
mkdir -p frontend/src/types
mkdir -p frontend/src/utils
mkdir -p frontend/src/lib

```

**Windows users:** If `mkdir -p` doesn't work: Create same struture using mkdir:

```cmd

mkdir frontend/src/components/ui
mkdir frontend/src/components/charts
mkdir frontend/src/components/claims
mkdir frontend/src/components/members
mkdir frontend/src/components/dashboard
mkdir frontend/src/components/layout
mkdir frontend/src/pages
mkdir frontend/src/services
mkdir frontend/src/hooks
mkdir frontend/src/types
mkdir frontend/src/utils
mkdir frontend/src/lib
```

**Verify Structure:**

```bash
# Install tree (if not already)
# macOS: brew install tree
# Ubuntu: sudo apt install tree
# Windows: use File Explorer

tree -L 2
```

You should see:

```
.
├── backend
│   ├── app
│   ├── migrations
│   ├── scripts
│   └── tests
├── docs
├── terraform
│   ├── environments
│   └── modules
└── frontend
    ├──src
    ├── components
    │   ├── charts
    │   ├── claims
    │   ├── dashboard
    │   ├── layout
    │   ├── members
    │   └── ui
    ├── hooks
    ├── lib
    ├── pages
    ├── services
    ├── types
    └── utils

```

### Step 21: Test Initial Setup

1. Start Development Server

```bash
# Make sure you're in frontend directory
npm run dev

# Expected output:
  VITE v4.x.x  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

2. Open Browser
    - Open browser (Chrome, Firefox, Safari, Edge)
    - Go to: http://localhost:3000
    - You should see the default Vite + React page

**All checks passed?** ✅ ASll the prerequisites are now satisfied

**Any checks failed?** ❌ Go back to the relevant step and troubleshoot.
