pipeline {
    agent {
        dockerfile true
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests inside the Docker container defined by Dockerfile'
                    sh 'pytest waveload/tests/ --junitxml=report.xml --cov=waveload --cov-report=xml=coverage.xml'
                }
            }
        }

        stage('Publish Test Results and Coverage') {
            steps {
                junit 'report.xml'
                publishCoverage issuesFile: 'coverage.xml', publisherName: 'CoverageReport'
            }
        }

        stage('Run Linting') {
            steps {
                script {
                    echo 'Running linting inside the Docker container'
                    sh 'pylint waveload > lint.txt'
                }
            }
        }

        stage('Publish Lint Results') {
            steps {
                // Example: You might need a specific plugin to visualize lint results
                // For now, we can just archive the file.
                archiveArtifacts 'lint.txt'
            }
        }
    }
}
