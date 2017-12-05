grade_criteria = ["fp_1_1", 
                  "fp_1_2", 
                  "fp_1_3", 
                  "fp_1_4"]

def not_present(df):
    return df[df[grade_criteria].isnull().all(axis=1)]

def present(df):
    return df[df[grade_criteria].isin([0,1,2,3]).all(axis=1)]

def not_submit_not_present(df):
    df = df[~df["fp_1_sub"].isin(["Yes"])]
    return not_present(df)

def not_submit_present(df):
    df = df[~df["fp_1_sub"].isin(["Yes"])]
    return present(df)

def submit_not_present(df):
    df = df[df["fp_1_sub"].isin(["Yes"])]   
    return not_present(df)

def submit_present(df):
    df = df[df["fp_1_sub"].isin(["Yes"])]
    return present(df)
