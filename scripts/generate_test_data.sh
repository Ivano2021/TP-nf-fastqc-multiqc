#!/bin/bash
# generate_test_data.sh - Genera datos de prueba para benchmarks
#
# Descarga reads de SARS-CoV-2 de nf-core/test-datasets y genera
# sets de archivos FASTQ de diferentes tamaños para benchmarking.
#
# Uso: ./scripts/generate_test_data.sh
#
# Genera:
#   data/set_10mb/   - 8 archivos de ~2.5MB cada uno (20MB total)
#   data/set_50mb/   - 8 archivos de ~13MB cada uno (99MB total)
#   data/set_100mb/  - 8 archivos de ~25MB cada uno (197MB total)
#   data/set_500mb/  - 8 archivos de ~123MB cada uno (984MB total)

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Generador de Datos de Prueba ===${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "main.nf" ]; then
    echo -e "${RED}Error: Ejecutar desde el directorio raíz del proyecto${NC}"
    echo "Uso: ./scripts/generate_test_data.sh"
    exit 1
fi

# Crear directorio data si no existe
mkdir -p data
cd data

echo -e "${YELLOW}1. Descargando archivo base de nf-core/test-datasets...${NC}"
curl -sL "https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/sarscov2/illumina/fastq/test_1.fastq.gz" | gunzip > base.fastq

if [ ! -s base.fastq ]; then
    echo -e "${RED}Error: No se pudo descargar el archivo base${NC}"
    exit 1
fi

echo -e "${GREEN}   ✓ Archivo base descargado ($(du -h base.fastq | cut -f1))${NC}"

echo -e "${YELLOW}2. Creando bloque intermedio (100x)...${NC}"
for i in {1..100}; do cat base.fastq; done > block_100x.fastq
echo -e "${GREEN}   ✓ Bloque creado ($(du -h block_100x.fastq | cut -f1))${NC}"

# Función para crear set de archivos
create_set() {
    local name=$1
    local blocks=$2
    local dir="set_${name}"

    echo -e "${YELLOW}3. Creando set ${name}...${NC}"

    # Crear archivo de tamaño deseado
    echo "   Generando archivo base..."
    for i in $(seq 1 $blocks); do cat block_100x.fastq; done | gzip > "test_${name}.fastq.gz"

    # Crear directorio y copiar 8 veces
    mkdir -p "$dir"
    echo "   Copiando a 8 muestras..."
    for i in {1..8}; do
        cp "test_${name}.fastq.gz" "${dir}/sample_${i}.fastq.gz"
    done

    # Mostrar tamaño
    local size=$(du -sh "$dir" | cut -f1)
    echo -e "${GREEN}   ✓ ${dir}/ creado (${size} total)${NC}"
}

# Crear sets de diferentes tamaños
# 10MB: 3 bloques de 3.4MB = ~10MB
create_set "10mb" 3

# 50MB: 15 bloques
create_set "50mb" 15

# 100MB: 30 bloques
create_set "100mb" 30

# 500MB: 150 bloques
create_set "500mb" 150

echo -e "${YELLOW}4. Limpiando archivos temporales...${NC}"
rm -f base.fastq block_100x.fastq test_*.fastq.gz
echo -e "${GREEN}   ✓ Limpieza completada${NC}"

echo ""
echo -e "${GREEN}=== Datos de prueba generados exitosamente ===${NC}"
echo ""
echo "Estructura creada:"
du -sh set_*/
echo ""
echo "Para ejecutar benchmarks:"
echo "  nextflow run main.nf --reads 'data/set_100mb/*.fastq.gz' -profile sequential"
echo "  nextflow run main.nf --reads 'data/set_100mb/*.fastq.gz' -profile parallel"
