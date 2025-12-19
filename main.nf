// main.nf (PLACEHOLDER)
// Reemplazá este archivo por tu main.nf real.

nextflow.enable.dsl = 2

params.reads  = "${baseDir}/data/*.fastq"
params.outdir = "${baseDir}/results"

workflow {
    reads_ch = Channel.fromPath(params.reads)
    fastqc_out = FASTQC(reads_ch)
    fastqc_out.collect().set { multiqc_in }
    MULTIQC(multiqc_in)
}

process FASTQC {
    container 'biocontainers/fastqc:v0.11.9_cv8'
    publishDir "${params.outdir}/fastqc", mode: 'copy'
    input:
      path reads
    output:
      path "*_fastqc.*"
    script:
    '''
    fastqc ${reads} -o .
    '''
}

process MULTIQC {
    container 'ewels/multiqc:latest'
    publishDir "${params.outdir}/multiqc", mode: 'copy'
    input:
      path qc_files
    output:
      path "multiqc_report.html"
      path "multiqc_data"
    script:
    '''
    multiqc . -o .
    '''
}
