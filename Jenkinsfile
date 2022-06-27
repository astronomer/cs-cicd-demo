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
           sh 'curl -LJO https://github.com/astronomer/astro-cli/releases/download/v1.1.0/astro_1.1.0_linux_amd64.tar.gz'
           sh 'tar xzf astro_1.1.0_linux_amd64.tar.gz'
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
