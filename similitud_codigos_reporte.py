#!/usr/bin/env python3
"""
Analizador de Similitud de Códigos Fuente v2.0

Herramienta para análisis comparativo de códigos fuente utilizando métricas
de similitud validadas científicamente: Similitud del Coseno, Índice de Jaccard
y Distancia de Levenshtein normalizada.

Referencias principales:
    - Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for 
      automatic indexing. Communications of the ACM, 18(11), 613-620.
    - Jaccard, P. (1912). The distribution of the flora in the alpine zone.
      New Phytologist, 11(2), 37-50.
    - Levenshtein, V. I. (1966). Binary codes capable of correcting deletions,
      insertions, and reversals. Soviet Physics Doklady, 10(8), 707-710.

Aplicaciones validadas en literatura de ingeniería de software:
    - Bellon, S., et al. (2007). Comparison and evaluation of clone detection 
      tools. IEEE Transactions on Software Engineering, 33(9), 577-591.
    - Roy, C. K., et al. (2009). Comparison and evaluation of code clone 
      detection techniques and tools. Science of Computer Programming, 74(7), 470-495.

Autor: GitHub Copilot
Licencia: MIT
Fecha: Noviembre 2025
"""

import sys
import math
import re
import csv
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter
from itertools import combinations
from datetime import datetime
import subprocess

# ======================================
# 🔹 Limpieza y tokenización del código
# ======================================

# Palabras clave importantes para preservar la semántica
PYTHON_KEYWORDS = {
    'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 
    'finally', 'with', 'import', 'from', 'return', 'yield', 'break', 
    'continue', 'pass', 'and', 'or', 'not', 'in', 'is', 'lambda'
}

def detectar_lenguaje(nombre_archivo: str) -> str:
    """Detecta el lenguaje de programación basado en la extensión."""
    ext = Path(nombre_archivo).suffix.lower()
    lenguajes = {
        '.py': 'python',
        '.js': 'javascript', 
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp'
    }
    return lenguajes.get(ext, 'unknown')

def limpiar_codigo(texto: str, lenguaje: str = 'python') -> List[str]:
    """
    Limpia el código eliminando comentarios, espacios y docstrings.
    Retorna lista de tokens normalizados preservando palabras clave.
    
    Args:
        texto: Código fuente a limpiar
        lenguaje: Lenguaje de programación ('python', 'javascript', etc.)
    
    Returns:
        Lista de tokens normalizados
    """
    if not texto.strip():
        return []
    
    try:
        # Limpiar según el lenguaje
        if lenguaje == 'python':
            # Eliminar docstrings y comentarios de Python
            texto = re.sub(r'"""[\s\S]*?"""', '', texto)
            texto = re.sub(r"'''[\s\S]*?'''", '', texto)
            texto = re.sub(r'#.*', '', texto)
        elif lenguaje in ['javascript', 'java', 'cpp', 'c', 'csharp']:
            # Eliminar comentarios de C-style
            texto = re.sub(r'/\*[\s\S]*?\*/', '', texto)
            texto = re.sub(r'//.*', '', texto)
        
        # Eliminar strings literales pero preservar su presencia
        texto = re.sub(r'"[^"]*"', 'STRING_LITERAL', texto)
        texto = re.sub(r"'[^']*'", 'STRING_LITERAL', texto)
        
        # Normalizar espacios
        texto = re.sub(r'\s+', ' ', texto.strip())
        
        # Tokenización mejorada
        tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|\d+|[=+\-*/<>:.,(){}[\];]', texto)
        
        # Filtrar tokens vacíos y normalizar
        tokens_limpios = []
        for token in tokens:
            if token and len(token.strip()) > 0:
                # Preservar palabras clave importantes
                if token.lower() in PYTHON_KEYWORDS:
                    tokens_limpios.append(f"KEYWORD_{token.upper()}")
                else:
                    tokens_limpios.append(token.lower())
        
        return tokens_limpios
        
    except Exception as e:
        print(f"⚠️  Error al limpiar código: {e}")
        return []


# ======================================
# 🔹 Índice 1: Cosine Similarity
# ======================================
def similitud_coseno(tokens1: List[str], tokens2: List[str]) -> float:
    """
    Calcula la similitud del coseno entre dos listas de tokens.
    
    La similitud del coseno mide el ángulo entre dos vectores de frecuencia
    de tokens, ignorando la magnitud (longitud del documento).
    
    Basado en el modelo de espacio vectorial propuesto por Salton et al. (1975)
    para recuperación de información automática.
    
    Referencias:
        Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for 
        automatic indexing. Communications of the ACM, 18(11), 613-620.
    
    Args:
        tokens1: Lista de tokens del primer código
        tokens2: Lista de tokens del segundo código
    
    Returns:
        float: Similitud entre 0.0 (completamente diferentes) y 1.0 (idénticos)
    """
    if not tokens1 or not tokens2:
        return 0.0
    
    c1, c2 = Counter(tokens1), Counter(tokens2)
    inter = set(c1.keys()) & set(c2.keys())
    
    if not inter:
        return 0.0
    
    num = sum(c1[x] * c2[x] for x in inter)
    den1 = math.sqrt(sum(v**2 for v in c1.values()))
    den2 = math.sqrt(sum(v**2 for v in c2.values()))
    den = den1 * den2
    
    return num / den if den else 0.0


