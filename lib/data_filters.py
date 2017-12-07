def default_chain_func(x):
    return x

def row_val_exists(df, col_name, chain_func=default_chain_func):
    return chain_func(df[df[col_name].notnull()])

def row_val_isnull(df, col_name, chain_func=default_chain_func):
    return chain_func(df[df[col_name].isnull()])

def row_val_not_in_list(df, col_name, exclude_list, chain_func=default_chain_func):
    return chain_func(df[~df[col_name].isin(exclude_list)])

def row_val_in_list(df, col_name, include_list, chain_func=default_chain_func):
    return chain_func(df[df[col_name].isin(include_list)])

def drop_cols(df, col_names=None, col_indicies=None, chain_func=default_chain_func):
    print col_indicies
    if col_names:
        return chain_func(df.drop(col_names, axis=1))
    if col_indicies:
        return chain_func(df.drop(df.columns[col_indicies], axis=1))