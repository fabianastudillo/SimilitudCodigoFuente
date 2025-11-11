def calcular_area_rectangulo(largo, ancho):
    """Calcula el área de un rectángulo."""
    return largo * ancho

def calcular_perimetro_rectangulo(largo, ancho):
    """Calcula el perímetro de un rectángulo."""
    return 2 * (largo + ancho)

class Rectangulo:
    def __init__(self, largo, ancho):
        self.largo = largo
        self.ancho = ancho
    
    def area(self):
        return calcular_area_rectangulo(self.largo, self.ancho)
    
    def perimetro(self):
        return calcular_perimetro_rectangulo(self.largo, self.ancho)

if __name__ == "__main__":
    rect = Rectangulo(5, 3)
    print(f"Área: {rect.area()}")
    print(f"Perímetro: {rect.perimetro()}")