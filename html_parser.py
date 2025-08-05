import json
from sys import argv
from html_compares import report_diff
import os

def parse_html(html_path, parsed_report_path):
    print(f'Processing {html_path}')
    html_p = html_path
    header, report_data = "", ""
    issue_types = {"Ammounts": [], "Error": [], "Warning": [], "Notice": []}
    stats1 = dict()
    issues = []

    # Working with passed html path
    with open(html_p, "r", encoding="utf-8") as inp:
        raw_html = inp.read()
        header = raw_html[raw_html.index("<tr>"):raw_html.index("</table>")]
        
        # Gathering issues count from the report's header
        header = header.replace('<tr><th id="col_info">', '').replace('</td></tr>', '').replace('</th><td>', '').replace('</tbody>', '')

        stats1["Errors"] = int(header[13:header.index("Total Warnings:")])
        stats1["Warnings"] = int(header[header.index("Total Warnings:") + 15:header.index("Total Notices:")])
        stats1["Notices"] = int(header[header.index("Total Notices:") + 14:])
        issue_types["Ammounts"].append(stats1)
        
        # Gathering all found issues for further processing
        results_start = raw_html.index("<tr>", raw_html.index("Description"))
        results_end = raw_html.index("</html>")
        report_data = raw_html[results_start:results_end].replace('</tbody>', '').replace('</table>','').replace('</body>', '').rstrip()

        # Separating issues and adding them into issues list
        pointer_start, pointer_end = report_data.index("<tr>") + len("<tr>"), report_data.index("</tr>")
        for i in range(sum(stats1.values())):
            tmp = report_data[pointer_start:pointer_end]
            issues.append(tmp)
            if i != (sum(stats1.values()) - 1):
                pointer_start = report_data.index("<tr>", pointer_end) + len("<tr>")              
                pointer_end = report_data.index('</tr>', pointer_start)
                
        # Processing issues and distributing each into an appropriate issue group (Error \ Warning \ Notice)
        for issue in issues:
            if "Error" in issue:
                issue_types["Error"].append({"Scenario": issue[issue.index('"col_scenario">') + 15:issue.index('</td>')],
                                            "Source": issue[issue.index('"col_source">') + 13:issue.index('</td>', issue.index('"col_source">'))],
                                            "Description": issue[issue.index('"col_description">') + 18:issue.index('</td>', issue.index('"col_description">'))]})
            elif "Warning" in issue:
                issue_types["Warning"].append({"Scenario": issue[issue.index('"col_scenario">') + 15:issue.index('</td>')],
                                            "Source": issue[issue.index('"col_source">') + 13:issue.index('</td>', issue.index('"col_source">'))],
                                            "Description": issue[issue.index('"col_description">') + 18:issue.index('</td>', issue.index('"col_description">'))]})
            elif "Notice" in issue:
                issue_types["Notice"].append({"Scenario": issue[issue.index('"col_scenario">') + 15:issue.index('</td>')],
                                            "Source": issue[issue.index('"col_source">') + 13:issue.index('</td>', issue.index('"col_source">'))],
                                            "Description": issue[issue.index('"col_description">') + 18:issue.index('</td>', issue.index('"col_description">'))]})
            else:
                print(f"Couldn't distribute {issue} to any of available groups")

        # Sorting issues for smooth comparison (first sort by scenario name, second by issue description)
        issue_types["Error"] = sorted(issue_types["Error"], key=lambda x: (x["Scenario"], x["Description"]))
        issue_types["Warning"] = sorted(issue_types["Warning"], key=lambda x: (x["Scenario"], x["Description"]))
        issue_types["Notice"] = sorted(issue_types["Notice"], key=lambda x: (x["Scenario"], x["Description"]))
        print(f'Errors - {len(issue_types["Error"])}, Warnings - {len(issue_types["Warning"])}, Notices - {len(issue_types["Notice"])}')
        # print(issue_types)
        
    # Writing down final report into json
    with open(parsed_report_path, "w", encoding="utf-8") as out2:
        json.dump(issue_types, out2, indent="\t", ensure_ascii=False)
    
    print(f'Report {html_p} has been processed. Results in {parsed_report_path}. Report folder: {os.getcwd()}')
    return parsed_report_path

d1, d2 = argv[1].replace("\\", "/"), argv[2].replace("\\", "/")

doc1 = parse_html(d1, "report_left.json")
doc2 = parse_html(d2, "report_right.json")

report_diff(doc1, doc2)

