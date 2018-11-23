def scmVars = checkout scm
def branchName = scmVars.GIT_BRANCH

pipeline {
    agent any
    tools {
        maven 'Maven 3.3.9'
        jdk 'jdk8'
    }
    stages {
        stage ('Initialize') {
            steps {
                sh '''
                    echo "PATH = ${PATH}"
                    echo "M2_HOME = ${M2_HOME}"
                '''
            }
        }

        stage ('Build') {
            steps {
                sh 'mvn -Dmaven.test.failure.ignore=true clean install' 
            }
        }
        
        stage ('Deploy'){
            steps {
                deploy("target/MBP-0.1.war", "localhost", "/${branchName}")
            }
        }
    }
}

def deploy(file, host, context) {
    sh "curl -v -u deployer:deployer -T ${file} 'http://${host}:8888/manager/text/deploy?path=${context}&update=true'"
}
