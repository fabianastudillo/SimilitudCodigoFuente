# 🔍 Analizador de Similitud de Códigos Fuente v2.0

Una herramienta avanzada para analizar y comparar la similitud entre archivos de código fuente utilizando múltiples métricas de similitud.

## ✨ Características Principales

### 🚀 **Mejoras v2.0**
- ✅ **Manejo robusto de errores** con validación completa de archivos
- ✅ **Soporte multi-lenguaje** (Python, JavaScript, Java, C++, C#, etc.)
- ✅ **Algoritmos optimizados** con menor uso de memoria
- ✅ **Argumentos de línea de comandos** configurables
- ✅ **Múltiples formatos de salida** (CSV, JSON)
- ✅ **Estadísticas detalladas** y análisis resumido
- ✅ **Documentación completa** con type hints
- ✅ **Tokenización inteligente** que preserva palabras clave

### 📊 **Métricas de Similitud**
- **Similitud del Coseno**: Mide el ángulo entre vectores de frecuencia de tokens [1,2]
- **Índice de Jaccard**: Calcula similitud basada en intersección/unión de conjuntos [3,4]
- **Ratio de Levenshtein**: Distancia de edición normalizada entre textos [5,6]

## 🛠️ Instalación

```bash
git clone https://github.com/usuario/SimilitudCodigoFuente.git
cd SimilitudCodigoFuente
```

**Requisitos básicos:** Python 3.6+

**Para generar reportes PDF:** pandoc y XeLaTeX
```bash
# Ubuntu/Debian
sudo apt-get install pandoc texlive-xetex

# macOS  
brew install pandoc mactex

# Windows
# Descargar desde https://pandoc.org/installing.html
# y https://miktex.org/
```

## 📖 Uso

### Uso Básico
```bash
python3 similitud_codigos_reporte.py archivo1.py archivo2.py
```

### Opciones Avanzadas
```bash
# Múltiples archivos con umbral de similitud
python3 similitud_codigos_reporte.py *.py --threshold 0.5

# Reporte en formato Markdown (con matriz de similitud)
python3 similitud_codigos_reporte.py archivo1.py archivo2.py archivo3.py --formato md

# Reporte en formato PDF (requiere pandoc)
python3 similitud_codigos_reporte.py *.py --formato pdf --output reporte_final

# Formato JSON con metadatos extendidos
python3 similitud_codigos_reporte.py *.java --formato json --output analisis_java

# Personalizar archivo de salida
python3 similitud_codigos_reporte.py *.py --output mi_reporte

# Sin estadísticas en consola
python3 similitud_codigos_reporte.py *.py --no-estadisticas
```

### Argumentos Disponibles
```
archivos              Archivos de código fuente a comparar (2 o más)
-t, --threshold       Umbral mínimo similitud (0.0-1.0, default: 0.0)
-f, --formato         Formato salida: csv, json, md, pdf (default: csv)
-o, --output          Nombre base archivo salida (default: reporte_similitud)
--no-estadisticas     No mostrar estadísticas en consola
--version             Mostrar versión del programa
-h, --help            Mostrar ayuda
```

## 📋 Ejemplo de Salida

### Consola
```
================================================================================
🔍 ANALIZADOR DE SIMILITUD DE CÓDIGOS FUENTE v2.0
================================================================================
🔍 Analizando archivos de código fuente...

✅ Procesado: test_file1.py (107 tokens, lenguaje: python)
✅ Procesado: test_file2.py (121 tokens, lenguaje: python)

📊 Comparando 2 archivos...

Comparación                                                  |  Cosine |  Jaccard |   Leven. |
-----------------------------------------------------------------------------------------------
test_file1.py ↔ test_file2.py                                |   0.763 |    0.538 |    0.613 |

📈 Estadísticas de similitud:
  Total de comparaciones: 1
  Coseno    - Promedio: 0.763, Max: 0.763
  Jaccard   - Promedio: 0.538, Max: 0.538
  Levenshtein - Promedio: 0.613, Max: 0.613

✅ Reporte CSV generado: reporte_similitud.csv
🎉 Análisis completado exitosamente!
```

### Archivo JSON
```json
{
  "metadata": {
    "fecha_generacion": "2025-11-11T10:30:45",
    "version": "2.0",
    "archivos_procesados": 3
  },
  "archivos": [
    {"nombre": "test_file1.py", "ruta": "test_file1.py"},
    {"nombre": "test_file2.py", "ruta": "test_file2.py"}
  ],
  "comparaciones": [
    {
      "archivo_a": "test_file1.py",
      "archivo_b": "test_file2.py", 
      "similitud_coseno": 0.7628,
      "similitud_jaccard": 0.5385,
      "similitud_levenshtein": 0.6128
    }
  ],
  "estadisticas": {
    "cosine_promedio": 0.7628,
    "cosine_max": 0.7628,
    "total_comparaciones": 1
  }
}
```

### Reporte Markdown
- **Tabla de archivos procesados** con numeración
- **Matriz de similitud visual** para múltiples archivos (>3)
- **Comparaciones detalladas** en formato tabla
- **Estadísticas con gráficos ASCII** 
- **Detección automática de similitudes altas** (≥ 0.7)
- **Interpretación y metodología** incluidas

### Reporte PDF
- **Conversión automática** desde Markdown usando pandoc
- **Formato profesional** con márgenes y tipografía optimizada
- **Requiere pandoc instalado** (fallback a Markdown si no está disponible)
- **Metadata del documento** incluida

## 🔧 Características Técnicas

### Lenguajes Soportados
- Python (`.py`)
- JavaScript (`.js`)
- Java (`.java`)
- C++ (`.cpp`)
- C (`.c`)
- C# (`.cs`)
- PHP (`.php`)
- Ruby (`.rb`)
- Go (`.go`)

### Optimizaciones
- **Algoritmo Levenshtein**: Complejidad espacial O(min(n,m)) en lugar de O(n×m)
- **Tokenización inteligente**: Preserva palabras clave y estructura semántica
- **Validación robusta**: Verificación de archivos antes del procesamiento
- **Manejo de errores**: Continúa procesamiento aunque algunos archivos fallen

### Interpretación de Resultados
- **0.0 - 0.3**: Similitud baja (códigos muy diferentes)
- **0.3 - 0.7**: Similitud media (algunos elementos comunes)
- **0.7 - 0.9**: Similitud alta (códigos muy parecidos)
- **0.9 - 1.0**: Similitud muy alta (posible duplicación)

### Fundamento Científico

Esta herramienta implementa métricas de similitud ampliamente validadas en la literatura científica:

- **Similitud del Coseno**: Utilizada extensamente en recuperación de información y procesamiento de lenguaje natural desde los trabajos pioneros de Salton et al. (1975). Es especialmente efectiva para comparar documentos de diferentes longitudes.

- **Índice de Jaccard**: Métrica clásica desarrollada originalmente para estudios botánicos (Jaccard, 1912), adoptada en ciencias de la computación por su simplicidad y efectividad para medir similitud entre conjuntos.

- **Distancia de Levenshtein**: Algoritmo fundamental en teoría de códigos y bioinformática, propuesto por Vladimir Levenshtein (1966) para corrección de errores, con aplicaciones modernas en detección de plagios y análisis de secuencias.

### Aplicaciones en Detección de Clones de Código

Las técnicas implementadas están respaldadas por investigación específica en detección de clones de código fuente (Bellon et al., 2007; Roy et al., 2009), con aplicaciones en:

- **Análisis de calidad de software**
- **Detección de plagio académico**  
- **Refactoring y mantenimiento de código**
- **Auditorías de propiedad intelectual**

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`) 
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📚 Referencias Académicas

> **Nota**: Las referencias completas en formato BibTeX están disponibles en [`referencias.bib`](referencias.bib) para uso académico.

### Métricas de Similitud - Fundamentos Teóricos

**[1]** Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM*, 18(11), 613-620. [DOI: 10.1145/361219.361220](https://doi.org/10.1145/361219.361220)

**[2]** Singhal, A. (2001). Modern information retrieval: A brief overview. *IEEE Data Engineering Bulletin*, 24(4), 35-43.

**[3]** Jaccard, P. (1912). The distribution of the flora in the alpine zone. *New Phytologist*, 11(2), 37-50. [DOI: 10.1111/j.1469-8137.1912.tb05611.x](https://doi.org/10.1111/j.1469-8137.1912.tb05611.x)

**[4]** Real, R., & Vargas, J. M. (1996). The probabilistic basis of Jaccard's index of similarity. *Systematic Biology*, 45(3), 380-385. [DOI: 10.1093/sysbio/45.3.380](https://doi.org/10.1093/sysbio/45.3.380)

**[5]** Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707-710.

**[6]** Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM*, 21(1), 168-173. [DOI: 10.1145/321796.321811](https://doi.org/10.1145/321796.321811)

### Aplicaciones en Detección de Similitud de Código

**[7]** Bellon, S., Koschke, R., Antoniol, G., Krinke, J., & Merlo, E. (2007). Comparison and evaluation of clone detection tools. *IEEE Transactions on Software Engineering*, 33(9), 577-591. [DOI: 10.1109/TSE.2007.70725](https://doi.org/10.1109/TSE.2007.70725)

**[8]** Roy, C. K., Cordy, J. R., & Koschke, R. (2009). Comparison and evaluation of code clone detection techniques and tools: A qualitative approach. *Science of Computer Programming*, 74(7), 470-495. [DOI: 10.1016/j.scico.2009.02.007](https://doi.org/10.1016/j.scico.2009.02.007)

**[9]** Rattan, D., Bhatia, R., & Singh, M. (2013). Software clone detection: A systematic review. *Information and Software Technology*, 55(7), 1165-1199. [DOI: 10.1016/j.infsof.2013.01.008](https://doi.org/10.1016/j.infsof.2013.01.008)

**[10]** White, M., Tufano, M., Vendome, C., & Poshyvanyk, D. (2016). Deep learning code fragments for code clone detection. *Proceedings of the 31st IEEE/ACM International Conference on Automated Software Engineering*, 87-98. [DOI: 10.1145/2970276.2970326](https://doi.org/10.1145/2970276.2970326)

### Procesamiento de Lenguaje Natural y Tokenización

**[11]** Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press. Cambridge, UK.

**[12]** Jurafsky, D., & Martin, J. H. (2019). *Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition* (3rd ed.). Pearson Prentice Hall.

## �🙏 Agradecimientos

- Algoritmos basados en investigación en procesamiento de lenguaje natural y recuperación de información
- Inspirado en herramientas de detección de plagio académico y clones de código  
- Metodologías validadas por la comunidad científica internacional
- Comunidad Python por las excelentes librerías estándar