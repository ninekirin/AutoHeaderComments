#!/usr/bin/python
# Auto Header Comments Adder
# --------------------------------------------------------
# Descriptions: The script is aimed to add the comments
#               in the first few lines of the source code
#               in order to meet the homework requirements
# Author:       Kirin
# Date:         2022/04/16
# --------------------------------------------------------
# Updates:
# 2022/04/16:   Initial version
# 2022/05/23:   Added support for Java Project, changed the "simulate" to "test"
# --------------------------------------------------------

# Import

import os
import re
import argparse
import logging

# Environment Variables

C_HEADERCOMMENTS = """/*
 ============================================================================
 Name        : *file_name
 Author      : *student_id
 Version     : 0.1
 Copyright   : COPTLEFT
 Description : *code_type *week_id, Task *task_id
 ============================================================================
 */\n\n"""

JAVA_HEADERCOMMENTS = """/*
 ============================================================================
 Name        : *file_name
 Author      : *student_id
 Description : *code_type *task_id, Question *question_id, *pure_file_name class
 ============================================================================
 */\n\n"""

OS_HEADERCOMMENTS = """/*
 ============================================================================
 Name        : *file_name
 Author      : *student_id
 Description : *code_type *exercise_id, part *pure_file_name
 ============================================================================
 */\n\n"""

stuLTRdict = {"k": "15", "l": "16", "m": "17", "n": "18", "p": "19", "q": "20", "r": "21", "s": "22", "t": "23", "u": "24", "v": "25", "w": "26", "x": "27", "y": "28", "z": "29"}
stuIDdict = {v : k for k, v in stuLTRdict.items()}

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

# 使用FileHandler输出到文件
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# 使用StreamHandler输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

def convertNumberToLetter(student_id) -> str:
    """
    Converts a letter based student ID to a number based student ID
    in the format of "A#########"
    where A is the year of the student's enrollment
    and # is the student ID.

    Example:
    convertToNumber("2100000000") -> "R100000000"
    """
    return stuIDdict[student_id[:2]] + student_id[1:]

def convertLetterToNumber(student_id) -> str:
    """
    Converts a number based student ID to a letter based student ID
    in the format of "##########"
    where # is the student ID.

    Example:
    convertToNumber("R100000000") -> "2100000000"
    """
    return stuLTRdict[student_id[:1].lower()] + student_id[2:]

def get_file_header(file_path, lines):
    file_header = ""
    with open(file_path, "r") as f:
        for _ in range(lines):
            file_header += f.readline()
    return file_header

def delete_file_header(file_path, lines):
    with open(file_path, "r") as f:
        a = f.readlines()
    with open(file_path, "w") as f:
        f.write(''.join(a[lines:]))

def get_comments(file_name, file_path, code_type, code_lang) -> str:
    if code_lang == "Java":
        file_header = JAVA_HEADERCOMMENTS
        fetched_info = file_path.replace("\\", "/").split("/")
        for item in fetched_info:
            txt = re.search(r'Lab[0-9]+_[0-9]{10}|Assignment[0-9]+_[0-9]{10}|Project_[0-9]{10}', item, re.I)
            if hasattr(txt, "group"):
                infos = txt.group().split("_")
                file_header = file_header.replace("*code_type", f"{code_type}")
                file_header = file_header.replace("*task_id", infos[0].replace(f"{code_type}", ""))
                file_header = file_header.replace("*student_id", infos[1])
            txt2 = re.search(r"Question[0-9]+", item)
            if hasattr(txt2, "group"):
                file_header = file_header.replace("*question_id", txt2.group().replace("Question", ""))
        file_header = file_header.replace("*pure_file_name", file_name.split(".")[0])
        file_header = file_header.replace("*code_type", code_type)
    elif code_lang == "C":
        file_header = C_HEADERCOMMENTS
        # Lab
        if (code_type == "Lab" and re.search(r"^[A-Z][0-9]+[A-Z][0-9]+[A-Z][0-9]{9}(.*)\.c$", file_name, re.I)):
            week_id = re.search(r'W[0-9]+', file_name, re.I).group().replace("w", "W")
            file_header = file_header.replace("*week_id", week_id.replace("W", ""))
            task_id = re.search(r'T[0-9]+', file_name, re.I).group().replace("t", "T")
            file_header = file_header.replace("*task_id", task_id.replace("T", ""))
            student_id = re.search(r'[A-Z][0-9]{9}', file_name, re.I).group().replace("r", "R")
            file_header = file_header.replace("*student_id", convertLetterToNumber(student_id))
            file_header = file_header.replace("*code_type", "Week")
        # Assignment
        if (code_type == "Assignment" and re.search(r"^[A-Z][0-9]+[A-Z][0-9]+_[A-Z][0-9]{9}(.*)\.c$", file_name, re.I)):
            week_id = re.search(r'A[0-9]+', file_name, re.I).group().replace("a", "A")
            file_header = file_header.replace("*week_id", week_id.replace("A", ""))
            task_id = re.search(r'T[0-9]+', file_name, re.I).group().replace("t", "T")
            file_header = file_header.replace("*task_id", task_id.replace("T", ""))
            student_id = re.search(r'[A-Z][0-9]{9}', file_name, re.I).group().replace("r", "R")
            file_header = file_header.replace("*student_id", convertLetterToNumber(student_id))
            file_header = file_header.replace("*code_type", "Assignment")
    elif code_lang == "OS":
        # Hands-on Exercises
        # Path Structure: ../COMP3033/Hands-on Exercises/Exercise 1/..
        # FileName Rule: pure_file_name.extension
        file_header = OS_HEADERCOMMENTS
        fetched_info = file_path.replace("\\", "/").split("/")
        if code_type == "Hands-on Exercises" or code_type.to_lower() == "hoe":
            code_type = "Hands-on Exercises"
            for item in fetched_info:
                txt = re.search(r'Exercise [0-9]+', item)
                if hasattr(txt, "group"):
                    file_header = file_header.replace("*exercise_id", txt.group().replace("Exercise ", ""))
        file_header = file_header.replace("*pure_file_name", file_name.split(".")[0])
        file_header = file_header.replace("*code_type", code_type)



    file_header = file_header.replace("*file_name", file_name)
    return file_header

