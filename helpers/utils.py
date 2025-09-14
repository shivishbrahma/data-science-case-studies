import pandas as pd
import numpy as np
from IPython.display import display_markdown
import os
import shutil
import subprocess
from pathlib import Path
import zipfile


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
    zip_path = input_dir / f"{dataset_name}.zip"
    dataset_dir = input_dir / dataset_name

    if os.path.exists(dataset_dir) and not overwrite:
        print("Dataset already downloaded and extracted to:", dataset_dir)
        return dataset_dir

    # copy credentials to ~/.kaggle
    if not os.path.exists(os.path.join(dst, cred_filename)):
        os.makedirs(dst, exist_ok=True)
        shutil.copy(cred_filename, os.path.join(dst, cred_filename))

    # download dataset via kaggle CLI (requires kaggle.json in ~/.kaggle and kaggle installed)
    if os.path.exists(zip_path) and overwrite:
        os.remove(zip_path)

    if not os.path.exists(zip_path):
        # returns 0 on success
        ret = subprocess.run(
            [
                "kaggle",
                "datasets",
                "download",
                "-d",
                "{}/{}".format(username, dataset_name),
                "-p",
                "./input",
            ],
            check=False,
            capture_output=True,
        )
        if ret.returncode != 0:
            raise RuntimeError(
                "kaggle download failed (ensure kaggle is installed and authenticated)"
            )
        else:
            print(ret.stdout.decode("utf-8"))
    else:
        print("Dataset already downloaded to:", zip_path)

    input_dir.mkdir(parents=True, exist_ok=True)
    dataset_dir.mkdir(parents=True, exist_ok=True)

    # move the zip into input/ (overwrite if exists)
    shutil.move(str(zip_path), str(input_dir / zip_path.name))

    # unzip into input/youtube-new
    with zipfile.ZipFile(input_dir / zip_path.name, "r") as z:
        z.extractall(path=dataset_dir)

    print("Downloaded and extracted to:", dataset_dir)
    return dataset_dir

def get_working_dir(dataset_name: str):
    cwd = Path(os.path.dirname(os.path.abspath(__file__))).parent
    print("Setting the base path to:", cwd)
    working_dir = cwd / "working" / dataset_name
    os.makedirs(working_dir, exist_ok=True)
    return working_dir