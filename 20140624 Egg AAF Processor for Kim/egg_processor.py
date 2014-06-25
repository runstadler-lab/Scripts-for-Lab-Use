"""
Author: Eric J. Ma 
Affiliation: Massachusetts Institute of Technology

Purpose of this script:
Kimberly Davis (labmate) is going to compile AAF positives from the MIT 
samples that we have collected to date.

In the process of compiling, some samples will be discarded down to 1 sample, 
and others will be kept in full (all 5 samples); yet others may not have all 5 
tubes kept, some may have only 2, 3 or 4. The samples that are kept will have 
to be organized into a new "compiled" box. 

To streamline this process, this script was written to take in a CSV file of 
the samples to be kept, and output a list of where to put each new sample.

How to use this script:
	1. Place this script in the directory that contains the input file.

	2.Type in terminal:
	python egg_processor.py input_file.csv output_file.csv current_box 
		current_row current_col
	(NOTE: see INPUTS for definition of current_box, row and col)

	3. Look for output_file.csv in the same directory. 

INPUTS:
-	CSV file of the following structure (ensure that the column names 
	match up :
		(Sample ID, Tubes Collected, Date of Harvest)

		-	The "Tubes Collected" column is the number of tubes that have been 
			collected, which is any number between 1 and 5.
		-	The "Date of Harvest" column should be in the format DD-Month-YY

-	Name of the output file, which has to be a CSV file.

-	Current position of last tube. It should be of the format:
		(Box # (integer), Row (letter), Column (integer))

		(NOTE: see get_next_box_position() for range of letters available for 
			Row and Column)

OUTPUTS:
-	CSV file of the following structure:
		(Sample ID [with "Tube x of total" appended], Date of Harvest, Box, 
		Row, Column)
"""

import pandas as pd
import sys

def get_next(iterable, current_element):
	"""
	This method gets the next position in the iterable. If the position is the 
	last one, it will recurse back to the beginning.
	"""
	if current_element in iterable:
		index = iterable.index(current_element)

		if index == len(iterable) - 1:
			next_index = 0
		else:
			next_index = index + 1

		return iterable[next_index]
	
	else:
		raise ValueError("element %s not in iterable %s" % (current_element, iterable))

def get_next_box_position(current_box, current_row, current_col, ):
	"""
	We assume that each box has 9 rows and 9 columns. The rows are letters A->
	I, the columns are numbers 1->9,and boxes are continuous integers starting 
	at 1 through to infinity.
	
	For the very first samples to be added in, we have a hard-coded 
	conditional. The input required for this is box=1 row=A col=0.
	"""
	rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
	cols = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	
	
	if current_box == 1 and current_row == 'A' and current_col == 0:
		new_box = 1
		new_row = 'A'
		new_column = 1
		
		return (new_box, new_row, new_column)
		
		pass
	
	else:
		new_column = get_next(cols, current_col)
	

	
	if new_column == 1:
		new_row = get_next(rows, current_row)
	else:
		new_row = current_row
		
	if (current_row, current_col) == ('I', 9):
		new_box = current_box + 1
		
	else:
		new_box = current_box
		
	return (new_box, new_row, new_column)


def generate_sample_box_pos_list(current_box, current_row, current_col, \
	filename):

	"""
	This generates a list of tuples based on the input spreadsheet.
	"""
	
	new_samples = []
	infile = pd.read_csv(filename)
	for row in infile.iterrows():
		sample_id = row[1]['Sample ID']
		tubes_collected = row[1]['Tubes Collected']
		date_of_harvest = row[1]['Date of Harvest']
		for i in range(tubes_collected):
			new_box, new_row, new_col = get_next_box_position(current_box, \
				current_row, current_col)
			tube_number = str(i+1) + " of " + str(tubes_collected)
			new_samples.append((sample_id, tube_number, date_of_harvest, \
				new_box, new_row, new_col))

			current_box = new_box
			current_row = new_row
			current_col = new_col
			
	return new_samples

def generate_sample_box_pos_df(box_pos_list):
	"""
	This method generates a pandas DataFrame of the sample_box_pos_list. 
	"""
	new_df = pd.DataFrame(box_pos_list)
	new_df.columns = ['Sample ID', 'Tube Number', 'Date of Harvest', 'Box', \
	'Row', 'Column']
	
	return new_df


if __name__ == "__main__":
	infile = sys.argv[1]
	outfile = sys.argv[2]
	current_box = int(sys.argv[3])
	current_row = str(sys.argv[4])
	current_col = int(sys.argv[5])

	print infile, outfile, current_box, current_row, current_col

	new_samples = generate_sample_box_pos_list(current_box, current_row, \
		current_col, infile)

	new_df = generate_sample_box_pos_df(new_samples)

	new_df.to_csv(outfile)