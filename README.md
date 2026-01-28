# Mock-PharmacyBenefitManagement-System

A web based project of medium-complexity that simulates core PBM (Pharmacy Benefits Manager) functionality by processing, analyzing, and visualizing prescription drug claims data.

## Core Technical Alignment

### This project utilizes the following tech features:

- Python/Flask backend with RESTful APIs
- SQLAlchemy ORM with advanced PostgreSQL features
- AWS deployment (EC2/RDS or containerized on ECS)
- Infrastructure as Code using Terraform
- Unit testing with pytest
- Git/version control best practices

## Project Architecture

1. Backend (Python/Flask)  
   /api  
   /claims - CRUD operations for prescription claims  
   /analytics - Aggregate data endpoints  
   /members - Member management  
   /drugs - Drug catalog and pricing  
   /reports - Generate cost analysis reports

2. Database Schema (PostgreSQL)

- Key Tables:
    - members - Patient/member information
    - claims - Prescription claims with timestamps, costs, pharmacy info
    - drugs - Drug catalog (NDC codes, generic/brand, therapeutic class)
    - pharmacies - Pharmacy network data
    - formulary - Drug tier classifications and cost structures
    - Advanced PostgreSQL Features to Showcase:
        - CTEs for complex claim aggregations
        - Window functions for trending analysis (costs over time, member utilization patterns)
        - Materialized views for pre-computed analytics dashboards
        - Full-text search on drug names and descriptions
        - Stored procedures for claim adjudication logic
        - Indexes for performance optimization on large datasets

3. Key Features

- Core Functionality:
    - Ingest and validate prescription claims (CSV upload or API)
    - Member portal to view their claims history
    - Basic claims processing workflow (pending → approved → paid)
    - Drug Catalog search with autocomplete
    - Pharmacy Network to manage pharmacy network and locations

- Analytics and Reports
    - Dashboard showing:
        - Total claims cost by time period
        - Generic vs. brand utilization rates
        - Top 10 most expensive drugs
        - Cost trends using window functions
        - Pharmacy network performance metrics
    - Use CTEs for complex aggregations like "members with >3 claims in 30 days"
    - Generate cost savings reports (brand → generic opportunities)

- Advanced Features:
    - Prior authorization workflow simulation
    - Formulary tier checking (is drug covered? what's the copay?)
    - Claims anomaly detection (duplicate claims, unusual costs)

4. Infrastructure (AWS + Terraform)  
   ├── VPC with public/private subnets  
   ├── RDS PostgreSQL instance (private subnet)  
   ├── EC2 instance or ECS container running Flask app  
   ├── S3 bucket for claim document storage  
   ├── CloudWatch for logging and monitoring  
   ├── Application Load Balancer  
   ├── Route 53 for DNS (optional)

5. Testing Strategy

- Unit tests for business logic (claim validation, cost calculations)
- Integration tests for API endpoints
- Database tests for complex queries and stored procedures
- Target 70%+ code coverage
