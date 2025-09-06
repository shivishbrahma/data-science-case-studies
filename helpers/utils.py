import pandas as pd
from IPython.display import display_markdown

# Utilities function
def dataframe_summary(df: pd.DataFrame):
    column_summary_md = "|Column|Type|Missing|Unique|Min|Max|Mean|"
    column_summary_md += "\n|---|---|---|---|---|---|---|"
    for column_name in df.columns:
        column_summary_md += "\n|{}|{}|{}|{}|{}|{}|{}|".format(
            column_name,
            df[column_name].dtype,
            df[column_name].isnull().sum(),
             df[column_name].nunique(),
            "" if df[column_name].dtype in ["object", "bool"] else "{:.5g}".format(df[column_name].min()),
            "" if df[column_name].dtype in ["object", "bool"] else "{:.5g}".format(df[column_name].max()),
            "" if df[column_name].dtype in ["object", "bool"] else "{:.5g}".format(df[column_name].mean()) 
        )

    display_markdown(f"""## DataFrame Summary
---------------
**Shape**: {df.shape}  
**Columns**: {list(df.columns)}  
### Column Summary:
{column_summary_md}
""", raw=True)