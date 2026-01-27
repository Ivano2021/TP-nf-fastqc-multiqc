nextflow.enable.dsl=2

/*
 * Parámetros de entrada y salida
 */
params.reads  = "${baseDir}/data/*.{fastq,fastq.gz,fq,fq.gz}"
params.outdir = "${baseDir}/results"

/*
 * Proceso FASTP
 * Preprocesamiento de reads (filtrado y trimming)
 */
process FASTP {

    tag "$reads.baseName"

    container 'quay.io/biocontainers/fastp:0.23.4--hadf994f_2'
    publishDir "${params.outdir}/fastp", mode: 'copy'

    cpus 2
    memory '2 GB'

    input:
    path reads

    output:
    path "trimmed_${reads.baseName}.fastq.gz"
    path "${reads.baseName}_fastp.json"
    path "${reads.baseName}_fastp.html"

    script:
    """
    fastp \
        -i $reads \
        -o trimmed_${reads.baseName}.fastq.gz \
        --thread ${task.cpus} \
        --json ${reads.baseName}_fastp.json \
        --html ${reads.baseName}_fastp.html
    """
}

/*
 * Proceso FASTQC
 * Control de calidad de los reads
 */
process FASTQC {

    tag "$reads.baseName"

    container 'biocontainers/fastqc:v0.11.9_cv8'
    publishDir "${params.outdir}/fastqc", mode: 'copy'

    cpus 1
    memory '1 GB'

    input:
    path reads

    output:
    path "*_fastqc.zip"
    path "*_fastqc.html"

    script:
    """
    fastqc $reads -o .
    """
}

/*
 * Proceso MULTIQC
 * Consolidación de reportes de QC
 */
process MULTIQC {

    container 'quay.io/biocontainers/multiqc:1.14--pyhdfd78af_0'
    publishDir "${params.outdir}/multiqc", mode: 'copy'

    input:
    path qc_results

    output:
    path "multiqc_report.html"

    script:
    """
    multiqc .
    """
}

/*
 * Workflow principal
 */
workflow {

    /*
     * Canal de entrada con los FASTQ
     */
    reads_ch = Channel.fromPath(params.reads)

    /*
     * Ejecución paralela de FASTP
     */
    fastp_out = FASTP(reads_ch)

    /*
     * FASTQC sobre los reads procesados
     */
    fastqc_out = FASTQC(fastp_out)

    /*
     * MultiQC final
     */
    MULTIQC(fastqc_out)
}

