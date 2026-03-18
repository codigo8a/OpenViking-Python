# Descripción: Este skill saluda al usuario y muestra la fecha y hora actual de forma épica.
import datetime

def run():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🏴‍☠️ ¡Saludos, Guerrero de OpenViking! La arena de batalla marca las: {now}")

if __name__ == "__main__":
    run()
