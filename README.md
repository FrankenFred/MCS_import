# MCS_import
Python code designed to interface with output files from the PLP-LIF system in 919. 
Used to import the Multi-Channel Scalar data, fitting with a single exponential, and fianlly collating all data arrays and fit coefficients into text output files.

Files read in are assumed "*.log" from LIF software.
  -Code assumes time bin is the same for each dataset. Importing files with different time bins WILL cause an error.

Output files are "*.txt" tab delimited:
  -"Fit_Coeffs.txt" contains fit coefficients
  -"Fit_uncert.txt" contains corresponding fit uncertainties
  -"DAT_summary.txt" contains collated raw data in one file


