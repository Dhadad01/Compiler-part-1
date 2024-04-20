import glob
import os
import sys
import re

COMPARE_EXTENSION = '.cmp'

from JackAnalyzer import analyze_file


def run_files_in_folder(folder_path):
    assert os.path.isdir(folder_path)
    print("Testing folder:", os.path.basename(folder_path), end=' ')

    files_to_assemble = [
        os.path.join(folder_path, filename)
        for filename in os.listdir(folder_path)]
    countfalse = 0
    counter = 0
    all_true = True

    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".jack":
            continue
        counter += 1

        output_path = filename + ".xml"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            try:
                analyze_file(input_file, output_file)
            except:
                print("\n!!! Error while analyzing file:", input_path)
                raise
        remove_tabs(output_path + COMPARE_EXTENSION)
        this_true = compare_files(output_path, output_path + COMPARE_EXTENSION)
        if not this_true:
            countfalse += 1
        all_true = all_true and this_true

    print(f"{counter} files found: Comparison is {all_true}, found {countfalse} wrong files")


def remove_tabs(cmp_file):
    # first get all lines from file
    with open(cmp_file, 'r') as f:
        lines = f.readlines()

    # remove spaces
    new_line =[]
    ch = '<'
    # The Regex pattern to match al characters on and before '-'
    pattern = ".*" + ch
    # Remove all characters before the character '-' from string
    for line in lines:
        new_line.append(line[del_str(line):])

    # finally, write lines in the file
    with open(cmp_file, 'w') as f:
        f.writelines(new_line)


def del_str(line):
    for i in range(len(line)):
        if line[i] == '<':
            return i


def compare_files(our_path, compare_path):
    if open(our_path, 'r').read() != open(compare_path, 'r').read():
        print("\nDifference in file:", our_path)
        return False
    return True


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 3:
        sys.exit("Invalid usage, please use: run_tests <d|f> <input path>")
    assert sys.argv[1] in ['d', 'f']

    argument_path = os.path.abspath(sys.argv[2])
    assert os.path.isdir(argument_path)

    if sys.argv[1] == 'f':
        run_files_in_folder(argument_path)
    else:
        for dirpath in glob.glob(os.path.join(argument_path, '*')):
            if os.path.isdir(dirpath) and os.path.basename(dirpath)[0] not in ['.', '_']:
                run_files_in_folder(dirpath)
