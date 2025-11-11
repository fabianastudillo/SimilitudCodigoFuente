def area_rectangulo(longitud, anchura):
    """Función para calcular área de rectágulo."""
    resultado = longitud * anchura
    return resultado

def perimetro_rectangulo(longitud, anchura):
    """Función para calcular perímetro de rectángulo.""" 
    resultado = 2 * (longitud + anchura)
    return resultado

class FiguraRectangular:
    def __init__(self, longitud, anchura):
        self.longitud = longitud
        self.anchura = anchura
    
    def obtener_area(self):
        return area_rectangulo(self.longitud, self.anchura)
    
    def obtener_perimetro(self):
        return perimetro_rectangulo(self.longitud, self.anchura)

def main():
    figura = FiguraRectangular(5, 3)
    print(f"El área es: {figura.obtener_area()}")
    print(f"El perímetro es: {figura.obtener_perimetro()}")

if __name__ == "__main__":
    main()