import json
from sys import argv
import os

def parse_html(html_path, parsed_report_path):
    print(f'Processing {html_path}')
    if ".html" not in html_path:
        input("\nArgument provided is not a .html report. Expected .html. Try again with correct parameter.\n"
              "Example: html_parser.py 'E:/report1.html'")
        return
    issue_types = {"Ammounts": {"Errors": 0, "Warnings": 0, "Notices": 0}, "Error": [], "Warning": [], "Notice": []}
    issues = []

    # Working with passed html path
    with open(html_path, "r", encoding="utf-8") as inp:
        raw_html = inp.read()
        header = raw_html[raw_html.index("<tr>"):raw_html.index("</table>")]
        
        # Gathering issues count from the report's header
        header = header.replace('<tr><th id="col_info">', '').replace('</td></tr>', '')\
            .replace('</th><td>', '').replace('</tbody>', '')

        issue_types["Ammounts"]["Errors"] = int(header[13:header.index("Total Warnings:")])
        issue_types["Ammounts"]["Warnings"] = int(header[header.index("Total Warnings:") + 15:header.index("Total Notices:")])
        issue_types["Ammounts"]["Notices"] = int(header[header.index("Total Notices:") + 14:])
        # issue_types["Ammounts"].append(stats1)
        
        # Gathering all found issues for further processing
        results_start = raw_html.index("<tr>", raw_html.index("Description"))
        results_end = raw_html.index("</html>")
        report_data = raw_html[results_start:results_end].replace('</tbody>', '')\
            .replace('</table>','').replace('</body>', '').rstrip()

        # Separating issues and adding them into issues list
        pointer_start, pointer_end = report_data.index("<tr>") + len("<tr>"), report_data.index("</tr>")
        for i in range(sum(issue_types["Ammounts"].values())):
            tmp = report_data[pointer_start:pointer_end]
            issues.append(tmp)
            if i != (sum(issue_types["Ammounts"].values()) - 1):
                pointer_start = report_data.index("<tr>", pointer_end) + len("<tr>")              
                pointer_end = report_data.index('</tr>', pointer_start)
                
        # Processing issues and distributing each into an appropriate issue group (Error \ Warning \ Notice)
        sc_reg = '"col_scenario">'
        src_reg = '"col_source">'
        dsc_reg = '"col_description">'
        for issue in issues:
            if "Error" in issue:
                issue_types["Error"].append({"Scenario": issue[issue.index(sc_reg) + 15:issue.index('</td>')],
                                            "Source": issue[issue.index(src_reg) + 13:issue.index('</td>', issue.index(src_reg))],
                                            "Description": issue[issue.index(dsc_reg) + 18:issue.index('</td>', issue.index(dsc_reg))].rstrip(),
                                            "Bug": None})
            elif "Warning" in issue:
                issue_types["Warning"].append({"Scenario": issue[issue.index(sc_reg) + 15:issue.index('</td>')],
                                            "Source": issue[issue.index(src_reg) + 13:issue.index('</td>', issue.index(src_reg))],
                                            "Description": issue[issue.index(dsc_reg) + 18:issue.index('</td>', issue.index(dsc_reg))].rstrip(),
                                            "Bug": None})
            elif "Notice" in issue:
                issue_types["Notice"].append({"Scenario": issue[issue.index(sc_reg) + 15:issue.index('</td>')],
                                            "Source": issue[issue.index(src_reg) + 13:issue.index('</td>', issue.index(src_reg))],
                                            "Description": issue[issue.index(dsc_reg) + 18:issue.index('</td>', issue.index(dsc_reg))].rstrip(),
                                            "Bug": None})
            else:
                print(f"Couldn't distribute {issue} to any of available groups")

        # Sorting issues for smooth comparison (first sort by scenario name, second by issue description)
        issue_types["Error"] = sorted(issue_types["Error"], key=lambda x: (x["Scenario"], x["Description"], x["Source"]))
        issue_types["Warning"] = sorted(issue_types["Warning"], key=lambda x: (x["Scenario"], x["Description"], x["Source"]))
        issue_types["Notice"] = sorted(issue_types["Notice"], key=lambda x: (x["Scenario"], x["Description"], x["Source"]))
        print(f'Errors - {len(issue_types["Error"])}, Warnings - {len(issue_types["Warning"])}, Notices - {len(issue_types["Notice"])}')
        # print(issue_types)
        
    # Writing down final report into json
    with open(parsed_report_path, "w", encoding="utf-8") as out2:
        json.dump(issue_types, out2, indent="\t", ensure_ascii=False)
    
    print(f'Report {html_path} has been processed. Results in {parsed_report_path}. Report folder: {os.getcwd()}')
    return parsed_report_path

if __name__ == "__main__":
    if len(argv) == 2:
        d1 = argv[1].replace("\\", "/")
        doc1 = parse_html(d1, "parsed_report.json")
    elif len(argv) == 1:
        input("Path to html for conversion was not provided. Try again.\n"
              "Example: html_parser.py 'E:/report1.html'")
    else:
        input("Too many arguments provided. Expected only one.\n"
              "Example: html_parser.py 'E:/report1.html'")

