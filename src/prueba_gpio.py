import time
import board
import digitalio  # Esta es la biblioteca base que usa 'adafruit_hx711'
import sys

# Los mismos pines que usamos antes
PIN_DT = board.D27   # GPIO 27 (Pin 13)
PIN_SCK = board.D17  # GPIO 17 (Pin 11)

print("--- Prueba de GPIO de bajo nivel (Blinka) ---")
print(f"Configurando SCK (D17) como SALIDA (OUTPUT)")
print(f"Configurando DT (D27) como ENTRADA (INPUT)")

try:
    # Configura el pin de Clock (SCK) como salida
    pin_sck = digitalio.DigitalInOut(PIN_SCK)
    pin_sck.direction = digitalio.Direction.OUTPUT

    # Configura el pin de Data (DT) como entrada
    pin_dt = digitalio.DigitalInOut(PIN_DT)
    pin_dt.direction = digitalio.Direction.INPUT

    # El pin DT (Data) del HX711 debe estar en 'alto' (True)
    # cuando está inactivo. Habilitamos un 'pull-up' interno
    # en la Pi para ayudar a estabilizar esta señal.
    pin_dt.pull = digitalio.Pull.UP 

    print("Pines configurados. Iniciando bucle de lectura...")
    print("Presiona Ctrl+C para salir.")

    while True:
        # Leemos el valor del pin de datos.
        # Cuando el HX711 está listo, pone este pin en 'bajo' (False).
        # Si está inactivo, debería estar en 'alto' (True)
        print(f"Valor del pin DT (D27): {pin_dt.value}")

        # Simplemente movemos el pin de clock para ver que funciona
        pin_sck.value = True
        time.sleep(0.5)
        pin_sck.value = False
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nPrueba detenida.")
except Exception as e:
    print(f"\n[ERROR FATAL] Falló la configuración de GPIO: {e}")
    print("Esto sugiere un problema con 'adafruit-blinka',")
    print("la configuración de tu Pi, o permisos.")
    print("Intenta ejecutar de nuevo con 'sudo python prueba_gpio.py'.")
    sys.exit()