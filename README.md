[![travis](https://travis-ci.org/bjpop/barcode_analysis.svg?branch=master)](https://travis-ci.org/bjpop/barcode_analysis)

# Overview 

In the examples below, `$` indicates the command line prompt.

# Licence

This program is released as open source software under the terms of [MIT License](https://raw.githubusercontent.com/bjpop/barcode_analysis/master/LICENSE).

# Installing

Clone this repository: 
```
$ git clone https://github.com/bjpop/barcode_analysis
```

Move into the repository directory:
```
$ cd barcode_analysis
```

Barcode_analysis can be installed using `pip` in a variety of ways (`$` indicates the command line prompt):

1. Inside a virtual environment:
```
$ python3 -m venv barcode_analysis_dev
$ source barcode_analysis_dev/bin/activate
$ pip install -U /path/to/barcode_analysis
```
2. Into the global package database for all users:
```
$ pip install -U /path/to/barcode_analysis
```
3. Into the user package database (for the current user only):
```
$ pip install -U --user /path/to/barcode_analysis
```


# General behaviour


## Help message

Barcode_analysis can display usage information on the command line via the `-h` or `--help` argument:

```
$ barcode_analysis -h
```


## Logging

If the ``--log FILE`` command line argument is specified, barcode_analysis will output a log file containing information about program progress. The log file includes the command line used to execute the program, and a note indicating which files have been processes so far. Events in the log file are annotated with their date and time of occurrence. 

```
$ barcode_analysis --log bt.log file1.fasta file2.fasta 
# normal barcode_analysis output appears here
# contents of log file displayed below
```
```
$ cat bt.log
12/04/2016 19:14:47 program started
12/04/2016 19:14:47 command line: /usr/local/bin/barcode_analysis --log bt.log file1.fasta file2.fasta
12/04/2016 19:14:47 Processing FASTA file from file1.fasta
12/04/2016 19:14:47 Processing FASTA file from file2.fasta
```

# Exit status values

Barcode_analysis returns the following exit status values:

* 0: The program completed successfully.
* 1: File I/O error. This can occur if at least one of the input FASTA files cannot be opened for reading. This can occur because the file does not exist at the specified path, or barcode_analysis does not have permission to read from the file. 
* 2: A command line error occurred. This can happen if the user specifies an incorrect command line argument. In this circumstance barcode_analysis will also print a usage message to the standard error device (stderr).


# Testing

# Bug reporting and feature requests

Please submit bug reports and feature requests to the issue tracker on GitHub:

[barcode_analysis issue tracker](https://github.com/bjpop/barcode_analysis/issues)
