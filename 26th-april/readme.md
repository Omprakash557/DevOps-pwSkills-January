# SonarQube Setup & Configuration Guide

## Table of Contents

- [macOS Installation](#macos-installation)
- [Windows Installation](#windows-installation)
- [Sample Code](#sample-code)
- [Test Code](#test-code)
- [Configuration File](#configuration-file)
- [Running SonarQube Analysis](#running-sonarqube-analysis)

---

## macOS Installation

### Step 1: Download Community Edition

1. Visit: [SonarQube Downloads](https://www.sonarsource.com/products/sonarqube/downloads/)
2. Download the latest Community Edition

### Step 2: Install SonarScanner

```bash
brew install sonar-scanner
```

### Step 3: Start SonarQube Server

Navigate to the extracted SonarQube directory:

```bash
cd sonarqube-x.x.x/bin/macosx-universal-64
./sonar.sh start
```

### Step 4: Access SonarQube UI

Open in browser:

```
http://localhost:9000
```

**Default Login Credentials:**
- Username: `admin`
- Password: `admin`

---

## Windows Installation

### Step 1: Download Community Edition

1. Visit: [SonarQube Downloads](https://www.sonarsource.com/products/sonarqube/downloads/)
2. Download the Community Edition for Windows

### Step 2: Download SonarScanner

1. Visit: [SonarScanner Documentation](https://docs.sonarsource.com/sonarqube-server/10.8/analyzing-source-code/scanners/sonarscanner)
2. Download **Windows x64** version
3. Extract to a folder (e.g., `C:\sonar-scanner`)

### Step 3: Add SonarScanner to PATH

1. Open **Environment Variables**
2. Add `C:\sonar-scanner\bin` to your System PATH

### Step 4: Start SonarQube Server

Navigate to the SonarQube bin folder:

```cmd
cd sonarqube-x.x.x\bin\windows-x86-64
StartSonar.bat
```

### Step 5: Check Server Logs

Monitor the console output for:
- `SonarQube is up`
- Server startup confirmation

### Step 6: Access SonarQube UI

Open in browser:

```
http://localhost:9000
```

**Default Login Credentials:**
- Username: `admin`
- Password: `admin`

---

## Sample Code

Create a file named `app.py`:

```python
"""
Simple Calculator Module
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """
    Divide a by b
    
    Args:
        a: Dividend
        b: Divisor
    
    Returns:
        Result of division
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

---

## Test Code

Create a file named `test_app.py`:

```python
"""
Test suite for Calculator Module
"""

import pytest
from app import add, subtract, multiply, divide

class TestBasicOperations:
    """Test basic arithmetic operations"""
    
    def test_add(self):
        """Test addition operation"""
        assert add(10, 5) == 15
        assert add(0, 0) == 0
        assert add(-5, 5) == 0
    
    def test_subtract(self):
        """Test subtraction operation"""
        assert subtract(10, 5) == 5
        assert subtract(5, 5) == 0
        assert subtract(0, 5) == -5
    
    def test_multiply(self):
        """Test multiplication operation"""
        assert multiply(10, 5) == 50
        assert multiply(0, 5) == 0
        assert multiply(-5, 2) == -10
    
    def test_divide(self):
        """Test division operation"""
        assert divide(10, 5) == 2
        assert divide(10, 2) == 5
        assert divide(5, 1) == 5
    
    def test_divide_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)
    
    def test_divide_negative(self):
        """Test division with negative numbers"""
        assert divide(-10, 2) == -5
        assert divide(10, -2) == -5
```

---

## Configuration File

Create a file named `sonar-project.properties`:

```properties
# =============================================================================
# SonarQube Configuration for Python Project
# =============================================================================

# Unique identifier for your project (required)
sonar.projectKey=Bandiya

# Display name of your project
sonar.projectName=Bandiya

# Project version
sonar.projectVersion=1.0

# Source code location
sonar.sources=.

# Programming language
sonar.language=py

# Test file inclusions
sonar.tests=.
sonar.test.inclusions=**/test_*.py

# Exclude directories from analysis
sonar.exclusions=**/__pycache__/**,**/venv/**,.git/**

# SonarQube server location (URL)
sonar.host.url=http://localhost:9000

# Authentication token
# Generate from: SonarQube UI → My Account → Security → Generate Tokens
sonar.token=sqp_a77fa37b7d3562635f1e9ed010f71dfdcda1d361

# Optional: Coverage report path
# sonar.python.coverage.reportPaths=coverage.xml

# Optional: Test execution report
# sonar.python.xunit.reportPath=test-results.xml
```

### How to Generate Token

1. Open SonarQube: `http://localhost:9000`
2. Click **My Account** (top-right)
3. Select **Security** tab
4. Click **Generate Tokens**
5. Enter token name (e.g., "local-scanner")
6. Copy the generated token
7. Replace `sonar.token` value in configuration file

---

## Running SonarQube Analysis

### Prerequisites

Before running analysis, ensure:

1. ✅ SonarQube server is running
2. ✅ SonarScanner is installed
3. ✅ `sonar-project.properties` file exists
4. ✅ `app.py` and `test_app.py` exist
5. ✅ Token is configured

### Step 1: Install Dependencies

```bash
pip install pytest
```

### Step 2: Run Tests

```bash
pytest test_app.py -v
```

**Expected Output:**
```
test_app.py::TestBasicOperations::test_add PASSED
test_app.py::TestBasicOperations::test_subtract PASSED
test_app.py::TestBasicOperations::test_multiply PASSED
test_app.py::TestBasicOperations::test_divide PASSED
test_app.py::TestBasicOperations::test_divide_by_zero PASSED
test_app.py::TestBasicOperations::test_divide_negative PASSED

====== 6 passed in 0.15s ======
```

### Step 3: Run SonarQube Analysis

**macOS/Linux:**

```bash
sonar-scanner \
  -Dsonar.projectKey=Bandiya \
  -Dsonar.projectName="Bandiya" \
  -Dsonar.projectVersion=1.0 \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqp_a77fa37b7d3562635f1e9ed010f71dfdcda1d361
```

**Windows (Command Prompt):**

```cmd
sonar-scanner ^
  -Dsonar.projectKey=Bandiya ^
  -Dsonar.projectName="Bandiya" ^
  -Dsonar.projectVersion=1.0 ^
  -Dsonar.sources=. ^
  -Dsonar.host.url=http://localhost:9000 ^
  -Dsonar.token=sqp_a77fa37b7d3562635f1e9ed010f71dfdcda1d361
```

**Using Configuration File:**

If you have `sonar-project.properties` configured:

```bash
sonar-scanner
```

### Step 4: View Results

Open in browser:

```
http://localhost:9000
```

Navigate to project **Bandiya** to see analysis results.

---

## Project File Structure

```
project-root/
├── app.py                           # Application code
├── test_app.py                      # Test code
├── sonar-project.properties         # SonarQube configuration
└── README.md                        # Documentation
```

---

## Expected SonarQube Results

After running analysis, you should see:

| Metric | Expected |
|--------|----------|
| Coverage | High % |
| Code Smells | Low |
| Bugs | 0 |
| Vulnerabilities | 0 |
| Duplications | Low |

---

## Troubleshooting

### Issue: SonarQube Server Not Starting

**Solution:**
- Ensure Java 11+ is installed
- Check port 9000 is not in use
- Review logs in `sonarqube-x.x.x/logs/`

### Issue: SonarScanner Command Not Found

**Windows:**
- Verify `C:\sonar-scanner\bin` is in PATH
- Restart command prompt

**macOS/Linux:**
- Run `brew install sonar-scanner`
- Verify with `sonar-scanner --version`

### Issue: Authentication Failed

**Solution:**
- Verify token is correct
- Generate new token from SonarQube UI
- Ensure SonarQube server is running

### Issue: No Code Coverage

**Solution:**
- Install coverage: `pip install pytest-cov coverage`
- Generate coverage reports
- Configure coverage path in `sonar-project.properties`

---

## Quick Reference Commands

### macOS

```bash
# Start SonarQube
cd sonarqube-x.x.x/bin/macosx-universal-64
./sonar.sh start

# Run tests
pytest test_app.py -v

# Run analysis
sonar-scanner
```

### Windows

```cmd
# Start SonarQube
cd sonarqube-x.x.x\bin\windows-x86-64
StartSonar.bat

# Run tests
pytest test_app.py -v

# Run analysis
sonar-scanner
```

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Download & Install SonarQube | 5 min |
| 2 | Install SonarScanner | 2 min |
| 3 | Start SonarQube Server | 1 min |
| 4 | Create Code & Tests | 5 min |
| 5 | Create Configuration | 2 min |
| 6 | Generate Token | 2 min |
| 7 | Run Analysis | 2 min |
| 8 | View Results | 1 min |
| **TOTAL** | **Complete Setup** | **~20 min** |

---

## Next Steps

1.  Follow installation steps for your OS
2.  Create `app.py` with sample code
3.  Create `test_app.py` with tests
4.  Create `sonar-project.properties`
5.  Generate SonarQube token
6.  Run analysis
7.  View results in dashboard

---

## Useful Links

- [SonarQube Official Downloads](https://www.sonarsource.com/products/sonarqube/downloads/)
- [SonarScanner Documentation](https://docs.sonarsource.com/sonarqube-server/10.8/analyzing-source-code/scanners/sonarscanner)
- [SonarQube Community Edition](https://www.sonarsource.com/products/sonarqube/)
- [Python Analysis in SonarQube](https://docs.sonarsource.com/sonarqube-server/10.8/analyzing-source-code/languages/python/)

---

**Happy Analyzing!** 
