import time
import board
import sys
from celda_carga import CeldaDeCarga  # Importamos la clase que acabamos de crear

# --- CONFIGURACIÓN ---
# ¡IMPORTANTE! Cambia estos pines a los que conectaste tu PRIMERA celda.
# Usamos la sugerencia de la sección 1.
PINES_CELDA_1_DT = board.D17
PINES_CELDA_1_SCK = board.D27

print("\n--- Herramienta de Calibración de Celdas de Carga (HX711) ---")

# 1. Inicializar la celda
try:
    print(f"Inicializando celda en DT={PINES_CELDA_1_DT} y SCK={PINES_CELDA_1_SCK}...")
    celda = CeldaDeCarga(pin_dt=PINES_CELDA_1_DT, pin_sck=PINES_CELDA_1_SCK)
    print("Celda inicializada con éxito.")
except Exception as e:
    print(f"\n[ERROR FATAL] No se pudo inicializar la celda.")
    print(f"Detalle: {e}")
    print("Verifica las conexiones y que los pines D5/D6 estén correctos.")
    sys.exit()

# 2. Proceso de Tara (Calibración a Cero)
print("\n--- PASO 1: CALIBRACIÓN (TARA) ---")
print("¡IMPORTANTE! Asegúrate de que no haya NADA de peso sobre la celda.")
input("Presiona ENTER cuando estés listo para poner la balanza a cero...")

celda.calibrar()

print("Tara completada. La lectura actual debería ser ~0.")
print(f"Lectura en crudo actual: {celda.obtener_lectura_cruda()}")

# 3. Proceso de Medición de Factor
print("\n--- PASO 2: ENCONTRAR EL FACTOR DE ESCALA ---")
print("¡IMPORTANTE! Coloca un objeto de PESO CONOCIDO sobre la celda.")
print("(ej. un paquete de arroz de 1kg = 1000g, una lata de refresco = 355g, etc.)")

peso_conocido_str = ""
while not peso_conocido_str.isdigit():
    peso_conocido_str = input("\nEscribe el peso conocido en GRAMOS (ej. 1000) y presiona ENTER: ")

peso_conocido = float(peso_conocido_str)
if peso_conocido <= 0:
    print("El peso debe ser mayor a 0.")
    sys.exit()

print(f"Tomando lectura con {peso_conocido}g. Por favor espera...")
time.sleep(2) # Dar tiempo a que se estabilice

lectura_cruda = celda.obtener_lectura_cruda()
print(f"Lectura en crudo obtenida: {lectura_cruda}")

# 4. Cálculo
try:
    factor_de_escala = lectura_cruda / peso_conocido
    print("\n--- ¡CÁLCULO COMPLETADO! ---")
    print(f"Tu FACTOR DE ESCALA (Reference Unit) es: {factor_de_escala}")
    print("\n¡GUARDA ESTE NÚMERO! Lo necesitarás en tu script 'main.py'.\n")

    # 5. Verificación
    print("--- PASO 3: VERIFICACIÓN ---")
    print(f"Aplicando el factor {factor_de_escala} a la celda...")
    celda.establecer_factor_escala(factor_de_escala)

    print("\nAhora mostraré el peso medido en tiempo real.")
    print("Verifica que la lectura sea cercana a los gramos que pusiste.")
    print("Presiona Ctrl+C para salir.")
    
    while True:
        peso_medido = celda.obtener_peso()
        print(f"  Peso medido: {peso_medido:.2f} g")
        time.sleep(0.5)

except ZeroDivisionError:
    print("[ERROR] La lectura en crudo fue 0. No se puede dividir por 0.")
    print("Asegúrate de que la celda esté bien conectada.")
except KeyboardInterrupt:
    print("\n\nCerrando script de calibración. ¡Adiós!")
except Exception as e:
    print(f"\nOcurrió un error: {e}")