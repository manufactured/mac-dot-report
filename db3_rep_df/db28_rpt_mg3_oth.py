import pandas as pd
from db1_main_df.db03_dtype_dict import (
    field_types_with_defaults, 
    get_valid_types
)

import pandas as pd

def write_st_alert_value(report_dataframe, index, new_status):
    current_status = report_dataframe.at[index, 'st_alert']
    
    # If there is already a status, overwrite it and add the red emoji
    if not pd.isna(current_status) and current_status != '':
        report_dataframe.at[index, 'st_alert'] = f" {new_status}"
    else:
        report_dataframe.at[index, 'st_alert'] = new_status
    
    return report_dataframe

def field_match_3_subsys(report_dataframe):
    # Confirm Docs: Both docs match each other - YAML vs CSV
    try:
        report_dataframe['st_docs'] = subsystem_docs(report_dataframe)
    except Exception as e:
        print(f"Error in subsystem_docs: {e}")
        report_dataframe['st_docs'] = ''

    # Confirm DotBot status: YAML matches FS Home and Repo
    try:
        report_dataframe['st_db_all'] = subsystem_db_all(report_dataframe)
    except Exception as e:
        print(f"Error in subsystem_db_all: {e}")
        report_dataframe['st_db_all'] = ''

    return report_dataframe

def subsystem_docs(report_dataframe):
    for index, row in report_dataframe.iterrows():
        if (row['item_name_rp_di'] == row['item_name_rp_db'] and
            row['item_type_rp_di'] == row['item_type_rp_db'] and
            row['item_name_hm_di'] == row['item_name_hm_db'] and
            row['item_type_hm_di'] == row['item_type_hm_db']):
            report_dataframe.at[index, 'st_docs'] = 'Valid'
        else:
            report_dataframe.at[index, 'st_docs'] = 'Invalid'
    
    return report_dataframe['st_docs']

def subsystem_db_all(report_dataframe):
    """
    Verify DotBot alignment between repo, home, and DotBot YAML.
    Updates 'st_db_all' with 'Valid' or 'Invalid' based on the match.
    """

    # Check if repo folder matches the corresponding entry in DotBot YAML
    repo_name_match = (report_dataframe['item_name_rp'] == report_dataframe['item_name_rp_db'])
    repo_type_match = (report_dataframe['item_type_rp'] == report_dataframe['item_type_rp_db'])

    # Check if home folder matches the corresponding entry in DotBot YAML
    home_name_match = (report_dataframe['item_name_hm'] == report_dataframe['item_name_hm_db'])
    home_type_match = (report_dataframe['item_type_hm'] == report_dataframe['item_type_hm_db'])

    # Check for default values in any of the relevant fields
    default_check = (
        (report_dataframe['item_name_rp'] == field_types_with_defaults['item_name_rp'][1]) |
        (report_dataframe['item_type_rp'] == field_types_with_defaults['item_type_rp'][1]) |
        (report_dataframe['item_name_hm'] == field_types_with_defaults['item_name_hm'][1]) |
        (report_dataframe['item_type_hm'] == field_types_with_defaults['item_type_hm'][1]) |
        (report_dataframe['item_name_rp_db'] == field_types_with_defaults['item_name_rp_db'][1]) |
        (report_dataframe['item_type_rp_db'] == field_types_with_defaults['item_type_rp_db'][1]) |
        (report_dataframe['item_name_hm_db'] == field_types_with_defaults['item_name_hm_db'][1]) |
        (report_dataframe['item_type_hm_db'] == field_types_with_defaults['item_type_hm_db'][1])
    )

    # Set 'Valid' or 'Invalid' based on name and type match and default check
    report_dataframe['st_db_all'] = 'Invalid'  # Default to 'Invalid'
    report_dataframe.loc[repo_name_match & repo_type_match & home_name_match & home_type_match & ~default_check, 'st_db_all'] = 'Valid'

    return report_dataframe['st_db_all']