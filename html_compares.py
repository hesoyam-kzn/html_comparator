import subprocess, os
from sys import argv

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
        a = subprocess.run([winmerge_path, p1, p2, "/t", "Webpage"])
    elif all(".json" in line for line in [p1, p2]):
        a = subprocess.run([winmerge_path, p1, p2])
    #b = subprocess.run([winmerge_path, path1, path2, "/or", "C:/TMP/report.html", "/noninteractive", ])
    #TODO: ебани ответ по коду возврата если нет никакого диффа, чтобы юзер в комстроке это явно увидел

if __name__ == "__main__":
    mode_cmd = True
    if len(argv) < 2:
        mode_cmd = False
    if mode_cmd:
        path1, path2 = argv[1].replace("\\", "/"), argv[2].replace("\\", "/")
    if mode_cmd:
        b = report_diff(path1, path2)
    # This text is shown even when you call comparisson from aside. MB there is a way to show it only if html_compares.py is running itself and report_diff is not called from another .py?
    # else:
    #     print("Please restart and provide two paths for validation reports. Available income extensions: .html and .json.\n" \
    #     "Example: html_compares.py 'E:/report1.html' 'E:/report2.html'")