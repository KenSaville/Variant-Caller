"""
fetch reference genome using efetch, fastq files  using fastq dump, find snps
version 0.2.3
"""


import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile



#SRR = 'SRR1553500'
#ACC = 'AF086833'

@small_task    
def call_variants(ACC:str, SRR:str)->LatchFile:

 #   ref_file= Path("ref_genome.fa").resolve()

    _efetch_cmd = [
           "efetch",
            "-db",
            "nuccore",
            "-format",
            "fasta",
            "-id",
            ACC,
         ]

    seq = subprocess.run(_efetch_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

    f = open('ref.fa', "w") 
    f.write(seq)
    f.close()   

#    return LatchFile(str(ref_file), "latch///ref.fa")
    
#def make_index(ref_file):

    subprocess.run(["bwa", "index", "ref.fa"])


#def fastq_dump(SRR:str):

    _fastq_dump_cmd = [
       "fastq-dump","--split-files", "-X", "100000", "--outdir", "fastq_seqs",
       SRR       
     ]

    subprocess.run(_fastq_dump_cmd)
   
#def bwa_mem (SRR:str):

    TAG = f'@RG\\tID:{SRR}\\tSM:{SRR}\\tLB:{SRR}'
    R1 = "fastq_seqs/" + SRR + "_1.fastq"
    R2 = "fastq_seqs/" + SRR + "_2.fastq"
    bam_file=Path(SRR + ".bam").resolve()
    ref = "ref.fa"
    
    bwa_cmd = subprocess.Popen(["bwa", "mem", "-R", TAG, ref, R1, R2],
        stdout = subprocess.PIPE
    )
    
    with open(bam_file, "wb") as f:
     
        sam_tool = subprocess.run(
            ["samtools", "sort"],
            stdin=bwa_cmd.stdout,
            stdout=f) 

#def bcf_genotypes (SRR:str):
 
    genotypes_file = Path("genotypes.vcf").resolve()
    mpileup_cmd = (["bcftools", "mpileup", "-O", "vu","-o","genotypes.vcf", "-f", "ref.fa", SRR + ".bam"])
    genotypes = subprocess.run(mpileup_cmd) 

     
#def bcf_call_variants()->LatchFile:
    variants_file = Path("/root/variants.vcf").resolve()
    bcf_call_cmd =(["bcftools", "call", "--ploidy", "1", "-vm", "-O", "v", "genotypes.vcf", "-o", variants_file])
    subprocess.run(bcf_call_cmd)
     
    return LatchFile(str(variants_file), "latch:///variants.vcf")


@workflow
def variant_caller (ACC: str, SRR: str) -> (LatchFile):
    """ Input a genbank accession number for reference genome; Fetch ref genome. Input SRR number to Fetch sequencing reads using fastq dump.   Uses bcf tools to find vrariants and generate a variants.vcf file.
        
   

    Variant Caller
    ----

    Variant_caller takes a genbank accession number for a reference genome and and sra accession number (e.g. SRR #) 
    from a sequencing experiment and returns a VCF file cataloguing the detected variants.
    
    * Works for haploid genomes (e.g. viruses, bacteria)

    * The code used to run this analysis is adapted from the Biostar Handbook (by Istvan Albert).
    

    __metadata__:
        display_name: Variant Caller
        author:
            name:  Ken Saville
            email: ksaville@albion.edu
            github repository: coming soon
        license:
            id: MIT
    Args:

        ACC:
          Accession number for reference genome test use AP018036 (this is the mucobacterium tuberculosis run)
          
          
          __metadata__:
            display_name: ACC
       
        SRR:
          SRA number for sequencing reads
          to test use SRR19576437 - 
          this is a sequencing run of M. Tb from Asian elephants
          Just used as an example to show that vcf file with snps is generated 
          
          __metadata__:

            display name: SRR
      
    """
    
    return call_variants(ACC=ACC, SRR=SRR)

