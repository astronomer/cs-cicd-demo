pipeline {
 agent any
   stages {
     stage('Setup Parameters') {
       steps {
         script {
            properties([
                githubProjectProperty(displayName: '', projectUrlStr: 'https://github.com/astronomer/cs-cicd-demo/'),
                parameters([string(defaultValue: 'BIY7f8hwatpA3B30gGhGfdFqoCK99AmI', name: 'ASTRONOMER_KEY_ID'),
                string(defaultValue: 'fPHG5Yvr9L-NmyCrZqAOEGryLJcgYq2kmRLVaPM4TD7QyPLhO91UXkpnDJLLSXiL', name: 'ASTRONOMER_KEY_SECRET'),
                string(defaultValue: 'cl4sjqwiu179451hvkibsr3knf', name: 'DEPLOYMENT_ID')]),
                pipelineTriggers([githubPush()])
            ])
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