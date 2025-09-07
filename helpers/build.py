import jupyter
import os
from pathlib import Path
from nbformat import read, write, NO_CONVERT
from nbformat import v4 as nbf_v4
from nbconvert import HTMLExporter
from traitlets.config import Config
import markdown
import shutil


def clear_outputs(nb):
    for cell in nb.cells:
        if cell.get("cell_type") == "code":
            cell.outputs = []
            cell.execution_count = None
    return nb


def convert_notebook(nb_path: Path, out_path: Path, clear_output: bool = False):
    with nb_path.open("r", encoding="utf-8") as f:
        nb = read(f, as_version=NO_CONVERT)
    if clear_output:
        nb = clear_outputs(nb)
    c = Config()
    # single-file HTML (inlines attachments/resources)
    c.HTMLExporter.embed_images = True
    c.HTMLExporter.exclude_input = False  # change True to hide code cells
    exporter = HTMLExporter(config=c)
    body, resources = exporter.from_notebook_node(nb)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(body)
    return out_path


if __name__ == "__main__":
    if os.path.exists("build"):
        shutil.rmtree("build")
    os.makedirs("build")

    # Iterate recursively over project directory
    for root, _, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".ipynb") and ".ipynb_checkpoints" not in root:
                print(f"Converting {filename}...")
                nb_path = Path(os.path.join(root, filename))
                out_path = Path(os.path.join("build", nb_path.with_suffix(".html")))
                convert_notebook(nb_path, out_path)
                print(f"Converted {filename} to {out_path}")
            elif filename.endswith(".md"):
                print(f"Converting {filename}...")

                md_path = Path(os.path.join(root, filename))
                if filename == "README.md":
                    html_path = Path(os.path.join("build", root, "index.html"))
                else:
                    html_path = Path(
                        os.path.join("build", md_path.with_suffix(".html"))
                    )
                with md_path.open("r", encoding="utf-8") as f:
                    md = f.read()
                    html = markdown.markdown(md)
                    html = html.replace(".ipynb", ".html")

                html_path.parent.mkdir(parents=True, exist_ok=True)
                with html_path.open("w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Converted {filename} to {html_path}")

    print("Done!")
