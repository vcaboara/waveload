pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image'
                    sh 'docker build -t waveload-app .'
                }
            }
        }

        stage('Run Tests in Docker') {
            steps {
                script {
                    echo 'Running tests inside Docker container'
                    sh 'docker run --rm -v "$(pwd)/waveload:/app/waveload" waveload-app pytest /app/waveload/tests/'
                }
            }
        }
        /*
        stage('Set Up Environment') {
            steps {
                script {
                    echo 'Setting up Python environment'
                    sh 'python3 -m venv venv'
                    sh 'source venv/bin/activate'
                    sh 'pip install --upgrade pip'
                    sh 'pip install -r requirements.txt' # If you have a requirements.txt
                    sh 'pip install pytest pytest-cov'
                    sh 'pip install -e .'
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo 'Building the project'
                    sh 'source venv/bin/activate'
                    sh 'python3 -m build'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests with pytest'
                    sh 'source venv/bin/activate'
                    sh 'pytest waveload/tests/'
                }
            }
        }

        stage('Code Coverage') {
            steps {
                script {
                    echo 'Generating code coverage report'
                    sh 'source venv/bin/activate'
                    sh 'pytest --cov=waveload --cov-report=xml'
                    publishCoverage issuesFile: 'cobertura.xml', publisherName: 'CoverageReport'
                }
            }
        }
        */
    }

    post {
        always {
            cleanWorkspace()
        }
    }
}
