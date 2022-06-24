pipeline {
    agent {
        docker {
            image 'latest'
            args '-u root:sudo'
        }
    }
    stages {
      stage('Deploy to Astronomer') {
       when {
        expression {
          return env.GIT_BRANCH == "origin/main"
        }
       }
       steps {
         script {
               sh "curl -sSL install.astronomer.io | sudo bash -s"
               sh 'astro deploy -f'
         }
       }
     }
   }
 post {
   always {
     cleanWs()
   }
  }
}
