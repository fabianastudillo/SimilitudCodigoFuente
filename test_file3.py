import math

def calcular_area_circulo(radio):
    """Calcula el área de un círculo."""
    return math.pi * radio ** 2

def calcular_circunferencia(radio):
    """Calcula la circunferencia de un círculo."""
    return 2 * math.pi * radio

class Circulo:
    def __init__(self, radio):
        self.radio = radio
    
    def area(self):
        return calcular_area_circulo(self.radio)
    
    def circunferencia(self):
        return calcular_circunferencia(self.radio)

if __name__ == "__main__":
    circulo = Circulo(5)
    print(f"Área del círculo: {circulo.area():.2f}")
    print(f"Circunferencia: {circulo.circunferencia():.2f}")