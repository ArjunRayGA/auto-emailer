import pandas as pd
import importlib
import os

from lib.utils import rename_cols, run_data_filters, find_replace_refs, settings_loader
from lib.gmail_api_client import get_client, test_client, markdown_compiler, create_message

def main(template_name):
    template_path =  os.path.abspath("templates/{}".format(template_name))

    # get all settings in a settings object
    settings_files = [os.path.join(template_path, 'data.json'), 'shared/data/class_data.json']
    settings = settings_loader(settings_files)

    # get relevant dicts from settings object
    csv_load_settings = settings["data"]["csv_load_settings"]

    # read in the csv data
    csv_path = os.path.join(template_path, csv_load_settings["csv_file"])
    data = pd.read_csv(csv_path, skiprows=csv_load_settings["skiprows"], header=1)

    print data

    # run data filters
    data = run_data_filters(data, data_filters=csv_load_settings["data_filters"])
    
    # rename columns
    data = rename_cols(data, csv_load_settings["col_rename_dict"])


    # split data into template data using logic
    logic_nodes = settings["data"]["logic_nodes"]
    logic = importlib.import_module('templates.{}.logic'.format(template_name))
    for node in logic_nodes:
        run_func = getattr(logic, node["function"])
        node["data"] = run_func(data)

    for node in logic_nodes:
        print '\n\n', node["function"].upper(), '\n'
        body = node["body"]
        title = node["title"]
        data = node["data"]
        for i, row in data.iterrows():
            data_kwargs = {
                "recipient": row['email'],
                "name": row["first_name"],
                "submitted": row['fp_1_sub'],
                "part_1_grade": row['fp_1_1'],
                "part_2_grade": row['fp_1_1'],
                "part_3_grade": row['fp_1_1'],
                "part_4_grade": row['fp_1_1']
            }
            markdown_compiler(body, template_path, **data_kwargs)

    service = get_client()
    # test_client(service)

    # print logic_nodes
     

if __name__ == "__main__": 
    main("final_project_01")
   


# with open(csv_file, 'r') as f:
#     data = csv.reader(f, delimiter=",")
#     data = [row for row in data][4:]
#     print data
    # for i, row in enumerate(data):
    #     if i == 0:
    #         continue

    #     first_name = row[0]
    #     last_name = row[1]
    #     email = row[2]
    #     resubmitted = row[3]
    #     meets = row[4]
    #     email_prepped = row[5]
    #     email_send = row[6]

    #     if not resubmitted:
    #         markdown = markdownStudent.format(first_name)
    #         title = markdownStudentTitle
    #         print "RESUBMISSION"
    #         print email.upper()
    #         popupCompose(email, title, markdown, ",".join(cc_emails))
    #         raw_input("Press Enter to continue...")
    #         print
    #     elif resubmitted and not email_send:
    #         complete_or_not = "completed" if meets == "y" else "not completed"
    #         markdown = markdownSendEmail.format(first_name, complete_or_not, complete_or_not)
    #         title = markdownSendEmailTitle.format(first_name, complete_or_not)
    #         print "NEED TO SEND EMAIL"
    #         print email.upper()
    #         # cc_emails_mod = cc_emails
    #         # email = cc_emails_mod.pop(1)
    #         popupCompose(",".join(cc_emails), title, markdown, "")
    #         raw_input("Press Enter to continue...")
    #         print
