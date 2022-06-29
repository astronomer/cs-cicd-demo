pipeline {
 agent any
   stages {
     stage('Set Environment Variables') {
        steps {
            script {
                env.ASTRONOMER_KEY_ID = params.ASTRONOMER_KEY_ID
                env.ASTRONOMER_KEY_SECRET = params.ASTRONOMER_KEY_SECRET
                env.DEPLOYMENT_ID = params.DEPLOYMENT_ID
            }
        }
     }
     stage('Deploy to Astronomer') {
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