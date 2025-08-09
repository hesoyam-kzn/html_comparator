import json
from sys import argv

origin = argv[1].replace("\\", "/")
print(origin)
# origin = r'{origin}'.replace("\\", "/")
listos = {"Ammounts": {"Errors": 0, "Warnings": 0, "Notices": 0}, "Error": [], "Warning": [], "Notice": []}

with open(origin, encoding="utf-8") as inp_f, open("clipboard.json", "w", encoding="utf-8") as out_f:
    a = [l.rstrip() for l in inp_f.readlines()]
    for i in a:
        tmp_list = list(map(lambda x: x.replace("[", "").replace("]", "") if x != i[4] else i[4], i.split("\t")))
        if "Error" in tmp_list:
            listos["Error"].append({"Scenario": tmp_list[1], "Source": tmp_list[3], "Description": tmp_list[4]})
        elif "Warning" in tmp_list:
            listos["Warning"].append({"Scenario": tmp_list[1], "Source": tmp_list[3], "Description": tmp_list[4]})
        elif "Notice" in tmp_list:
            listos["Notice"].append({"Scenario": tmp_list[1], "Source": tmp_list[3], "Description": tmp_list[4]})
    
    listos["Error"] = sorted(listos["Error"], key=lambda x: (x["Scenario"], x["Description"]))
    listos["Warning"] = sorted(listos["Warning"], key=lambda x: (x["Scenario"], x["Description"]))
    listos["Notice"] = sorted(listos["Notice"], key=lambda x: (x["Scenario"], x["Description"]))
    listos["Ammounts"]["Errors"] = len(listos["Error"])
    listos["Ammounts"]["Warnings"] = len(listos["Warning"])
    listos["Ammounts"]["Notices"] = len(listos["Notice"])
    b = json.dump(listos, out_f, indent="\t")