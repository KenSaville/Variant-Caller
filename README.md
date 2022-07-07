# Variant-Caller
A Latch Bio workflow to call DNA sequence variants

In this workflow the user inputs a genbank accession number referring to the appropriate reference genome and an SRR number referring to a particular DNA sequencing run.  The bcf tools are then implemeneted to identify variants and generate a variant.vcf file.  This file along with the ref genome fasta file can be loaded into igv or other visualization tool to visualize variants. 

To test the workflow use

ACC:  AP0180 36 ( a M. tuberculosis genome)

and 

SRR: SRR19576437 ( asequencing run of Mt isolates from elephants)

These examples were eseentially chosen at random just to test the workflow. 

The CLI code underlying the workflow was adapted from the biostar handbook:  https://www.biostarhandbook.com/

