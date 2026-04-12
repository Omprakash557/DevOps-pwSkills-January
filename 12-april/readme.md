# Python Sample Project for Jenkins Pipeline

A beginner-friendly guide to integrate a simple Python application with Jenkins CI/CD automation.

## Project Structure

```
python-jenkins-demo/
├── app.py
├── test_app.py
├── requirements.txt
├── Jenkinsfile
├── .gitignore
└── README.md
```

---

## Step 1: Simple Python Application

### File: app.py

Create a simple calculator application with basic functions.

```python
#!/usr/bin/env python3
"""Simple Calculator Application for Jenkins Demo"""

def add(a, b):
    """Add two numbers"""
    return a + b


def subtract(a, b):
    """Subtract two numbers"""
    return a - b


def multiply(a, b):
    """Multiply two numbers"""
    return a * b


def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    """Main function to demonstrate calculator"""
    print("=== Python Calculator ===")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"5 - 3 = {subtract(5, 3)}")
    print(f"5 * 3 = {multiply(5, 3)}")
    print(f"6 / 3 = {divide(6, 3)}")
    print("========================")


if __name__ == "__main__":
    main()
```

**To run locally:**
```bash
python3 app.py
```

---

## Step 2: Python Dependencies

### File: requirements.txt

List all Python packages needed for the project.

```
pytest==7.4.0
pytest-cov==4.1.0
flake8==6.0.0
```

**To install:**
```bash
pip3 install -r requirements.txt
```

---

## Step 3: Unit Tests

### File: test_app.py

Write unit tests to verify all functions work correctly.

```python
#!/usr/bin/env python3
"""Unit Tests for Calculator Application"""

import unittest
from app import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    """Test cases for calculator functions"""
    
    def test_add(self):
        """Test addition"""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
    
    def test_subtract(self):
        """Test subtraction"""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(10, 10), 0)
    
    def test_multiply(self):
        """Test multiplication"""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 100), 0)
    
    def test_divide(self):
        """Test division"""
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(1, 3), 0.333, places=2)
    
    def test_divide_by_zero(self):
        """Test division by zero raises error"""
        with self.assertRaises(ValueError):
            divide(10, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

**To run tests:**
```bash
python3 -m pytest test_app.py -v
```

---

## Step 4: Jenkins Pipeline Configuration

### File: Jenkinsfile

Define the complete CI/CD pipeline for Jenkins.

```groovy
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
    }
    

    
    stages {
        
        stage('Setup Python') {
            steps {
                echo "Setting up Python environment..."
                sh 'python3 --version'
                sh 'pip3 --version'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'pip3 install -r requirements.txt'
            }
        }
        
        
        stage('Run Application') {
            steps {
                echo "Running the application..."
                sh 'python3 app.py'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh 'python3 -m pytest test_app.py -v --tb=short'
            }
        }
        
        stage('Test Coverage') {
            steps {
                echo "Generating test coverage report..."
                sh 'python3 -m pytest test_app.py --cov=app --cov-report=term-missing || true'
            }
        }
        
        stage('Build Artifacts') {
            steps {
                echo "Creating build artifacts..."
                sh '''
                    mkdir -p dist
                    cp app.py dist/
                    cp test_app.py dist/
                    cp requirements.txt dist/
                    echo "Artifacts ready in dist/ directory"
                '''
            }
        }
    }
    
    post {
        always {
            echo "Cleaning up workspace..."
            cleanWs()
        }
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed! Check logs above."
        }
    }
}
```

---

## Step 5: Git Configuration

### File: .gitignore

Ignore unnecessary files in version control.

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
*.log
```

---

## Step 6: Jenkins Setup Instructions

### Prerequisites
- Jenkins installed and running
- Git installed on Jenkins server
- Python 3.7+ installed on Jenkins server
- GitHub account with public repository

### Step 6.1: Install Required Jenkins Plugins

1. Go to **Manage Jenkins > Manage Plugins**
2. Search and install:
   - Git Plugin
   - Pipeline Plugin
   - (Optional) Blue Ocean for better visualization

