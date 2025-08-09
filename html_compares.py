import subprocess, os
from sys import argv
from html_parser import parse_html

def report_diff(p1, p2):
    winmerge_path = "C:/Program Files/WinMerge/WinMergeU.exe"
    #Checking if winmerge is installed on PC
    if os.path.isdir(winmerge_path.rstrip("WinMergeU.exe")):
        print("Running compare")
    else:
        #Asking for install or getting winmerge from non-default folder
        print(f"\x1b[31m[Log] [Error] Can't launch 'WinMerge' app from '{winmerge_path}'. Compare requires this app.\x1b[0m\n"
            "Please install it from 'https://winmerge.org/' and rerun script if you don't have it.\n"
            "Or provide a path to its executable if you have it installed to non-default folder.\n")
        while True:
            winmerge_path = input(f"\n\x1b[96mProvide 'WinMergeU.exe' path to proceed\x1b[0m \x1b[93m(Last path: '{winmerge_path}'):\x1b[0m ")
            if ("/" in winmerge_path) or ("\\" in winmerge_path):
                break
            else:
                print("Incorrect input, try again.")

    if all(".html" in line for line in [p1, p2]):
        conversion_need = (False if input("\nYou've sent 2 htmls, choose how to work with them:\n"
                                 "1 \x1b[96m(Default)\x1b[0m - Convert to .json and compare after\n"
                                 "2 - Compare two htmls\nYour choice: ") == "2" else True)
        if conversion_need:
            left, right = parse_html(p1, "report_left.json"), parse_html(p2, "report_right.json")
            a = subprocess.run([winmerge_path, left, right])
            return a.returncode
        else:
            a = subprocess.run([winmerge_path, p1, p2, "/t", "Webpage"])
            return a.returncode
    elif all(".json" in line for line in [p1, p2]):
        a = subprocess.run([winmerge_path, p1, p2])
        return a.returncode
    else:
        input("\x1b[31mERROR\x1b[0m\nExtensions for provided paths were not equal. Expected 2 .html or 2 .json\n"
              "Example: html_compares.py 'E:/report1.html' 'E:/report2.html'")
        # return

if __name__ == "__main__":
    if len(argv) == 3:
        path1, path2 = argv[1].replace("\\", "/"), argv[2].replace("\\", "/")
        b = report_diff(path1, path2)
        print(f'Returncode is {b}')
    else:
        input("\x1b[31mERROR\x1b[0m\n Please restart and provide two paths for validation reports with the same extensions.\n"
              "Available income extensions: .html and .json.\n"
              "Example: html_compares.py 'E:/report1.html' 'E:/report2.html'")