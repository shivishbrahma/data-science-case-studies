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
import urllib.error


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
    """
    Get or create a working directory for a specific dataset.
    :param dataset_name: The name of the dataset.
    :return: The path to the working directory.
    """

    cwd = Path(os.path.dirname(os.path.abspath(__file__))).parent
    print("Setting the base path to:", cwd)
    working_dir = cwd / "working" / dataset_name
    os.makedirs(working_dir, exist_ok=True)
    return working_dir


def download_by_url(url: str, filename: str, unzip=False, overwrite=False):
    """
    Download a file from a given URL and save it to a specified filename.
    :param url: The URL of the file to download.
    :param filename: The name of the file to save the downloaded content to.
    :param unzip: If True, unzip the file after download and remove the archive.
    :param overwrite: If True, overwrite the file if it already exists.
    :return: The directory name where the file is saved, or None on failure.
    """

    dirname = os.path.dirname(filename)
    os.makedirs(dirname, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",  # let urllib handle encoding; use 'identity' to avoid gzip issues
        "Referer": "https://www.ssa.gov/oact/babynames/limits.html",
    }

    if not os.path.exists(filename) or overwrite:
        print(f"Downloading {url} to {filename}")
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=30) as response, open(
                filename, "wb"
            ) as out_file:
                shutil.copyfileobj(response, out_file)
            print(f"✅ Download complete: {filename}")
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP error: {e.code} {e.reason}")
            if os.path.exists(filename):
                os.remove(filename)
            return None
        except (urllib.error.URLError, IOError) as e:
            print(f"❌ Error downloading file: {e}")
            if os.path.exists(filename):
                os.remove(filename)  # remove partial file
            return None
    else:
        print("File already downloaded to:", filename)

    if unzip:
        print(f"Unzipping {filename}")
        try:
            with zipfile.ZipFile(filename, "r") as zip_ref:
                zip_ref.extractall(dirname)
            os.remove(filename)
            print(f"✅ Unzipped to: {dirname}")
        except (zipfile.BadZipFile, FileNotFoundError) as e:
            print(f"❌ Error unzipping file: {e}")
            return None

    return dirname
