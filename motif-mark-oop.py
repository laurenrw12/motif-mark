#!/usr/bin/env python
import argparse
import cairo
import re

def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-f", help="Name of fasta file", required=True, type=str)
    parser.add_argument("-m", help="Name of motifs file", required=True, type=str)
    return parser.parse_args() 

args = get_args()
f = args.f
m = args.m

####################
# Global Variables #
####################

FEATURE_HEIGHT = 25
VALUE_TO_CENTER = 50
GENE_GROUP_HEIGHT = 100

COLOR_LIST = [(255/255,0/255,0/255), (0/255,32/255,255/255), (0/255,192/255,0/255), (160/255,32/255,255/255), (255/255,160/255,16/255)] #[red,blue,green,purple,orange]

IUPAC = {
    "U":"[TU]",
    "W":"[ATU]",
    "S":"[CG]",
    "M":"[AC]",
    "K":"[GTU]",
    "R":"[AG]",
    "Y":"[CTU]",
    "B":"[CGTU]",
    "D":"[AGTU]",
    "H":"[ACTU]",
    "V":"[ACG]",
    "N":"[ACGTU]",
}

###########
# Classes #
###########

class Gene:
    def __init__(self, start, end, gene_name, gene_num):
        '''This is how a Gene is made.'''
        ## Data ##
        self.start = start
        self.end = end
        self.gene_name = gene_name
        self.gene_num = gene_num

    def draw(self, context):
        #draw line
        context.set_source_rgb(0, 0, 0) #Solid black
        context.set_line_width(1)
        y = (GENE_GROUP_HEIGHT * self.gene_num) + VALUE_TO_CENTER*2
        context.move_to(self.start + VALUE_TO_CENTER, y)        #(x,y)
        context.line_to(self.end + VALUE_TO_CENTER, y)      #(ending x, ending y)
        context.stroke()

        #write header
        context.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(10)
        context.move_to(GENE_GROUP_HEIGHT/5, y - VALUE_TO_CENTER/2)
        context.show_text(self.gene_name)

class Exon:
    def __init__(self, start, end, gene_num):
        '''This is how a Exon is made.'''
        ## Data ##
        self.start = start
        self.end = end
        self.gene_num = gene_num

    def draw(self, context):
        context.set_source_rgb(0, 0, 0) #Solid black
        y = (GENE_GROUP_HEIGHT * self.gene_num) + VALUE_TO_CENTER/2
        context.rectangle(self.start + VALUE_TO_CENTER, y + VALUE_TO_CENTER*1.25, self.end - self.start, FEATURE_HEIGHT)        #(x0,y0,x1,y1) (moves left to right, moves up and down, width of box, height of box)
        context.fill()

class Motif:
    def __init__(self, start, end, gene_num, color):
        '''This is how a Motif is made.'''
        ## Data ##
        self.start = start
        self.end = end
        self.color = color 
        self.gene_num = gene_num

    def draw(self, context):
        context.set_source_rgb(self.color[0], self.color[1], self.color[2]) 
        y = (GENE_GROUP_HEIGHT * self.gene_num) + VALUE_TO_CENTER/2
        print(self.start)
        context.rectangle(self.start + VALUE_TO_CENTER, y + VALUE_TO_CENTER*1.25, self.end - self.start, FEATURE_HEIGHT)        #(x0,y0,x1,y1) (moves left to right, moves up and down, width of box, height of box)
        context.fill()

#############
# Functions #
#############

def find_exon(sequence: str) -> tuple:
    '''Takes a DNA sequence (index) and returns two integers as the starting and ending location of the exon.'''
    for i in range(len(sequence)):
        if sequence[i].isupper():
            start = int(i)
            break
    
    for i in range(start, len(sequence)): 
        if sequence[i].islower():
            end = int(i) 
            break

    return (start, end)

def possible_motifs(motif: str) -> str:
    '''DOC STRING'''
    motif = motif.upper()

    for ambiguous_nucleotide, possible_nucleotides in IUPAC.items(): 
        motif = motif.replace(ambiguous_nucleotide, possible_nucleotides) 

    return motif

######################
# Read Through Files #
######################

# read through fasta file and create fasta_dict
fasta_dict:dict = {}
with open(f, "r") as fr:
    while True:
        line = fr.readline().strip()

        if line == "":
            break

        if line.startswith(">"):
            header = line
            fasta_dict[header] = ""

        else: 
            fasta_dict[header] += line

# read through motif file and create motif dict
motif_dict = {}
with open(m, "r") as mr:
    while True:
        line = mr.readline().strip()

        if line == "":
            break

        motif_dict[line] = possible_motifs(line)


################################
# Create Initial Image Surface #
################################

#get width of image surface 
longest_seq = 0
for fasta in fasta_dict: 
    if len(fasta_dict[fasta]) > longest_seq:
        longest_seq = len(fasta_dict[fasta])
width = longest_seq + VALUE_TO_CENTER*2 + 125

#get height of image surface 
height = (GENE_GROUP_HEIGHT * len(fasta_dict)) + 50

#create image surface 
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
context = cairo.Context(surface)
context.set_source_rgb(1, 1, 1) #white 
context.paint()

#########################################
# Add Genes, Exons, and Motifs to Image #
#########################################

for i, header in enumerate(fasta_dict): 
    gene = Gene(0, len(fasta_dict[header]), header, i)
    gene.draw(context)

    #find start and end of exon 
    (start, end) = find_exon(fasta_dict[header])

    exon = Exon(start, end, i)
    exon.draw(context)

    for j, motif in enumerate(motif_dict):
        matches = re.finditer(motif_dict[motif], fasta_dict[header].upper())
        for match in matches:
            start = match.start()
            end = match.start() + len(match.group())
            motif = Motif(start, end, i, COLOR_LIST[j])
            motif.draw(context)

###############################
# Add Title & Legend to Image #
###############################

#set font and color
context.set_source_rgba(0,0,0) #black
context.select_font_face("Verdana", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

#write title
context.set_font_size(15)
context.move_to(25, 25)
context.show_text("Visualization of Motif Marks from " + args.f)
context.set_font_size(10)
context.move_to(25, 40)
context.show_text("Created By: Lauren Williams: 03-03-2025")

#write legend 
x = width - 125
context.set_font_size(10)
context.move_to(x, 25)
context.show_text("MOTIF LEGEND")

#draw boxes of colors and write out each motif name 
for i, motif in enumerate(motif_dict):
    context.set_source_rgb(COLOR_LIST[i][0], COLOR_LIST[i][1], COLOR_LIST[i][2])
    y = (i+1)*30 
    context.rectangle(x, y + 10, 15, 15)        #(x0,y0,x1,y1) (moves left to right, moves up and down, width of box, height of box)
    context.fill()

    context.set_font_size(10)
    context.move_to(x + 20, y + 20)
    context.show_text(motif)

###############
# Save to PNG #
###############

name = f.split(".")
surface.write_to_png(f"{name[0]}.png")