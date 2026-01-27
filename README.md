# nf-fastqc-multiqc (Nextflow DSL2 + Docker)

Pipeline de Control de Calidad (FASTP + FastQC + MultiQC) implementado en **Nextflow DSL2** y ejecutable con **Docker**.

## Resultados del Benchmark

Este proyecto incluye benchmarks que demuestran el beneficio del paralelismo con contenedores Docker:

| Datos | Secuencial | Paralelo | Speedup |
|-------|------------|----------|---------|
| 20 MB | 36.8s | 12.6s | **2.9x** |
| 99 MB | 48.5s | 15.1s | **3.2x** |
| 197 MB | 65.3s | 18.0s | **3.6x** |
| 984 MB | 140s | 30s | **4.7x** |

Ver [INFORME_RESULTADOS.md](INFORME_RESULTADOS.md) para el análisis completo.

## Estructura del Repositorio

```
TP-nf-fastqc-multiqc/
├── main.nf                    # Pipeline Nextflow (DSL2)
├── nextflow.config            # Configuración (Docker + perfiles)
├── README.md                  # Este archivo
├── INFORME_RESULTADOS.md      # Informe completo de resultados
├── CITATION.cff               # Metadatos de citación
├── LICENSE                    # Licencia MIT
├── .gitignore                 # Archivos ignorados
├── data/                      # Datos de entrada (no versionados)
│   └── .keep
├── results/                   # Outputs (generados al ejecutar)
├── scripts/                   # Scripts auxiliares
│   ├── generate_test_data.sh  # Genera datos de prueba para benchmarks
│   ├── generate_charts.py     # Genera gráficos del benchmark
│   └── benchmark.sh           # Script de benchmark
└── docs/
    ├── charts/                # Gráficos de resultados
    ├── benchmarks/            # Archivos de trace (evidencia)
    └── screenshots/           # Capturas de ejecución
```

## Requisitos

- **Java** 17+
- **Nextflow** 25+
- **Docker** 20+

Verificar instalación:
```bash
java -version
nextflow -version
docker --version
```

## Quick Start

### 1. Clonar el repositorio
```bash
git clone https://github.com/Ivano2021/TP-nf-fastqc-multiqc
cd TP-nf-fastqc-multiqc
```

### 2. Agregar datos FASTQ
```bash
cp /ruta/a/tus/archivos/*.fastq.gz data/
```

### 3. Ejecutar el pipeline
```bash
# Ejecución estándar
nextflow run main.nf

# Con reportes de trazabilidad
nextflow run main.nf \
  -with-report report.html \
  -with-trace trace.txt \
  -with-timeline timeline.html
```

## Perfiles de Ejecución

El pipeline incluye perfiles para controlar el paralelismo:

```bash
# Secuencial (1 proceso a la vez)
nextflow run main.nf -profile sequential

# Paralelo (8 procesos simultáneos)
nextflow run main.nf -profile parallel

# Máximo (aprovecha todo el hardware)
nextflow run main.nf -profile max
```

## Pipeline: Procesos

| Proceso | Herramienta | Función |
|---------|-------------|---------|
| FASTP | fastp 0.23.4 | Preprocesamiento y filtrado de reads |
| FASTQC | FastQC 0.11.9 | Control de calidad por muestra |
| MULTIQC | MultiQC 1.14 | Reporte agregado de todas las muestras |

## Contenedores Docker

| Proceso | Imagen |
|---------|--------|
| FASTP | `quay.io/biocontainers/fastp:0.23.4--hadf994f_2` |
| FASTQC | `biocontainers/fastqc:v0.11.9_cv8` |
| MULTIQC | `quay.io/biocontainers/multiqc:1.14--pyhdfd78af_0` |

## Nota para Apple Silicon (M1/M2/M3)

El archivo `nextflow.config` incluye el workaround necesario:
```groovy
docker.runOptions = '--platform=linux/amd64'
```

## Reproducir Benchmarks

```bash
# 1. Generar datos de prueba (descarga de nf-core/test-datasets)
./scripts/generate_test_data.sh

# 2. Ejecutar benchmark secuencial
nextflow run main.nf --reads "data/set_100mb/*.fastq.gz" -profile sequential -with-trace trace_seq.txt

# 3. Ejecutar benchmark paralelo
nextflow run main.nf --reads "data/set_100mb/*.fastq.gz" -profile parallel -with-trace trace_par.txt

# 4. Generar gráficos
python3 scripts/generate_charts.py
```

## Autores

- Iván Privitera Signoretta
- Estefanía Tranier

## Licencia

MIT - ver [LICENSE](LICENSE)

## Citar

Si usás este pipeline, citalo usando los metadatos de [CITATION.cff](CITATION.cff).
