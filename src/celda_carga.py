import time
import sys
from hx711py.hx711 import HX711  # ¡Importamos la nueva biblioteca!
import RPi.GPIO as GPIO  # Usa la biblioteca nativa

class CeldaDeCarga:
    """
    Clase para interactuar con el sensor HX711.
    (VERSIÓN 8.0 - Usando la biblioteca nativa 'hx711py')
    """
    
    def __init__(self, pin_dt, pin_sck):
        """
        Inicializa el sensor HX711.
        :param pin_dt: El número de pin GPIO (BCM) para DT.
        :param pin_sck: El número de pin GPIO (BCM) para SCK.
        """
        try:
            self.hx = HX711(dout_pin=pin_dt, pd_sck_pin=pin_sck)
            
            # Establece el factor de escala (calibration ratio).
            # Esta biblioteca SÍ tiene el método 'set_reference_unit'.
            self.hx.set_reference_unit(1)
            
            print(f"Celda de Carga (DT={pin_dt}, SCK={pin_sck}) inicializada.")
            self.calibrar()

        except Exception as e:
            print(f"Error inicializando CeldaDeCarga (DT={pin_dt}): {e}")
            self.hx = None

    def calibrar(self):
        """
        Realiza la tara (pone la balanza a cero).
        """
        if not self.hx:
            return

        try:
            print(f"Iniciando calibración (tara)...")
            # Esta biblioteca SÍ tiene el método 'tare()'.
            self.hx.tare()
            print("Calibración completada. No pongas peso aún.")
            time.sleep(1)
        except Exception as e:
            print(f"Error durante la calibración: {e}")

    def establecer_factor_escala(self, factor):
        """
        Establece el factor de escala (o 'reference unit').
        """
        if not self.hx:
            return
            
        self.hx.set_reference_unit(factor)
        print(f"Factor de escala establecido en: {factor}")

    def obtener_peso(self):
        """
        Devuelve el peso actual en gramos.
        """
        if not self.hx:
            return 0.0

        try:
            # Esta biblioteca SÍ tiene 'get_weight()'.
            # Promedia 5 lecturas.
            peso = self.hx.get_weight(5)
            
            if peso < 0:
                peso = 0.0
                
            return peso
        except Exception as e:
            print(f"Error al leer el peso: {e}")
            return 0.0

    def obtener_lectura_cruda(self):
        """
        Devuelve el valor 'en crudo' del ADC.
        """
        if not self.hx:
            return 0
        try:
            # Esta biblioteca SÍ tiene 'get_value()'.
            valor = self.hx.get_value(5)
            return valor
        except Exception as e:
            print(f"Error al leer valor en crudo: {e}")
            return 0