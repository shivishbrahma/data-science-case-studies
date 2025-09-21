import pandas as pd
import numpy as np
from IPython.display import display_markdown
import os
import shutil
import subprocess
from pathlib import Path
import zipfile
import kaggle
import urllib.request


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


def download_from_kaggle(username: str, dataset_name: str, overwrite=False):
    """
    Download a dataset from Kaggle and extract it to a specified directory.
    :param username: The username of the Kaggle user who owns the dataset.
    :param dataset_name: The name of the dataset to download.
    :param overwrite: Whether to overwrite an existing dataset directory.
    """
    # install kaggle api and set the credentials
    dst = os.path.join(os.path.expanduser("~"), ".kaggle")
    cred_filename = "kaggle.json"
    cwd = Path(os.path.dirname(os.path.abspath(__file__))).parent
    print("Setting the base path to:", cwd)

    input_dir = cwd / "input"
    dataset_dir = input_dir / dataset_name

    if os.path.exists(dataset_dir) and not overwrite:
        print("Dataset already downloaded and extracted to:", dataset_dir)
        return dataset_dir

    # copy credentials to ~/.kaggle
    if not os.path.exists(os.path.join(dst, cred_filename)):
        os.makedirs(dst, exist_ok=True)
        shutil.copy(cred_filename, os.path.join(dst, cred_filename))

    # returns 0 on success
    kaggle.api.dataset_download_files(
        dataset=f"{username}/{dataset_name}",
        path=str(dataset_dir),
        unzip=True,
    )

    print("Downloaded and extracted to:", dataset_dir)
    return dataset_dir


def get_working_dir(dataset_name: str):
    cwd = Path(os.path.dirname(os.path.abspath(__file__))).parent
    print("Setting the base path to:", cwd)
    working_dir = cwd / "working" / dataset_name
    os.makedirs(working_dir, exist_ok=True)
    return working_dir


def download_by_url(url: str, filename: str, unzip=False, overwrite=False, chunk_size=1024):
    """
    Download a file from a given URL and save it to a specified filename.
    :param url: The URL of the file to download.
    :param filename: The name of the file to save the downloaded content to.
    """
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if os.path.exists(filename) and not overwrite:
        print("File already downloaded to:", filename)
        return

    # download file using urlib and stream mode
    try:
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
        print(f"✅ Download complete: {filename}")
    except Exception as e:
        print(f"❌ Error downloading file: {e}")

    if unzip:
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(dirname)
        os.remove(filename)

    return dirname
