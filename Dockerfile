
FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

# Its easy to build binaries from source that you can later reference as
# subprocesses within your workflow.


# Or use managed library distributions through the container OS's package
# manager.
#Install tools needed for variant analysis

RUN apt-get update -y &&\
    apt-get install -y autoconf samtools
    
RUN apt-get install -y bcftools

RUN apt-get install -y bwa

RUN apt-get install -y emboss

RUN apt-get install -y ncbi-entrez-direct

RUN apt-get install -y sra-toolkit

# You can use local data to construct your workflow image.  Here we copy a
# pre-indexed reference to a path that our workflow can reference.
#COPY data /root/reference
#ENV BOWTIE2_INDEXES="reference"

COPY wf /root/wf

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