### Step 6.2: Create Pipeline Job

1. Click **New Item** in Jenkins dashboard
2. Enter job name: `python-demo-pipeline`
3. Select **Pipeline**
4. Click **OK**

### Step 6.3: Configure Pipeline

**Option A: Pipeline Script from SCM (Recommended)**

1. Scroll to **Pipeline** section
2. Select **Pipeline script from SCM**
3. Fill in:
   - **SCM**: Git
   - **Repository URL**: `https://github.com/YOUR-USERNAME/python-jenkins-demo.git`
   - **Branch Specifier**: `*/main`
   - **Script Path**: `Jenkinsfile`
4. Click **Save**

**Option B: Direct Jenkinsfile in Jenkins**

1. Select **Pipeline script**
2. Copy the Jenkinsfile content from Step 4
3. Paste it in the text area
4. Click **Save**

---

## Step 7: Run the Pipeline

### Triggering a Build

1. Click **Build Now** to start the pipeline
2. Watch the build progress in **Build History**
3. Click the build number to view details
4. Click **Console Output** to see real-time logs

### Expected Pipeline Execution Flow

```
Checkout Code
    └─> Clone from GitHub
    
Setup Python
    └─> Verify Python 3.x installed
    
Install Dependencies
    └─> Install pytest, flake8, pytest-cov
    
Code Quality Check
    └─> Run flake8 linter
    
Run Application
    └─> Execute app.py
    └─> Show calculation results
    
Run Tests
    └─> Run pytest on test_app.py
    └─> Execute all test cases
    
Test Coverage
    └─> Generate coverage report
    
Build Artifacts
    └─> Create dist/ directory
    └─> Copy application files
```

### Sample Output

```
=== Pipeline Output ===

Checking out code from GitHub...
Setting up Python environment...
Python 3.9.x
pip 23.x.x

Installing Python dependencies...
Successfully installed pytest-7.4.0 pytest-cov-4.1.0 flake8-6.0.0

Running code quality checks...
app.py:5:1: E302 expected 2 blank lines, found 1
test_app.py: passed flake8 check

Running the application...
=== Python Calculator ===
5 + 3 = 8
5 - 3 = 2
5 * 3 = 15
6 / 3 = 2.0
========================

Running unit tests...
test_app.py::TestCalculator::test_add PASSED
test_app.py::TestCalculator::test_subtract PASSED
test_app.py::TestCalculator::test_multiply PASSED
test_app.py::TestCalculator::test_divide PASSED
test_app.py::TestCalculator::test_divide_by_zero PASSED

5 passed in 0.12s

Coverage Report:
Name      Stmts   Miss  Cover
app.py       16      0   100%
test_app.py  20      0   100%

Pipeline executed successfully!
```

---

## Student Assignment Ideas

### Task 1: Add New Function

Add a `power()` function to calculate exponents:

```python
def power(base, exponent):
    """Calculate base to the power of exponent"""
    return base ** exponent
```

Then:
- Write a test case for `power()`
- Update requirements.txt if needed
- Commit and push to GitHub
- Verify Jenkins pipeline passes

### Task 2: Intentional Failure Scenario

1. Modify `test_app.py` to fail intentionally:
   ```python
   def test_add():
       assert add(2, 3) == 6  # Wrong expectation
   ```
2. Commit and push
3. Observe Jenkins failure logs
4. Fix the test and watch pipeline succeed

### Task 3: Add Lint Stage to Pipeline

Update **Jenkinsfile** to include code formatting checks:

```groovy
stage('Lint Check') {
    steps {
        echo "Running flake8 linter..."
        sh 'pip3 install flake8'
        sh 'flake8 app.py test_app.py'
    }
}
```

### Task 4: Docker Integration

Create a **Dockerfile** to run tests in a container:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app.py .
COPY test_app.py .

