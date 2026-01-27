Benchmarking y análisis de rendimiento

Este repositorio incluye un análisis de rendimiento del pipeline FastQC + MultiQC con el objetivo de evaluar el impacto del paralelismo y la contenerización mediante Docker en entornos multi-core.

Se compararon ejecuciones secuenciales y paralelas utilizando diferentes tamaños de datasets (desde ~20 MB hasta ~1 GB), manteniendo constante la lógica del pipeline y variando únicamente la configuración de ejecución mediante perfiles de Nextflow.

El benchmarking se basa en las siguientes métricas:

Tiempo total de ejecución del pipeline

Speedup (relación entre ejecución secuencial y paralela)

Tiempo ahorrado mediante paralelismo

Distribución temporal de los procesos

Uso de CPU y memoria

Los datos de benchmark fueron obtenidos a partir de los archivos de trace generados automáticamente por Nextflow (-with-trace), los cuales se encuentran disponibles en el directorio:

docs/benchmarks/


Cada archivo trace_*.txt contiene información detallada sobre:

Duración de cada proceso

Uso de CPU

Consumo de memoria

Orden y concurrencia de ejecución

Los gráficos y el análisis detallado de los resultados (speedup, escalabilidad y eficiencia) se presentan en el informe técnico incluido en el repositorio:

INFORME_RESULTADOS.md


Los scripts utilizados para generar los datos de prueba, ejecutar los benchmarks y producir las visualizaciones se encuentran en el directorio:

scripts/


Este enfoque garantiza la reproducibilidad completa de los resultados y permite verificar empíricamente el comportamiento del pipeline bajo diferentes configuraciones de ejecución.
