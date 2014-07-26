"""
Author: Eric J. Ma, written for Nichola J. Hill, PhD.
Affiliation: Massachusetts Institute of Technology

Purpose: This is the script used for cleaning influenza sequences of anything before 1977.

The input is a Nexus-format file with the dates present after the last "|" character.

The format of the dates can be: 
-	DD/MM/YYYY
-	MM/YYYY
-	YYYY

The outputs will be a Nexus-format file with anything prior to 1977 removed.

To run this program, in Terminal, type:

	python clean_before_1977.py <input_nexus_filename> <output_nexus_filename>

Do not include the "<" and ">" characters.
"""


from Bio import SeqIO

import sys

def read_sequences(infile):
	"""
	This function takes in a Nexus file's filename, and reads the sequences 
	into memory, returning a list of sequences.
	"""

	sequences = list(SeqIO.parse(infile, 'nexus'))

	return sequences

def clean_sequences(sequences):
	"""
	This function takes in a list of sequences, parses the year to check if 
	the year is after 1977 or not, and adds those that are after 1977 
	(inclusive) to a new list, and returns that new list.
	"""
	new_sequences = []
	for sequence in sequences:
		year = sequence.id.split('|')[-1]
		if len(year) == 10 or len(year) == 7:
			if int(year.split('/')[-1]) >= 1977:
				new_sequences.append(sequence)
		if len(year) == 4:
			if int(year) >= 1977:
				new_sequences.append(sequence)

	return new_sequences

def write_sequences(sequences, outfile):
	"""
	This function writes a list of sequences to disk. List of sequences and 
	output filename have to be specified.
	"""
	SeqIO.write(sequences, outfile, 'nexus')

if __name__ == "__main__":
	infile = sys.argv[1]
	outfile = sys.argv[2]
	print('Reading file %s' % infile)

	sequences = read_sequences(infile)
	print('Starting with %s sequences in %s.' % (len(sequences), infile))

	new_sequences = clean_sequences(sequences)
	print('Finished with %s sequences.' % len(new_sequences))

	print('Writing file as %s' % outfile)
	write_sequences(new_sequences, outfile)