import pandas as pd
import templates.final_project_1 as template
from lib.utils import rename_cols, run_data_filters, find_replace_refs, settings_loader

def main():
    settings_files = ['settings/csv_load_settings.json', 'settings/class_data.json']
    settings = settings_loader(settings_files)
    csv_load_settings = settings["csv_load_settings"]
    class_data = settings["class_data"]

    skiprows = csv_load_settings["skiprows"]
    csv_file = csv_load_settings["csv_file"]
    col_rename_dict = csv_load_settings["col_rename_dict"]
    data_filters = csv_load_settings["data_filters"]

    data = pd.read_csv(csv_file, skiprows=skiprows, header=1)
    data = run_data_filters(data, data_filters=data_filters)
    
    data = rename_cols(data, col_rename_dict)
    print data

if __name__ == "__main__": main()
    


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