# ======================================
# 🔹 Índice 2: Jaccard Similarity
# ======================================
def similitud_jaccard(tokens1: List[str], tokens2: List[str]) -> float:
    """
    Calcula el índice de Jaccard entre dos listas de tokens.
    
    El índice de Jaccard mide la similitud como el tamaño de la intersección
    dividido por el tamaño de la unión de los conjuntos.
    
    Originalmente desarrollado por Paul Jaccard (1912) para estudios botánicos,
    ampliamente adoptado en ciencias de la computación para análisis de similitud.
    
    Referencias:
        Jaccard, P. (1912). The distribution of the flora in the alpine zone.
        New Phytologist, 11(2), 37-50.
    
    Args:
        tokens1: Lista de tokens del primer código
        tokens2: Lista de tokens del segundo código
    
    Returns:
        float: Similitud entre 0.0 (sin elementos comunes) y 1.0 (idénticos)
    """
    if not tokens1 or not tokens2:
        return 0.0
    
    set1, set2 = set(tokens1), set(tokens2)
    inter = len(set1 & set2)
    union = len(set1 | set2)
    
    return inter / union if union else 0.0


# ======================================
# 🔹 Índice 3: Levenshtein Ratio (Optimizado)
# ======================================
def distancia_levenshtein(a: str, b: str) -> int:
    """
    Calcula la distancia de edición (Levenshtein) entre dos cadenas.
    
    Implementación optimizada que usa solo O(min(len(a), len(b))) memoria
    en lugar de O(len(a) * len(b)).
    
    Algoritmo propuesto por Vladimir Levenshtein (1966) para corrección de errores
    en códigos binarios, con optimización de Wagner & Fischer (1974).
    
    Referencias:
        Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, 
        insertions, and reversals. Soviet Physics Doklady, 10(8), 707-710.
        
        Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction 
        problem. Journal of the ACM, 21(1), 168-173.
    
    Args:
        a: Primera cadena
        b: Segunda cadena
    
    Returns:
        int: Número mínimo de operaciones (inserción, eliminación, sustitución)
             necesarias para transformar 'a' en 'b'
    """
    if len(a) < len(b):
        return distancia_levenshtein(b, a)
    
    if len(b) == 0:
        return len(a)
    
    # Usar solo dos filas para optimizar memoria
    prev_row = list(range(len(b) + 1))
    
    for i, ca in enumerate(a):
        curr_row = [i + 1]
        for j, cb in enumerate(b):
            # Costo de inserción, eliminación y sustitución
            insert_cost = prev_row[j + 1] + 1
            delete_cost = curr_row[j] + 1  
            substitute_cost = prev_row[j] + (0 if ca == cb else 1)
            
            curr_row.append(min(insert_cost, delete_cost, substitute_cost))
        
        prev_row = curr_row
    
    return prev_row[-1]


def ratio_levenshtein(texto1: str, texto2: str) -> float:
    """
    Convierte la distancia de Levenshtein en un índice de similitud normalizado.
    
    Args:
        texto1: Primera cadena de texto
        texto2: Segunda cadena de texto
    
    Returns:
        float: Similitud entre 0.0 (completamente diferentes) y 1.0 (idénticos)
    """
    if not texto1 and not texto2:
        return 1.0
    
    if not texto1 or not texto2:
        return 0.0
    
    dist = distancia_levenshtein(texto1, texto2)
    max_len = max(len(texto1), len(texto2))
    
    return 1.0 - (dist / max_len) if max_len > 0 else 0.0


# ======================================
# 🔹 Comparación entre archivos (Mejorado)
# ======================================

