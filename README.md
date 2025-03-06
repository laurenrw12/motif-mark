# motif-mark 
Lauren Williams
March 2025

## Overview
motif-mark is a object oriented, python program that visualizes motifs and exons on a gene. The tool takes a fasta file and a motif text file with each motif on a separate line, and generates a .png figure illustrating where motifs were identified in each fasta record. An example figure is shown below:

![example image](https://github.com/laurenrw12/motif-mark/blob/main/Figure_1.png)

Genes are represented by black lines, exons are represented by black boxes, and different motifs are represented by different colored boxes.

## Details
The input fasta file should follow convention, with a FASTA definition line (beginning with a carat ">" and a unique sequence identifier) followed by one or more lines of the nucleotide sequence.

The input motif file should contain up to five motifs with one motif per line that is less than or equal to 10 bases. Motifs should be written using IUPAC notation, which includes nucleobases represented by A, T, C, and G, as well as eleven ambiguity characters representing every possible combination of the four DNA bases. Ambiguous motifs are handled within this tool.

The output of this tool is a .png file containing the pycairo figure. The output file will follow the same naming convention as the fasta file. For example, ["Figure_1.fasta"](https://github.com/laurenrw12/motif-mark/blob/main/Figure_1.txt) will output ["Figure_1.png"](https://github.com/laurenrw12/motif-mark/blob/main/Figure_1.png).

## Installation and Usage
To use motif-mark, the user will need [```motif-mark-oop.py```](https://github.com/laurenrw12/motif-mark/blob/main/motif-mark-oop.py), a fasta file, a motif text file, and the appropriate conda environment.

Conda Environment:
This program is set to run in an environment called my_pycairo. The only package installed and necessary in this environment is pycairo.

Using ```motif-mark.py -f <absolute path to fasta file> -m <absolute path to motif file>```:

**-f**: The fasta file containing gene records. The absolute path to the fasta file is required for the script to run.

**-m**: The motif text file containing one motif per line. The absolute path to the motif file is required for the script to run.
