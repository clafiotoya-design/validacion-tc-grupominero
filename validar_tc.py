import urllib.request
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuracion de correo
CORREO = "clafiotoya@gmail.com"
PASSWORD_APP = "tndr ovuf aspj xebd"

print("==============================================")
print("  GRUPO MINERO SAC - Validacion Tipo de Cambio")
print("==============================================")
print(f"  Fecha de ejecucion: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("----------------------------------------------")

# Leer tipo de cambio del sistema
print("\n[PASO 1] Leyendo tipo de cambio del sistema...")
ruta = r"C:\pipeline_tc\tipo_cambio_sistema.txt"
with open(ruta, "r") as f:
    tc_sistema = float(f.read().strip())
print(f"  TC ingresado en sistema: S/ {tc_sistema}")

# Consultar BCRP
print("\n[PASO 2] Consultando tipo de cambio oficial BCRP...")
url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04640PD/json"
req = urllib.request.urlopen(url, timeout=10)
data = json.loads(req.read().decode())
tc_bcrp = float(data["periods"][0]["values"][0])
print(f"  TC oficial BCRP: S/ {tc_bcrp}")

# Comparar
print("\n[PASO 3] Comparando valores...")
diferencia = abs(tc_sistema - tc_bcrp)
print(f"  Diferencia: S/ {round(diferencia, 4)}")

if diferencia <= 0.015:
    resultado = "OK"
    mensaje = f"Validacion exitosa. TC sistema S/ {tc_sistema} coincide con BCRP S/ {tc_bcrp}."
    print("\n  RESULTADO: OK - Tipo de cambio validado correctamente")
else:
    resultado = "ALERTA"
    mensaje = f"ALERTA: TC sistema S/ {tc_sistema} difiere del BCRP S/ {tc_bcrp}. Diferencia: S/ {round(diferencia,4)}."
    print("\n  RESULTADO: ALERTA - Diferencia supera el umbral permitido")

# Enviar correo
print("\n[PASO 4] Enviando notificacion por correo...")
try:
    msg = MIMEMultipart()
    msg["From"] = CORREO
    msg["To"] = CORREO
    msg["Subject"] = f"Grupo Minero SAC - Validacion TC {datetime.now().strftime('%d/%m/%Y')} - {resultado}"
    
    cuerpo = f"""
    GRUPO MINERO SAC
    Validacion Tipo de Cambio - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    
    TC ingresado en sistema: S/ {tc_sistema}
    TC oficial BCRP:         S/ {tc_bcrp}
    Diferencia:              S/ {round(diferencia, 4)}
    
    RESULTADO: {resultado}
    {mensaje}
    """
    
    msg.attach(MIMEText(cuerpo, "plain"))
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(CORREO, PASSWORD_APP)
    servidor.sendmail(CORREO, CORREO, msg.as_string())
    servidor.quit()
    print("  Correo enviado exitosamente a clafiotoya@gmail.com")
except Exception as e:
    print(f"  Error al enviar correo: {e}")

print("\n==============================================")
print("  Proceso finalizado")
print("==============================================")

if resultado == "ALERTA":
    raise Exception(mensaje)
