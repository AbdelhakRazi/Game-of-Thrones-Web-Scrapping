pipeline {
    agent any //where to execute
    stages {// where the work happens
        stage('build') {
            steps {
                echo 'building python application'
            }
        }
         stage('test') {
            steps {
                echo 'testing python application'
            }
        }
         stage('deploy') {
            steps {
                echo 'deploying python application'
            }
        }
    }
}
