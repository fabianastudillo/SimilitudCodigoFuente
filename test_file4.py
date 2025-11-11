def calcular_potencia(base, exponente):
    """Calcula la potencia de un número."""
    return base ** exponente

def calcular_factorial(n):
    """Calcula el factorial de un número."""
    if n <= 1:
        return 1
    return n * calcular_factorial(n - 1)

class Calculadora:
    def __init__(self):
        self.historial = []
    
    def potencia(self, base, exp):
        resultado = calcular_potencia(base, exp)
        self.historial.append(f"{base}^{exp} = {resultado}")
        return resultado
    
    def factorial(self, n):
        resultado = calcular_factorial(n)
        self.historial.append(f"{n}! = {resultado}")
        return resultado

if __name__ == "__main__":
    calc = Calculadora()
    print(f"2^3 = {calc.potencia(2, 3)}")
    print(f"5! = {calc.factorial(5)}")