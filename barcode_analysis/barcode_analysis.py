'''
Module      : Main
Description : The main entry point for the program.
Copyright   : (c) Bernie Pope, 31 Dec 2018 
License     : MIT 
Maintainer  : bjpope@unimelb.edu.au 
Portability : POSIX

'''

from argparse import ArgumentParser
import sys
import logging
import pkg_resources
import pysam
from Bio import SeqIO
import gzip
import csv


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
DEFAULT_VERBOSE = False
PROGRAM_NAME = "barcode_analysis"


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.

    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    logging.error(message)
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    description = 'Read one or more FASTA files, compute simple stats for each file'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        '--coords',
        type=str,
        help='File containing coordiates of genomic regions in bed format')
    parser.add_argument(
        '--barcodes',
        type=str,
        help='File containing read barcodes in FASTQ format')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--log',
                        metavar='LOG_FILE',
                        type=str,
                        help='record program progress in LOG_FILE')
    parser.add_argument('bam_file',
                        metavar='BAM_FILE',
                        type=str,
                        help='Input BAM file')
    return parser.parse_args()


def init_logging(log_filename):
    '''If the log_filename is defined, then
    initialise the logging facility, and write log statement
    indicating the program has started, and also write out the
    command line from sys.argv

    Arguments:
        log_filename: either None, if logging is not required, or the
            string name of the log file to write to
    Result:
        None
    '''
    if log_filename is not None:
        logging.basicConfig(filename=log_filename,
                            level=logging.DEBUG,
                            filemode='w',
                            format='%(asctime)s %(levelname)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S')
        logging.info('program started')
        logging.info('command line: %s', ' '.join(sys.argv))


def read_barcodes(filename):
    barcodes = {}
    with gzip.open(filename, "rt") as file:
        for seq in SeqIO.parse(file, "fastq"):
            barcodes[seq.id] = str(seq.seq)
    return barcodes


def read_coords(filename):
    coords = {}
    with open(filename) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if len(row) == 4:
                chrom, start, end, name = row
                coords[(chrom, int(start), int(end))] = name
    return coords 


header = "NAME,NUM_READS,NUM_BARCODES,NUM_BARCODES/NUM_READS,NUM_HITS,NUM_MISSES"


def read_bam(barcodes, coords, filename):
    samfile = pysam.AlignmentFile(filename, "rb")
    print(header)
    barcode_sequences = {}
    count = 0
    for (chrom, start, end), name in coords.items():
        seen_barcodes = set() 
        for read in samfile.fetch(chrom, start, end):
            this_seq = read.query_sequence
            this_id = read.query_name
            if this_id in barcodes:
                this_barcode = barcodes[this_id]
            if this_barcode not in barcode_sequences:
                barcode_sequences[this_barcode] = set()
            barcode_sequences[this_barcode].add(this_seq)
            count += 1
            if count >= 100000:
                break
    for barcode, seqs in barcode_sequences.items():
        print("{}".format(barcode))
        for s in seqs:
            print(s)

        #num_barcodes = len(seen_barcodes)
        #print("{},{},{},{},{},{}".format(name, num_reads, num_barcodes, num_barcodes/num_reads, num_hits, num_misses))
                


def main():
    "Orchestrate the execution of the program"
    options = parse_args()
    init_logging(options.log)
    barcodes = read_barcodes(options.barcodes)
    coords = read_coords(options.coords)
    read_bam(barcodes, coords, options.bam_file)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
