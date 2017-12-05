def col_val_exists(df, col_name):
    return df[df[col_name].notnull()]
def col_val_isnull(df, col_name):
    return df[df[col_name].isnull()]
def col_val_not_in_list(df, col_name, exclude_list):
    print exclude_list
    return df[~df[col_name].isin(exclude_list)]
