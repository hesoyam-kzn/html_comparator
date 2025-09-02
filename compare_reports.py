import subprocess, os
from sys import argv
from parse_html import parse_html
import json

# This function creates diff_report.txt file, where new and missing errors comparing to an ethalon are listed
def txt_reporter(doc1, doc2):
    lacking_issues, new_issues = {"Error": [], "Warning": [], "Notice": []}, {"Error": [], "Warning": [], "Notice": []}
    with open("diff_report.txt", "w", encoding="utf-8") as inp1, open(doc1, "r", encoding="utf-8") as pr1, open(doc2, "r", encoding="utf-8") as pr2:
            l_doc = json.load(pr1)
            r_doc = json.load(pr2)
            for i in list(l_doc.keys())[1:]:
                for j in l_doc[i]:
                    if j not in r_doc[i]:
                        lacking_issues[i].append(j)
            for j in list(r_doc.keys())[1:]:
                for l in r_doc[j]:
                    if l not in l_doc[j]:
                        new_issues[j].append(l)
            inp1.write("Issues which are missing:\n\n")
            for b in ["Error", "Warning", "Notice"]:
                if len(lacking_issues[b]) != 0:
                    inp1.write(f"\n{b} ({len(lacking_issues[b])} issue(s)):\n")
                    for k in lacking_issues[b]:
                        inp1.write(f"\t[{k['Scenario']}] [{k['Source']}] {k['Description']}" + "\n")
            inp1.write("\n\nNew issues:\n")
            for b in ["Error", "Warning", "Notice"]:
                if len(new_issues[b]) != 0:
                    inp1.write(f"\n{b} ({len(new_issues[b])} issue(s)):\n")
                    for k in new_issues[b]:
                        inp1.write(f"\t[{k['Scenario']}] [{k['Source']}] {k['Description']}" + "\n")

# Main function, which converts (if needed) htmls into jsons and shows winmerge with calling txt_reporter function after to write report
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
        # conversion_need = (False if input("\nYou've sent 2 htmls, choose how to work with them:\n"
        #                          "1 \x1b[96m(Default)\x1b[0m - Convert to .json and compare after\n"
        #                          "2 - Compare two htmls\nYour choice: ") == "2" else True)
        # if conversion_need:
        left = parse_html(p1, "report_left.json") 
        right = parse_html(p2, "report_right.json")
        txt_reporter(left, right)
        subprocess.run([winmerge_path, left, right])
            
        # else:
        #     subprocess.run([winmerge_path, p1, p2, "/t", "Webpage"])
    elif all(".json" in line for line in [p1, p2]):
        txt_reporter(p1, p2)
        subprocess.run([winmerge_path, p1, p2])
    else:
        input("\x1b[31mERROR\x1b[0m\nExtensions for provided paths were not equal. Expected 2 .html or 2 .json\n"
              "Example: html_compares.py 'E:/report1.html' 'E:/report2.html'")
        # return
    print("Compare has been completed. Check opened winmerge or 'diff_report.txt'")

if __name__ == "__main__":
    if len(argv) == 3:
        path1, path2 = argv[1].replace("\\", "/"), argv[2].replace("\\", "/")
        b = report_diff(path1, path2)
    else:
        input("\x1b[31mERROR\x1b[0m\n Please restart and provide two paths for validation reports with the same extensions.\n"
              "Available income extensions: .html and .json.\n"
              "Example: html_compares.py 'E:/report1.html' 'E:/report2.html'")