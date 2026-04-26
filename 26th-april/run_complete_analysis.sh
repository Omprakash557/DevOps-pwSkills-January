#!/bin/bash
# run_complete_analysis.sh
# Complete script to run pytest and SonarQube analysis

set -e  # Exit on error

# ============================================================================
# COLOR CODES FOR OUTPUT
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_KEY="python_user_management_app"
PROJECT_NAME="Python User Management System"
PROJECT_VERSION="1.0.0"
SONAR_HOST_URL="http://localhost:9000"

# ============================================================================
# FUNCTIONS
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ============================================================================
# CHECK PREREQUISITES
# ============================================================================

check_prerequisite() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is not installed"
        echo "   Install with: pip install $2 (or use package manager)"
        exit 1
    fi
}

print_header "Checking Prerequisites"

check_prerequisite "pytest" "pytest"
check_prerequisite "coverage" "coverage"
check_prerequisite "sonar-scanner" "sonar-scanner"

print_success "All prerequisites installed"

# ============================================================================
# CHECK SONARQUBE SERVER
# ============================================================================

print_header "Checking SonarQube Server"

if curl -s "$SONAR_HOST_URL/api/system/status" | grep -q '"status":"UP"'; then
    print_success "SonarQube server is running"
else
    print_error "SonarQube server is not running at $SONAR_HOST_URL"
    echo "   Start it with:"
    echo "   cd sonarqube-x.x.x/bin/linux-x86-64"
    echo "   ./sonar.sh console"
    exit 1
fi

# ============================================================================
# CHECK SONAR TOKEN
# ============================================================================

print_header "Checking SonarQube Token"

if [ -z "$SONAR_TOKEN" ]; then
    print_error "SONAR_TOKEN environment variable not set"
    echo "   Generate token in SonarQube UI:"
    echo "   1. Go to http://localhost:9000"
    echo "   2. My Account → Security"
    echo "   3. Generate Tokens"
    echo "   4. Set environment variable:"
    echo "      export SONAR_TOKEN=<your_token>"
    exit 1
fi

print_success "SONAR_TOKEN is set"

# ============================================================================
# STEP 1: RUN PYTEST
# ============================================================================

print_header "Step 1: Running Pytest"

if pytest test_user_manager.py -v --tb=short; then
    print_success "Pytest completed successfully"
else
    print_error "Pytest failed"
    exit 1
fi

# ============================================================================
# STEP 2: GENERATE COVERAGE
# ============================================================================

print_header "Step 2: Generating Coverage Report"

if coverage run -m pytest test_user_manager.py > /dev/null 2>&1; then
    print_success "Test execution completed"
else
    print_error "Failed to generate coverage data"
    exit 1
fi

# Generate XML report for SonarQube
if coverage xml; then
    print_success "Generated coverage.xml"
else
    print_error "Failed to generate coverage.xml"
    exit 1
fi

# Show coverage report
print_info "Coverage Summary:"
echo ""
coverage report
echo ""

# ============================================================================
# STEP 3: RUN CODE ANALYSIS TOOLS (OPTIONAL)
# ============================================================================

print_header "Step 3: Running Code Analysis Tools (Optional)"

# Run flake8 if available
if command -v flake8 &> /dev/null; then
    print_info "Running flake8..."
    flake8 user_manager.py || print_warning "Flake8 found issues"
else
    print_warning "flake8 not installed (optional)"
fi

# Run pylint if available
if command -v pylint &> /dev/null; then
    print_info "Running pylint..."
    pylint user_manager.py || print_warning "Pylint found issues"
else
    print_warning "pylint not installed (optional)"
fi

# Run bandit if available (security)
if command -v bandit &> /dev/null; then
    print_info "Running bandit (security check)..."
    bandit -r user_manager.py || print_warning "Bandit found issues"
else
    print_warning "bandit not installed (optional)"
fi

# ============================================================================
# STEP 4: RUN SONARQUBE ANALYSIS
# ============================================================================

print_header "Step 4: Running SonarQube Analysis"

print_info "Project Key: $PROJECT_KEY"
print_info "Project Name: $PROJECT_NAME"
print_info "Server: $SONAR_HOST_URL"
echo ""

if sonar-scanner \
  -Dsonar.projectKey="$PROJECT_KEY" \
  -Dsonar.projectName="$PROJECT_NAME" \
  -Dsonar.projectVersion="$PROJECT_VERSION" \
  -Dsonar.sources=. \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.login="$SONAR_TOKEN"; then
    print_success "SonarQube analysis completed successfully"
else
    print_error "SonarQube analysis failed"
    exit 1
fi

# ============================================================================
# SUMMARY
# ============================================================================

print_header "Analysis Complete! 🎉"

echo ""
echo "📊 Results Dashboard:"
echo "   http://localhost:9000/dashboard?id=$PROJECT_KEY"
echo ""
echo "📈 Coverage Report (HTML):"
echo "   Open: htmlcov/index.html"
echo ""
echo "✅ All checks passed!"
echo ""

print_success "Analysis pipeline completed successfully"
