# nf-fastqc-multiqc (Nextflow DSL2 + Docker)

Pipeline de Control de Calidad (FastQC + MultiQC) implementado en **Nextflow DSL2** y ejecutable con **Docker** (incluye workaround para Apple Silicon M1/M2 con `--platform=linux/amd64`).

## Contenido del repositorio

- `main.nf`: pipeline Nextflow (DSL2)
- `nextflow.config`: configuración (Docker + recursos)
- `data/`: FASTQ de ejemplo (NO versionar datos pesados)
- `results/`: outputs (NO versionar; se generan al correr)
- `docs/TP_Pipelines_Privitera_Dominguez_Tranier.docx`: informe del TP
- `docs/`: capturas/reportes opcionales (FastQC/MultiQC/trace/report/timeline)

## Requisitos

- Java (recomendado: 17)
- Nextflow (probado con 25.04.7)
- Docker Desktop

Verificar instalación:
```bash
nextflow -version
docker --version
```

## Quick start (local + Docker)

1) Clonar:
```bash
git clone <TU_URL_DEL_REPO>
cd nf-fastqc-multiqc
```

2) Colocar al menos un FASTQ en `data/` (ejemplo):
```bash
cp /ruta/a/archivo.fastq.gz data/
```

3) Ejecutar:
```bash
nextflow run main.nf -resume
```

## Generar reportes de trazabilidad (obligatorio TP)

```bash
nextflow run main.nf \
  -with-report report.html \
  -with-trace trace.txt \
  -with-timeline timeline.html \
  -with-dag flowchart.png \
  -resume
```

Abrir reportes en macOS:
```bash
open report.html
open timeline.html
open flowchart.png
open trace.txt
```

## Nota Apple Silicon (M1/M2)

En `nextflow.config` se fuerza la plataforma para imágenes amd64:
```groovy
docker.runOptions = '--platform=linux/amd64'
```

## Reproducibilidad

Contenedores usados:
- FastQC: `biocontainers/fastqc:v0.11.9_cv8`
- MultiQC: `ewels/multiqc:latest`

## Licencia

MIT (ver `LICENSE`).
