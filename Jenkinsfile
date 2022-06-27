pipeline {
 agent any
   stages {
     stage('Deploy to Astronomer') {
       when {
        expression {
          return env.GIT_BRANCH == "origin/main"
        }
       }
       steps {
         script {
           sh 'curl -sSL install.astronomer.io |  bash -s -b /usr/local/bin
           sh 'tar xzf astro_1.1.0_linux_arm64.tar.gz'
           sh "./astro deploy ${DEPLOYMENT_ID} -f"
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
