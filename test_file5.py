import random

def generar_numeros_aleatorios(cantidad):
    """Genera una lista de números aleatorios."""
    return [random.randint(1, 100) for _ in range(cantidad)]

def ordenar_lista(lista):
    """Ordena una lista de números."""
    return sorted(lista)

class GestorNumeros:
    def __init__(self):
        self.numeros = []
    
    def agregar_aleatorios(self, cantidad):
        nuevos = generar_numeros_aleatorios(cantidad)
        self.numeros.extend(nuevos)
        return nuevos
    
    def obtener_ordenados(self):
        return ordenar_lista(self.numeros)

def main():
    gestor = GestorNumeros()
    gestor.agregar_aleatorios(5)
    print("Números ordenados:", gestor.obtener_ordenados())

if __name__ == "__main__":
    main()