CMD ["pytest", "test_app.py", "-v"]
```

Then update Jenkinsfile to build and run the Docker image.

### Task 5: Email Notifications

Add email notifications to Jenkinsfile:

```groovy
post {
    success {
        emailext(
            subject: "Build Successful: ${env.JOB_NAME}",
            body: "Build ${env.BUILD_NUMBER} passed successfully",
            to: "your-email@example.com"
        )
    }
    failure {
        emailext(
            subject: "Build Failed: ${env.JOB_NAME}",
            body: "Build ${env.BUILD_NUMBER} failed. Check console output.",
            to: "your-email@example.com"
        )
    }
}
```

---

## Advanced Enhancements

### Code Coverage Analysis

Add coverage metrics to pipeline:

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### SonarQube Integration

Analyze code quality with SonarQube:

```groovy
stage('SonarQube Analysis') {
    steps {
        sh 'sonar-scanner'
    }
}
```

### Artifact Storage

Archive test reports and coverage:

```groovy
stage('Archive Artifacts') {
    steps {
        archiveArtifacts artifacts: 'dist/**/*', allowEmptyArchive: true
        publishHTML([
            reportDir: 'htmlcov',
            reportFiles: 'index.html',
            reportName: 'Coverage Report'
        ])
    }
}
```

### Automated Deployment

Deploy to production after successful build:

```groovy
stage('Deploy to Production') {
    when {
        branch 'main'
    }
    steps {
        sh 'python3 -m pip install --upgrade .'
        sh 'systemctl restart python-app'
    }
}
```

---

## Complete CI/CD Workflow

```
GitHub Repository
    ↓
Webhook Trigger
    ↓
Jenkins Pipeline
    ├─ Checkout Code
    ├─ Install Dependencies
    ├─ Run Tests
    ├─ Code Quality Check
    ├─ Build Artifacts
    └─ Deploy (Optional)
    ↓
Success/Failure Notification
```

---

## GitHub Webhook Setup (Auto-Trigger Builds)

### Step 1: Add Webhook to GitHub

1. Go to your GitHub repository
2. Settings → Webhooks → Add webhook
3. Fill in:
   - **Payload URL**: `http://YOUR-JENKINS-URL:8080/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: Select "Just the push event"
4. Click **Add webhook**

### Step 2: Enable Webhook in Jenkins Job

1. Go to Jenkins job configuration
2. Check "GitHub hook trigger for GITScm polling"
3. Save

Now every `git push` will automatically trigger a Jenkins build!

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.7+ on Jenkins agent |
| Module not found | Run `pip3 install -r requirements.txt` |
| Tests failing | Check app.py hasn't been modified |
| Jenkins can't clone repo | Add GitHub SSH key to Jenkins user |
| Webhook not triggering | Verify webhook URL and Jenkins is accessible |
| Permission denied | Ensure Jenkins user has file permissions |

---

## Resources

- [Jenkins Pipeline Documentation](https://jenkins.io/doc/book/pipeline/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Webhooks Guide](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Python Best Practices](https://pep8.org/)

---

## Quick Reference Commands

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/python-jenkins-demo.git

# Install dependencies
pip3 install -r requirements.txt

# Run application
python3 app.py

# Run tests
python3 -m pytest test_app.py -v

# Check code quality
flake8 app.py

# Generate coverage
python3 -m pytest --cov=app

# Commit and push
git add .
git commit -m "Your message"
git push origin main
```

---

## Key Learning Outcomes

By completing this project, you will understand:

- How to structure a Python project
- Writing unit tests with pytest
- Code quality checking with flake8
- Jenkins pipeline configuration
- GitHub integration with Jenkins
- CI/CD best practices
- Test coverage measurement
- Artifact archiving and deployment

---

## Next Steps

1. Complete the student assignments
2. Set up GitHub webhooks for auto-triggering
3. Add email notifications
4. Implement Docker containerization
5. Deploy to Kubernetes (advanced)

---

**Happy Learning with Jenkins and Python!**

For questions or issues, refer to the troubleshooting section or consult the official documentation links provided above.
