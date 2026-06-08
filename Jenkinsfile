pipeline {
    agent any
    
    stages {
        stage('Validacion Tipo de Cambio BCRP') {
            steps {
                bat 'python C:\\pipeline_tc\\validar_tc.py'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline finalizado exitosamente - TC validado correctamente'
        }
        failure {
            echo 'Pipeline fallido - Se detecto diferencia en el tipo de cambio'
        }
    }
}