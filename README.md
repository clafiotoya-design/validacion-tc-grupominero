# Validacion TC - Grupo Minero SAC

## Descripcion
Pipeline automatizado para validar el tipo de cambio diario 
ingresado en el ERP contra el tipo de cambio oficial del BCRP.

## Archivos
- **validar_tc.py** — script Python que realiza la validacion
- **Jenkinsfile** — define el pipeline en Jenkins

## Ramas
- **main** — codigo estable en produccion
- **desarrollo** — rama para nuevos cambios
- **hotfix** — rama para correcciones urgentes

## Funcionamiento
1. Lee el TC ingresado en el sistema
2. Consulta el TC oficial del BCRP en tiempo real
3. Compara ambos valores
4. Envia alerta por correo si hay diferencia mayor al umbral

## Tecnologias
- Python 3
- Jenkins
- GitHub
- API BCRP
