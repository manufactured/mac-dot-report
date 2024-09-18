import os
import logging
import pandas as pd
from .db11_merge import get_next_unique_id

def correct_and_validate_dot_info_df(dot_info_df):
    # Correct values: Replace NaN with empty strings in 'comment_di' field
    dot_info_df['comment_di'] = dot_info_df['comment_di'].fillna('')
    return dot_info_df

def load_di_dataframe():
    try:
        dot_info_file_path = "./data/dot-info.csv"
        
        # Load the CSV with explicit data types for the columns
        dot_info_df = pd.read_csv(dot_info_file_path, dtype={
            "item_name_rp_di": "string",
            "item_name_hm_di": "string",
            "dot_struc_di": "string",
            "item_type_rp_di": "string",
            "item_type_hm_di": "string",
            "cat_1_di": "string",
            "cat_1_name_di": "string",
            "cat_2_di": "string",
            "comment_di": "string",
            "no_show_di": "bool"
        }).copy()

        # Record the original order of rows
        dot_info_df['sort_orig'] = (dot_info_df.index + 1).astype("Int64")  # Convert to Int64 explicitly

        # Assign unique IDs
        dot_info_df['unique_id_di'] = dot_info_df.apply(lambda row: get_next_unique_id(), axis=1)
        dot_info_df["unique_id_di"] = dot_info_df["unique_id_di"].astype("Int64")

        # Apply the correction and validation function
        dot_info_df = correct_and_validate_dot_info_df(dot_info_df)

        # Toggle output directly within the function
        show_output = False
        show_full_df = False

        if show_output:
            if show_full_df:
                print("7️⃣ dot_info DataFrame:\n", dot_info_df)
            else:
                print("7️⃣ dot_info DataFrame (First 5 rows):\n", dot_info_df.head())

        return dot_info_df
    except Exception as e:
        logging.error(f"Error loading dot_info CSV: {e}")
        return pd.DataFrame()