def validar_archivo(nombre_archivo: str) -> Tuple[bool, str]:
    """
    Valida si un archivo existe, es legible y contiene código.
    
    Args:
        nombre_archivo: Ruta del archivo a validar
    
    Returns:
        Tuple[bool, str]: (es_válido, mensaje_error)
    """
    try:
        if not os.path.exists(nombre_archivo):
            return False, f"Archivo no encontrado: {nombre_archivo}"
        
        if not os.path.isfile(nombre_archivo):
            return False, f"No es un archivo: {nombre_archivo}"
        
        # Verificar que sea un archivo de código fuente
        extensiones_validas = {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go'}
        if Path(nombre_archivo).suffix.lower() not in extensiones_validas:
            return False, f"Extensión no soportada: {nombre_archivo}"
        
        # Intentar leer el archivo
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if not contenido.strip():
                return False, f"Archivo vacío: {nombre_archivo}"
        
        return True, "OK"
        
    except (IOError, UnicodeDecodeError, PermissionError) as e:
        return False, f"Error leyendo {nombre_archivo}: {str(e)}"


def generar_estadisticas(resultados: List[List]) -> Dict[str, float]:
    """
    Genera estadísticas resumen de los resultados de similitud.
    
    Args:
        resultados: Lista de resultados [archivo_a, archivo_b, cosine, jaccard, levenshtein]
    
    Returns:
        Dict con estadísticas (promedio, máximo, mínimo por métrica)
    """
    if not resultados:
        return {}
    
    cosines = [r[2] for r in resultados]
    jaccards = [r[3] for r in resultados]
    levenshteins = [r[4] for r in resultados]
    
    return {
        'cosine_promedio': sum(cosines) / len(cosines),
        'cosine_max': max(cosines),
        'cosine_min': min(cosines),
        'jaccard_promedio': sum(jaccards) / len(jaccards),
        'jaccard_max': max(jaccards),
        'jaccard_min': min(jaccards),
        'levenshtein_promedio': sum(levenshteins) / len(levenshteins),
        'levenshtein_max': max(levenshteins),
        'levenshtein_min': min(levenshteins),
        'total_comparaciones': len(resultados)
    }


def generar_matriz_similitud(f, resultados: List[List], archivos_procesados: List[str], 
                           metrica: str = 'coseno') -> None:
    """
    Genera una matriz de similitud en formato Markdown.
    
    Args:
        f: Archivo donde escribir
        resultados: Lista de resultados de comparación
        archivos_procesados: Lista de archivos procesados
        metrica: Métrica a mostrar ('coseno', 'jaccard', 'levenshtein')
    """
    # Crear diccionario de similitudes para acceso rápido
    sim_dict = {}
    metrica_idx = {'coseno': 2, 'jaccard': 3, 'levenshtein': 4}
    idx = metrica_idx.get(metrica, 2)
    
    for resultado in resultados:
        key = (resultado[0], resultado[1])
        sim_dict[key] = resultado[idx]
        # Agregar la versión simétrica
        key_inv = (resultado[1], resultado[0])
        sim_dict[key_inv] = resultado[idx]
    
    # Generar encabezados
    nombres_archivos = [Path(archivo).name for archivo in archivos_procesados]
    f.write("| | " + " | ".join([f"`{nombre}`" for nombre in nombres_archivos]) + " |\n")
    f.write("|" + "-|" * (len(archivos_procesados) + 1) + "\n")
    
    # Generar filas de la matriz
    for i, archivo_a in enumerate(archivos_procesados):
        nombre_a = Path(archivo_a).name
        f.write(f"| `{nombre_a}` |")
        
        for j, archivo_b in enumerate(archivos_procesados):
            if i == j:
                f.write(" **1.000** |")
            elif i < j:
                # Buscar similitud
                key = (archivo_a, archivo_b)
                sim = sim_dict.get(key, 0.0)
                color = get_color_similarity(sim)
                f.write(f" {color}{sim:.3f}** |")
            else:
                f.write(" - |")
        f.write("\n")


def get_color_similarity(similitud: float) -> str:
    """Retorna un indicador de color basado en el nivel de similitud."""
    if similitud >= 0.8:
        return "🔴**"  # Alta similitud
    elif similitud >= 0.6:
        return "🟡**"  # Similitud media-alta
    elif similitud >= 0.4:
        return "🟢**"  # Similitud media
    else:
        return "⚪**"  # Similitud baja


def generar_reporte_markdown(resultados: List[List], estadisticas: Dict, 
                           archivo_salida: str, archivos_procesados: List[str]) -> None:
    """
    Genera un reporte en formato Markdown con tablas y estadísticas.
    
    Args:
        resultados: Lista de resultados de comparación
        estadisticas: Diccionario con estadísticas resumen
        archivo_salida: Nombre base del archivo de salida
        archivos_procesados: Lista de archivos que fueron procesados
    """
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(f'{archivo_salida}.md', 'w', encoding='utf-8') as f:
        # Header del reporte
        f.write("# 🔍 Reporte de Similitud de Códigos Fuente\n\n")
        f.write("**Análisis Computacional de Similitud entre Códigos Fuente**\n")
        f.write("*Basado en Métricas Validadas Científicamente*\n\n")
        f.write("---\n\n")
        f.write("## 📋 Información del Análisis\n\n")
        f.write(f"- **Fecha de generación:** {fecha_actual}\n")
        f.write(f"- **Versión del software:** 2.0\n")
        f.write(f"- **Archivos analizados:** {len(archivos_procesados)}\n")
        f.write(f"- **Total de comparaciones:** {len(resultados)}\n")
        f.write(f"- **Métricas utilizadas:** Coseno, Jaccard, Levenshtein\n")
        f.write(f"- **Algoritmos implementados:** Salton et al. (1975), Jaccard (1912), Levenshtein (1966)\n\n")
        
        # Resumen ejecutivo
        if estadisticas:
            f.write("## 📊 Resumen Ejecutivo\n\n")
            
            # Determinar el nivel general de similitud
            promedio_general = (estadisticas['cosine_promedio'] + 
                              estadisticas['jaccard_promedio'] + 
                              estadisticas['levenshtein_promedio']) / 3
            
            if promedio_general >= 0.7:
                nivel_similitud = "**ALTA**"
                interpretacion = "Se detectaron similitudes significativas que requieren atención."
            elif promedio_general >= 0.4:
                nivel_similitud = "**MEDIA**"
                interpretacion = "Se observan similitudes moderadas entre algunos archivos."
            else:
                nivel_similitud = "**BAJA**"
                interpretacion = "Los archivos muestran diferencias considerables en su estructura."
            
            f.write(f"- **Nivel de similitud general:** {nivel_similitud} ({promedio_general:.3f})\n")
            f.write(f"- **Interpretación:** {interpretacion}\n")
            f.write(f"- **Métrica más discriminante:** ")
            
            # Encontrar la métrica con mayor variabilidad
            variabilidad_coseno = estadisticas['cosine_max'] - estadisticas['cosine_min']
            variabilidad_jaccard = estadisticas['jaccard_max'] - estadisticas['jaccard_min']  
            variabilidad_levenshtein = estadisticas['levenshtein_max'] - estadisticas['levenshtein_min']
            
            max_variabilidad = max(variabilidad_coseno, variabilidad_jaccard, variabilidad_levenshtein)
            if max_variabilidad == variabilidad_coseno:
                f.write("Similitud del Coseno\n")
            elif max_variabilidad == variabilidad_jaccard:
                f.write("Índice de Jaccard\n")
            else:
                f.write("Distancia de Levenshtein\n")
            
            f.write(f"- **Archivos con mayor similitud:** ")
            # Encontrar el par con mayor similitud
            max_similitud = 0
            par_similar = None
            for resultado in resultados:
                sim_max = max(resultado[2], resultado[3], resultado[4])
                if sim_max > max_similitud:
                    max_similitud = sim_max
                    par_similar = (Path(resultado[0]).name, Path(resultado[1]).name)
            
            if par_similar:
                f.write(f"`{par_similar[0]}` y `{par_similar[1]}` ({max_similitud:.3f})\n")
            
            f.write("\n")
        
        # Lista de archivos procesados
        f.write("## 📁 Archivos Analizados\n\n")
        for i, archivo in enumerate(archivos_procesados, 1):
            nombre_archivo = Path(archivo).name
            f.write(f"{i}. `{nombre_archivo}`\n")
        f.write("\n")
        
        # Tabla de resultados
        f.write("## 📊 Resultados de Similitud\n\n")
        
        # Si hay más de 3 archivos, mostrar matriz de similitud
        if len(archivos_procesados) > 3:
            f.write("### Matriz de Similitud (Coseno)\n\n")
            generar_matriz_similitud(f, resultados, archivos_procesados, 'coseno')
            f.write("\n")
        
        # Tabla detallada de comparaciones
        f.write("### Comparaciones Detalladas\n\n")
        f.write("| Archivo A | Archivo B | Coseno | Jaccard | Levenshtein |\n")
        f.write("|-----------|-----------|--------|---------|-------------|\n")
        
        for resultado in resultados:
            archivo_a = Path(resultado[0]).name
            archivo_b = Path(resultado[1]).name
            f.write(f"| `{archivo_a}` | `{archivo_b}` | {resultado[2]:.3f} | {resultado[3]:.3f} | {resultado[4]:.3f} |\n")
        
        f.write("\n")
        
        # Estadísticas
        if estadisticas:
            f.write("## 📈 Estadísticas Resumen\n\n")
            
            # Gráfico de barras en ASCII para estadísticas
            f.write("### Distribución de Similitud\n\n")
            f.write("```\n")
            f.write("Similitud del Coseno\n")
            f.write(f"Min  {estadisticas['cosine_min']:.3f} {'█' * int(estadisticas['cosine_min'] * 20)}\n")
            f.write(f"Prom {estadisticas['cosine_promedio']:.3f} {'█' * int(estadisticas['cosine_promedio'] * 20)}\n")
            f.write(f"Max  {estadisticas['cosine_max']:.3f} {'█' * int(estadisticas['cosine_max'] * 20)}\n")
            f.write("```\n\n")
            
            f.write("### Métricas Detalladas\n\n")
            f.write("| Métrica | Mínimo | Promedio | Máximo |\n")
            f.write("|---------|--------|----------|--------|\n")
            f.write(f"| **Coseno** | {estadisticas['cosine_min']:.3f} | {estadisticas['cosine_promedio']:.3f} | {estadisticas['cosine_max']:.3f} |\n")
            f.write(f"| **Jaccard** | {estadisticas['jaccard_min']:.3f} | {estadisticas['jaccard_promedio']:.3f} | {estadisticas['jaccard_max']:.3f} |\n")
            f.write(f"| **Levenshtein** | {estadisticas['levenshtein_min']:.3f} | {estadisticas['levenshtein_promedio']:.3f} | {estadisticas['levenshtein_max']:.3f} |\n")
            f.write("\n")
            
            # Análisis de similitudes altas
            similitudes_altas = [r for r in resultados if max(r[2], r[3], r[4]) >= 0.7]
            if similitudes_altas:
                f.write("### ⚠️ Similitudes Altas Detectadas\n\n")
                f.write("Los siguientes pares de archivos muestran similitud alta (≥ 0.7):\n\n")
                for resultado in similitudes_altas:
                    archivo_a = Path(resultado[0]).name
                    archivo_b = Path(resultado[1]).name
                    max_sim = max(resultado[2], resultado[3], resultado[4])
                    f.write(f"- `{archivo_a}` ↔ `{archivo_b}`: **{max_sim:.3f}**\n")
                f.write("\n")
        
        # Interpretación
        f.write("## 🎯 Interpretación de Resultados\n\n")
        f.write("- **0.0 - 0.3:** Similitud baja (códigos muy diferentes)\n")
        f.write("- **0.3 - 0.7:** Similitud media (algunos elementos comunes)\n")
        f.write("- **0.7 - 0.9:** Similitud alta (códigos muy parecidos)\n")
        f.write("- **0.9 - 1.0:** Similitud muy alta (posible duplicación)\n\n")
        
        # Metodología
        f.write("## 🔬 Metodología\n\n")
        f.write("Este análisis utiliza tres métricas de similitud validadas científicamente:\n\n")
        f.write("1. **Similitud del Coseno:** Mide el ángulo entre vectores de frecuencia de tokens [1,2]\n")
        f.write("2. **Índice de Jaccard:** Calcula similitud basada en intersección/unión de conjuntos [3,4]\n")
        f.write("3. **Ratio de Levenshtein:** Distancia de edición normalizada entre textos [5,6]\n\n")
        
        # Referencias académicas
        f.write("## 📚 Referencias\n\n")
        f.write("**[1]** Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM*, 18(11), 613-620. DOI: 10.1145/361219.361220\n\n")
        f.write("**[2]** Singhal, A. (2001). Modern information retrieval: A brief overview. *IEEE Data Engineering Bulletin*, 24(4), 35-43.\n\n")
        f.write("**[3]** Jaccard, P. (1912). The distribution of the flora in the alpine zone. *New Phytologist*, 11(2), 37-50. DOI: 10.1111/j.1469-8137.1912.tb05611.x\n\n")
        f.write("**[4]** Real, R., & Vargas, J. M. (1996). The probabilistic basis of Jaccard's index of similarity. *Systematic Biology*, 45(3), 380-385. DOI: 10.1093/sysbio/45.3.380\n\n")
        f.write("**[5]** Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707-710.\n\n")
        f.write("**[6]** Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM*, 21(1), 168-173. DOI: 10.1145/321796.321811\n\n")
        
        # Referencias adicionales para detección de clones
        f.write("### Aplicaciones en Detección de Similitud de Código\n\n")
        f.write("**[7]** Bellon, S., Koschke, R., Antoniol, G., Krinke, J., & Merlo, E. (2007). Comparison and evaluation of clone detection tools. *IEEE Transactions on Software Engineering*, 33(9), 577-591.\n\n")
        f.write("**[8]** Roy, C. K., Cordy, J. R., & Koschke, R. (2009). Comparison and evaluation of code clone detection techniques and tools: A qualitative approach. *Science of Computer Programming*, 74(7), 470-495.\n\n")
        
        # Conclusiones automáticas
        if estadisticas and len(resultados) > 0:
            f.write("## 🎯 Conclusiones\n\n")
            
            promedio_general = (estadisticas['cosine_promedio'] + 
                              estadisticas['jaccard_promedio'] + 
                              estadisticas['levenshtein_promedio']) / 3
            
            # Análisis de consistencia entre métricas
            similitudes_altas_coseno = sum(1 for r in resultados if r[2] >= 0.7)
            similitudes_altas_jaccard = sum(1 for r in resultados if r[3] >= 0.7)
            similitudes_altas_levenshtein = sum(1 for r in resultados if r[4] >= 0.7)
            total_comparaciones = len(resultados)
            
            f.write("### Hallazgos Principal\n\n")
            
            if promedio_general >= 0.7:
                f.write("- **Similitud significativa detectada**: Los archivos analizados muestran patrones estructurales y semánticos similares que sugieren origen común o reutilización de código.\n\n")
            elif promedio_general >= 0.4:
                f.write("- **Similitud moderada observada**: Existe cierto grado de similitud entre los archivos, posiblemente debido a convenciones de programación compartidas o funcionalidades similares.\n\n")
            else:
                f.write("- **Archivos diversos**: Los códigos analizados muestran diferencias sustanciales, indicando implementaciones independientes o enfoques distintos.\n\n")
            
            f.write("### Consistencia de Métricas\n\n")
            if similitudes_altas_coseno > 0 and similitudes_altas_jaccard > 0 and similitudes_altas_levenshtein > 0:
                f.write("- **Alta consistencia**: Las tres métricas coinciden en identificar similitudes altas, aumentando la confiabilidad del análisis.\n\n")
            elif (similitudes_altas_coseno > 0) + (similitudes_altas_jaccard > 0) + (similitudes_altas_levenshtein > 0) >= 2:
                f.write("- **Consistencia moderada**: Al menos dos métricas coinciden en los hallazgos principales.\n\n")
            else:
                f.write("- **Métricas divergentes**: Las diferentes métricas capturan aspectos distintos de similitud, sugiriendo patrones de similitud complejos.\n\n")
            
            f.write("### Recomendaciones\n\n")
            if promedio_general >= 0.8:
                f.write("- **Revisión necesaria**: Se recomienda revisar manualmente los archivos con alta similitud para evaluar posible duplicación o plagio.\n")
                f.write("- **Refactorización**: Considerar la extracción de código común en módulos reutilizables.\n\n")
            elif promedio_general >= 0.6:
                f.write("- **Monitoreo recomendado**: Vigilar la evolución de similitudes en futuras versiones.\n")
                f.write("- **Documentación**: Documentar las razones de similitudes altas si son intencionales.\n\n")
            else:
                f.write("- **Diversidad confirmada**: La variabilidad observada es esperada y saludable en el desarrollo de software.\n\n")
        
        f.write("---\n")
        f.write("*Reporte generado por Analizador de Similitud de Códigos Fuente v2.0*\n")
        f.write("*Basado en algoritmos validados científicamente y mejores prácticas en análisis de código*\n")


def generar_reporte_pdf(resultados: List[List], estadisticas: Dict, 
                       archivo_salida: str, archivos_procesados: List[str]) -> bool:
    """
    Genera un reporte en formato PDF. Requiere que pandoc esté instalado.
    
    Args:
        resultados: Lista de resultados de comparación
        estadisticas: Diccionario con estadísticas resumen
        archivo_salida: Nombre base del archivo de salida
        archivos_procesados: Lista de archivos que fueron procesados
    
    Returns:
        bool: True si se generó exitosamente, False en caso contrario
    """
    try:
        # Primero generar el Markdown
        generar_reporte_markdown(resultados, estadisticas, archivo_salida + "_temp", archivos_procesados)
        
        # Verificar si pandoc está disponible
        try:
            subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  pandoc no está instalado. Para generar PDF, instale pandoc:")
            print("    Ubuntu/Debian: sudo apt-get install pandoc")
            print("    macOS: brew install pandoc")
            print("    Windows: https://pandoc.org/installing.html")
            return False
        
        # Intentar diferentes motores PDF
        motores_pdf = ['xelatex', 'pdflatex', 'lualatex']
        
        for motor in motores_pdf:
            comando_pandoc = [
                'pandoc',
                f'{archivo_salida}_temp.md',
                '-o', f'{archivo_salida}.pdf',
                f'--pdf-engine={motor}',
                '-V', 'geometry:margin=1in',
                '-V', 'fontsize=11pt',
                '-V', 'linestretch=1.2',
                '--metadata', 'title=Reporte de Similitud de Códigos Fuente',
                '--metadata', 'author=Analizador de Similitud v2.0',
                '--metadata', f'date={datetime.now().strftime("%Y-%m-%d")}',
                '--metadata', 'subject=Análisis de Similitud de Código Fuente',
                '--metadata', 'keywords=similitud,código,coseno,jaccard,levenshtein',
                '--table-of-contents',
                '--toc-depth=2'
            ]
            
            try:
                resultado = subprocess.run(comando_pandoc, capture_output=True, text=True, timeout=30)
                
                if resultado.returncode == 0:
                    # Limpiar archivo temporal
                    if os.path.exists(f'{archivo_salida}_temp.md'):
                        os.remove(f'{archivo_salida}_temp.md')
                    return True
                else:
                    if motor == motores_pdf[-1]:  # último intento
                        print(f"❌ Error con {motor}: {resultado.stderr}")
                        print("💡 Sugerencia: Instale un motor LaTeX:")
                        print("    Ubuntu/Debian: sudo apt-get install texlive-xetex")
                        print("    macOS: brew install mactex")
            
            except subprocess.TimeoutExpired:
                print(f"⏱️  Timeout con {motor}, probando siguiente motor...")
                continue
            except Exception as e:
                print(f"⚠️  Error con {motor}: {e}")
                continue
        
        return False
            
    except Exception as e:
        print(f"❌ Error generando reporte PDF: {e}")
        return False


def guardar_resultados(resultados: List[List], estadisticas: Dict, formato: str = 'csv', 
                      archivo_salida: str = 'reporte_similitud', 
                      archivos_procesados: List[str] = None) -> None:
    """
    Guarda los resultados en el formato especificado.
    
    Args:
        resultados: Lista de resultados de comparación
        estadisticas: Diccionario con estadísticas resumen
        formato: Formato de salida ('csv', 'json', 'md', 'pdf')
        archivo_salida: Nombre base del archivo de salida (sin extensión)
        archivos_procesados: Lista de archivos que fueron procesados
    """
    if archivos_procesados is None:
        archivos_procesados = []
    
    try:
        if formato.lower() == 'csv':
            with open(f'{archivo_salida}.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Archivo A", "Archivo B", "Cosine", "Jaccard", "Levenshtein"])
                writer.writerows(resultados)
                
                # Agregar estadísticas al final
                writer.writerow([])
                writer.writerow(["=== ESTADÍSTICAS ==="])
                for key, value in estadisticas.items():
                    writer.writerow([key.replace('_', ' ').title(), f"{value:.4f}"])
            
            print(f"✅ Reporte CSV generado: {archivo_salida}.csv")
        
        elif formato.lower() == 'json':
            datos = {
                'metadata': {
                    'fecha_generacion': datetime.now().isoformat(),
                    'version': '2.0',
                    'archivos_procesados': len(archivos_procesados)
                },
                'archivos': [{'nombre': Path(a).name, 'ruta': a} for a in archivos_procesados],
                'comparaciones': [
                    {
                        'archivo_a': r[0],
                        'archivo_b': r[1],
                        'similitud_coseno': r[2],
                        'similitud_jaccard': r[3],
                        'similitud_levenshtein': r[4]
                    } for r in resultados
                ],
                'estadisticas': estadisticas
            }
            
            with open(f'{archivo_salida}.json', 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Reporte JSON generado: {archivo_salida}.json")
        
        elif formato.lower() == 'md':
            generar_reporte_markdown(resultados, estadisticas, archivo_salida, archivos_procesados)
            print(f"✅ Reporte Markdown generado: {archivo_salida}.md")
        
        elif formato.lower() == 'pdf':
            if generar_reporte_pdf(resultados, estadisticas, archivo_salida, archivos_procesados):
                print(f"✅ Reporte PDF generado: {archivo_salida}.pdf")
            else:
                # Fallback a Markdown si PDF falla
                generar_reporte_markdown(resultados, estadisticas, archivo_salida, archivos_procesados)
                print(f"✅ Reporte Markdown generado como alternativa: {archivo_salida}.md")
        
    except IOError as e:
        print(f"❌ Error guardando reporte: {e}")


def comparar_archivos(archivos: List[str], threshold: float = 0.0, 
                     formato_salida: str = 'csv', archivo_salida: str = 'reporte_similitud',
                     mostrar_estadisticas: bool = True) -> Optional[List[List]]:
    """
    Compara múltiples archivos de código y genera reporte de similitud.
    
    Args:
        archivos: Lista de rutas de archivos a comparar
        threshold: Umbral mínimo de similitud para mostrar (0.0-1.0)
        formato_salida: Formato del reporte ('csv', 'json')
        archivo_salida: Nombre base del archivo de salida
        mostrar_estadisticas: Si mostrar estadísticas en consola
    
    Returns:
        Lista de resultados o None si hay error
    """
    print("🔍 Analizando archivos de código fuente...\n")
    
    # Validar todos los archivos
    codigos = {}
    archivos_validos = []
    
    for nombre in archivos:
        es_valido, mensaje = validar_archivo(nombre)
        if not es_valido:
            print(f"⚠️  {mensaje}")
            continue
        
        try:
            with open(nombre, 'r', encoding='utf-8') as f:
                contenido = f.read()
                lenguaje = detectar_lenguaje(nombre)
                tokens = limpiar_codigo(contenido, lenguaje)
                
                if not tokens:
                    print(f"⚠️  No se pudieron extraer tokens de {nombre}")
                    continue
                
                codigos[nombre] = tokens
                codigos[nombre + "_txt"] = ' '.join(tokens)
                archivos_validos.append(nombre)
                print(f"✅ Procesado: {nombre} ({len(tokens)} tokens, lenguaje: {lenguaje})")
        
        except Exception as e:
            print(f"❌ Error procesando {nombre}: {e}")
            continue
    
    if len(archivos_validos) < 2:
        print("\n❌ Se necesitan al menos 2 archivos válidos para comparar")
        return None
    
    print(f"\n📊 Comparando {len(archivos_validos)} archivos...\n")
    
    # Realizar comparaciones
    resultados = []
    print(f"{'Comparación':60} | {'Cosine':>7} | {'Jaccard':>8} | {'Leven.':>8} |")
    print("-" * 95)
    
    for a, b in combinations(archivos_validos, 2):
        cos = similitud_coseno(codigos[a], codigos[b])
        jac = similitud_jaccard(codigos[a], codigos[b])
        lev = ratio_levenshtein(codigos[a + '_txt'], codigos[b + '_txt'])
        
        # Aplicar threshold
        if max(cos, jac, lev) >= threshold:
            resultados.append([a, b, round(cos, 4), round(jac, 4), round(lev, 4)])
            
            # Formatear nombres para display
            nombre_a = Path(a).name
            nombre_b = Path(b).name
            comparacion = f"{nombre_a} ↔ {nombre_b}"
            
            print(f"{comparacion:60} | {cos:7.3f} | {jac:8.3f} | {lev:8.3f} |")
    
    if not resultados:
        print(f"\n⚠️  No se encontraron similitudes por encima del umbral {threshold}")
        return []
    
    # Generar estadísticas
    estadisticas = generar_estadisticas(resultados)
    
    if mostrar_estadisticas and estadisticas:
        print(f"\n📈 Estadísticas de similitud:")
        print(f"  Total de comparaciones: {estadisticas['total_comparaciones']}")
        print(f"  Coseno    - Promedio: {estadisticas['cosine_promedio']:.3f}, Max: {estadisticas['cosine_max']:.3f}")
        print(f"  Jaccard   - Promedio: {estadisticas['jaccard_promedio']:.3f}, Max: {estadisticas['jaccard_max']:.3f}")
        print(f"  Levenshtein - Promedio: {estadisticas['levenshtein_promedio']:.3f}, Max: {estadisticas['levenshtein_max']:.3f}")
    
    # Guardar resultados
    guardar_resultados(resultados, estadisticas, formato_salida, archivo_salida, archivos_validos)
    
    return resultados


# ======================================
# 🔹 Configuración de argumentos y main
# ======================================

def configurar_argumentos() -> argparse.ArgumentParser:
    """Configura los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='🔍 Analizador de similitud entre códigos fuente',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s archivo1.py archivo2.py archivo3.py
  %(prog)s *.py --threshold 0.5 --formato md
  %(prog)s src/*.java --formato pdf --output reporte_java
  %(prog)s --threshold 0.3 --formato json *.py
  %(prog)s carpeta/*.cpp --formato md --output reporte_cpp
        """
    )
    
    parser.add_argument('archivos', nargs='+', 
                       help='Archivos de código fuente a comparar (mínimo 2)')
    
    parser.add_argument('-t', '--threshold', type=float, default=0.0,
                       help='Umbral mínimo de similitud (0.0-1.0, default: 0.0)')
    
    parser.add_argument('-f', '--formato', choices=['csv', 'json', 'md', 'pdf'], default='csv',
                       help='Formato del archivo de salida: csv, json, md, pdf (default: csv)')
    
    parser.add_argument('-o', '--output', default='reporte_similitud',
                       help='Nombre base del archivo de salida (default: reporte_similitud)')
    
    parser.add_argument('--no-estadisticas', action='store_true',
                       help='No mostrar estadísticas en consola')
    
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    
    return parser


def main():
    """Función principal del programa."""
    parser = configurar_argumentos()
    args = parser.parse_args()
    
    # Validar argumentos
    if len(args.archivos) < 2:
        print("❌ Error: Se necesitan al menos 2 archivos para comparar")
        sys.exit(1)
    
    if not (0.0 <= args.threshold <= 1.0):
        print("❌ Error: El threshold debe estar entre 0.0 y 1.0")
        sys.exit(1)
    
    print("=" * 80)
    print("🔍 ANALIZADOR DE SIMILITUD DE CÓDIGOS FUENTE v2.0")
    print("=" * 80)
    
    # Ejecutar análisis
    try:
        resultados = comparar_archivos(
            archivos=args.archivos,
            threshold=args.threshold,
            formato_salida=args.formato,
            archivo_salida=args.output,
            mostrar_estadisticas=not args.no_estadisticas
        )
        
        if resultados is None:
            sys.exit(1)
        elif len(resultados) == 0:
            print("\n⚠️  No se encontraron similitudes significativas")
        else:
            print(f"\n🎉 Análisis completado exitosamente!")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


# ======================================
# 🔹 Bloque principal
# ======================================
if __name__ == "__main__":
    main()