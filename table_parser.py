#!/usr/bin/python

import sys
import latex_table
from syst_calculator import SystDictionary, SystCalculator
import dict_to_file


if __name__ == "__main__":
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the LaTeX input file to be parsed")

    # Add two mutually exclusive arguments: grouped/ungrouped
    parser_grouped = parser.add_mutually_exclusive_group()
    parser_grouped.add_argument("--grouped", help="group systematics", action="store_true")
    parser_grouped.add_argument("--ungrouped", help="do *not* group systematics", action="store_false")

    # Add optional arguments for file output
    parser.add_argument("--json", dest="json_file", help="output a JSON file")
    parser.add_argument("--tex", dest="tex_file", help="output a LaTeX file")

    args = parser.parse_args()


    # ======================================================
    # Start the main execution here
    # ======================================================

    # Retrieve the table from the input file, save all columns it
    # contains, and store all entries as a dictionary.
    table = latex_table.readFromLatex(args.input)
    columns = table.getColumns()
    table = table.getEntries()

    # Load a JSON dictionary that contains all possible systematics
    # and which group they belong to (for look-up).
    syst_dict = SystDictionary("syst_dictionary.json")
    grouped_table = SystCalculator(table, syst_dict, columns).calcSystematics()

    # If we want grouped data, overwrite our initial table.
    if args.grouped:
        table = grouped_table

    if args.json_file:
        dict_to_file.storeJSON(table, args.json_file)
    if args.tex_file:
        dict_to_file.storeTEX(table, args.tex_file)

    for row in table:
        for column in table[row]:
            print "%s \t %s \t %s" % (row, column, table[row][column])
