pipeline {
 agent any
   stages {
     stage('Setup Parameters') {
       steps {
         script {
            properties([
                githubProjectProperty(displayName: '', projectUrlStr: 'https://github.com/astronomer/cs-cicd-demo/'),
                parameters([
                    string(defaultValue: 'FcCRwQxXowv3prv5leFV7ZrBwvMuz42Q', name: 'ASTRONOMER_KEY_ID'),
                    string(defaultValue: 'r0yAWAikagc0_U1E5WJD8P1_BTGdO_mgRENK0LLTIpWzo9_lGVt1TcRMDWY9NIv4', name: 'ASTRONOMER_KEY_SECRET'),
                    string(defaultValue: 'cl4xce7dx500201bzlxbveud5c', name: 'DEPLOYMENT_ID')
                ]),
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