def run(code_type, code_lang, folder, force_replace, test_run) -> bool:
    # Get the path of the file
    if not code_type:
        logging.error("Please provide the code type!")
        exit()
    if not code_lang:
        logging.error("Please provide the code language!")
        exit()
    if not folder:
        folder = os.getcwd()
    logging.info("Current Language: " + code_lang)
    logging.info("Current Code Type: " + code_type)
    logging.info("Current Folder: " + folder)
    if not os.path.exists(folder):
        logging.info("Folder does not exist!")
        exit()
    oswalk = os.walk(folder)
    # Iterate through folders to find the .{code_lang} files
    for file_path, _dir_list, file_list in oswalk:
        for file_name in file_list:
            print(file_name)
            # matched_file = re.search(rf"^(.*)\.{code_lang}$", file_name, re.I)
            if code_lang == "Java":
                matched_file = re.match(r"^(.*)\.java$", file_name, re.I)
            elif code_lang == "C":
                matched_file = re.match(r"^(.*)\.c$", file_name, re.I)
            elif code_lang == "OS":
                matched_file = re.match(r"^(.*)\.(.*)$", file_name, re.I)
            if matched_file:
                logging.info(f"Found {code_lang} file: {file_name} in {file_path}")
                logging.info("Generated comments: " + get_comments(file_name, file_path, code_type, code_lang))
                file_header = get_file_header(os.path.join(file_path, file_name), 9 if code_lang == "C" else 7)
                comment_exists = re.search(r"\/\*(\s|.)*?\*\/", file_header, re.I)
                if comment_exists:
                    original_comments = get_file_header(os.path.join(file_path, file_name), 9 if code_lang == "C" else 7)
                    logging.info(f"Comments already exist in {file_name}")
                    if force_replace:
                        logging.info(f"***Force replacing comment in {file_name}***!")
                        if not test_run:
                            delete_file_header(os.path.join(file_path, file_name), 9 if code_lang == "C" else 7)
                            with open(os.path.join(file_path, file_name), "r+") as f:
                                old = f.read()
                                f.seek(0)
                                f.write(get_comments(file_name, file_path, code_type, code_lang))
                                f.write(old)
                    logging.info("The original comment is " + original_comments)
                else:
                    logging.info("Adding comment in " + file_name)
                    if not test_run:
                        with open(os.path.join(file_path, file_name), "r+") as f:
                            old = f.read()
                            f.seek(0)
                            f.write(get_comments(file_name, file_path, code_type, code_lang))
                            f.write(old)

def main():
    logger.addHandler(ch)
    logger.addHandler(fh)
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", required=True, help="specifies the code type")
    parser.add_argument("-l", "--lang", required=True, help="specifies the code language")
    parser.add_argument("-f", "--folder", help="specifies the folder the script iterate")
    parser.add_argument("-force", "--forcereplace", action='store_true', help="force replace existing comments")
    parser.add_argument("-test", "--testrun", action='store_true', help="test run (does not actually write files)")
    args = parser.parse_args()
    run(args.type, args.lang, args.folder, args.forcereplace, args.testrun)

if __name__ == "__main__":
    main()