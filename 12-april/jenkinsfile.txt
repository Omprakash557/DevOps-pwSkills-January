pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.13'
        GITHUB_REPO = 'https://github.com/Taneshbad/Jenkins_project2.git'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "=========================================="
                echo "Checking out code from GitHub..."
                echo "Repository: https://github.com/Taneshbad/Jenkins_project2.git"
                echo "=========================================="
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/Taneshbad/Jenkins_project2.git']]
                ])
                bat 'git log --oneline -1'
            }
        }
        
        stage('Setup Python') {
            steps {
                echo "=========================================="
                echo "Setting up Python environment..."
                echo "=========================================="
                bat 'python --version'
                bat 'pip --version'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo "=========================================="
                echo "Installing Python dependencies..."
                echo "=========================================="
                bat 'pip install -r requirements.txt'
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo "=========================================="
                echo "Running code quality checks..."
                echo "=========================================="
                bat 'flake8 app.py test_app.py || exit 0'
            }
        }
        
        stage('Run Application') {
            steps {
                echo "=========================================="
                echo "Running the application..."
                echo "=========================================="
                bat 'python app.py'
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "=========================================="
                echo "Running unit tests..."
                echo "=========================================="
                bat 'python -m pytest test_app.py -v --tb=short'
            }
        }
        
        stage('Test Coverage') {
            steps {
                echo "=========================================="
                echo "Generating test coverage report..."
                echo "=========================================="
                bat 'python -m pytest test_app.py --cov=app --cov-report=term-missing || exit 0'
            }
        }
        
        stage('Build Artifacts') {
            steps {
                echo "=========================================="
                echo "Creating build artifacts..."
                echo "=========================================="
            }
        }
    }
    
    post {
        always {
            echo "=========================================="
            echo "Cleaning up workspace..."
            echo "=========================================="
            deleteDir()
        }
        success {
            echo "=========================================="
            echo "BUILD SUCCESSFUL!"
            echo "Repository: https://github.com/Taneshbad/Jenkins_project2.git"
            echo "=========================================="
        }
        failure {
            echo "=========================================="
            echo "BUILD FAILED - Check logs above"
            echo "Repository: https://github.com/Taneshbad/Jenkins_project2.git"
            echo "=========================================="
        }
    }
}
