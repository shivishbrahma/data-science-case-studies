import pandas as pd
import numpy as np
from IPython.display import display_markdown


def check_numeric_value(dtype: str):
    """
    Checks if a given data type is numeric.
    :param dtype: The data type to check.
    :return: True if the data type is numeric, False otherwise.
    """
    return dtype in ["int64", "float64"]


def dataframe_summary(df: pd.DataFrame):
    """
    Generates a markdown-formatted summary of a Pandas DataFrame, including column types, missing values,
    unique counts, and basic statistics (min, max, mean) for numeric columns.

    :param df: The Pandas DataFrame to summarize.
    :return: A string containing the markdown-formatted summary.
    """

    column_summary_md = "|Column|Type|Missing|Unique|Min|Max|Mean|"
    column_summary_md += "\n|---|---|---|---|---|---|---|"
    for column_name in df.columns:
        column_summary_md += "\n|{}|{}|{}|{}|{}|{}|{}|".format(
            column_name,
            df[column_name].dtype,
            df[column_name].isnull().sum(),
            df[column_name].nunique(),
            (
                "{:.5g}".format(df[column_name].min())
                if check_numeric_value(str(df[column_name].dtype))
                else ""
            ),
            (
                "{:.5g}".format(df[column_name].max())
                if check_numeric_value(str(df[column_name].dtype))
                else ""
            ),
            (
                "{:.5g}".format(df[column_name].mean())
                if check_numeric_value(str(df[column_name].dtype))
                else ""
            ),
        )

    display_markdown(
        f"""### DataFrame Summary
---------------
**Shape**: {df.shape}  
**Columns**: {list(df.columns)}  
#### Column Summary:
{column_summary_md}
""",
        raw=True,
    )
