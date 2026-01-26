
#!/bin/bash
set -e

echo "========================================="
echo "AWS Infrastructure Setup"
echo "========================================="
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not installed"
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not installed"
    exit 1
fi

# AWS Configuration
echo "1. Configuring AWS credentials..."
if [ ! -f ~/.aws/credentials ]; then
    echo "No AWS credentials found. Running aws configure..."
    aws configure
else
    echo "✓ AWS credentials already configured"
fi

# Navigate to Terraform directory
cd terraform/environments/dev

# Check for terraform.tfvars
if [ ! -f terraform.tfvars ]; then
    echo ""
    echo "2. Creating terraform.tfvars..."
    read -sp "Enter database password: " db_password
    echo ""
    cat > terraform.tfvars << EOF
aws_region  = "us-east-1"
db_password = "$db_password"
EOF
    chmod 600 terraform.tfvars
    echo "✓ terraform.tfvars created"
else
    echo "2. ✓ terraform.tfvars already exists"
fi

# Initialize Terraform
echo ""
echo "3. Initializing Terraform..."
terraform init

# Validate configuration
echo ""
echo "4. Validating Terraform configuration..."
terraform validate

# Plan infrastructure
echo ""
echo "5. Planning infrastructure..."
terraform plan -out=tfplan

# Ask for confirmation
echo ""
read -p "Do you want to apply this plan? (yes/no): " confirm

if [ "$confirm" == "yes" ]; then
    echo ""
    echo "6. Applying infrastructure..."
    terraform apply tfplan
    
    echo ""
    echo "========================================="
    echo "✓ Infrastructure deployed successfully!"
    echo "========================================="
    echo ""
    echo "Outputs:"
    terraform output
else
    echo "Deployment cancelled"
    rm -f tfplan
fi