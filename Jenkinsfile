pipeline {
  agent any
  tools {
      jdk 'jdk8'
      maven 'maven3.5'
  }
  stages {
      stage('test java installation') {
          steps {
              sh 'java -version'               
          }
      }
      stage('test maven installation') {
          steps {
              sh 'mvn -version'           
          }
      }
  }
}

