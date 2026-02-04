#!/bin/bash
# Benchmark script para comparar diferentes configuraciones de recursos

export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
cd /root/personal/TP-nf-fastqc-multiqc

RESULTS_FILE="benchmark_results.csv"
echo "config,cpus,memory,file,file_size_kb,fastqc_duration_s,multiqc_duration_s,total_duration_s,peak_memory_mb" > $RESULTS_FILE

run_benchmark() {
    local cpus=$1
    local memory=$2
    local config_name="${cpus}cpu_${memory}"

    echo "=== Running benchmark: $config_name ==="

    # Limpiar ejecuciones anteriores
    rm -rf work .nextflow* results trace.txt 2>/dev/null

    # Ejecutar pipeline con trace
    nextflow run main.nf \
        --reads "data/*.fastq" \
        -process.cpus $cpus \
        -process.memory "${memory}" \
        -with-trace trace.txt \
        -ansi-log false 2>&1 | tail -5

    # Parsear resultados del trace
    if [ -f trace.txt ]; then
        tail -n +2 trace.txt | while IFS=$'\t' read -r task_id hash native_id name status exit submit start complete duration realtime cpu_pct peak_rss peak_vmem rchar wchar; do
            # Extraer nombre del archivo del campo name
            file_info=$(echo "$name" | grep -oP '\(.*\)' | tr -d '()')

            # Convertir duración a segundos
            duration_sec=$(echo "$realtime" | sed 's/s$//' | sed 's/m/*60+/' | sed 's/h/*3600+/' | bc 2>/dev/null || echo "$realtime")

            # Obtener tamaño del archivo
            if [[ "$name" == *"FASTQC"* ]]; then
                process="FASTQC"
            else
                process="MULTIQC"
            fi

            # Peak RSS en MB
            peak_mb=$(echo "$peak_rss" | sed 's/ MB//' | sed 's/ GB/*1024/' | bc 2>/dev/null || echo "0")

            echo "$config_name,$cpus,$memory,$process,$file_info,$realtime,$peak_rss"
        done
    fi

    echo ""
}

# Ejecutar benchmarks con diferentes configuraciones
run_benchmark 1 "2 GB"
run_benchmark 2 "4 GB"
run_benchmark 4 "8 GB"

echo "=== Benchmark completado ==="
echo "Resultados guardados en: $RESULTS_FILE"
