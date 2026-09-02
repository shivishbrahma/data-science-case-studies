import jupyter
import os
from pathlib import Path
from nbformat import read, write, NO_CONVERT
from nbformat import v4 as nbf_v4
from nbconvert import HTMLExporter
from traitlets.config import Config
import markdown
import shutil
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup
import datetime
from argparse import ArgumentParser

BASE_URL = "/data-science-case-studies"
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def clear_outputs(nb):
    for cell in nb.cells:
        if cell.get("cell_type") == "code":
            cell.outputs = []
            cell.execution_count = None
    return nb


def convert_notebook(
    nb_path: Path, out_path: Path, clear_output: bool = False, variables: dict = {}
):
    with nb_path.open("r", encoding="utf-8") as f:
        nb = read(f, as_version=NO_CONVERT)
    if clear_output:
        nb = clear_outputs(nb)
    c = Config()
    # single-file HTML (inlines attachments/resources)
    # c.TemplateExporter.template_path.append(TEMPLATE_DIR)
    c.TemplateExporter.template_file = os.path.join(TEMPLATE_DIR, "notebook.j2")
    c.HTMLExporter.embed_images = True
    c.HTMLExporter.exclude_input = False  # change True to hide code cells
    exporter = HTMLExporter(config=c)
    exporter.environment.globals = env.globals

    for key, value in variables.items():
        exporter.environment.globals[key] = value

    body, _ = exporter.from_notebook_node(nb)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        f.write(body)
    return out_path


def get_title(html: str):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if h1 is None:
        return "Data Science Case Studies"
    return h1.text


def url_for(endpoint, **params):
    """
    Simple URL builder.

    Given an endpoint (e.g. route key, path name), and keyword arguments,
    returns a URL string.

    Example:
        url_for("static", filename="style.css") -> "/static/style.css"

    Raises:
        KeyError: if endpoint is unknown
    """

    routes = {
        "static": BASE_URL + "/static/{filename}",
    }
    tmpl = routes.get(endpoint)
    if tmpl is None:
        raise KeyError(f"unknown endpoint: {endpoint}")
    return tmpl.format(**params)


def breadcrumb_builder(path: str, navlinks: dict):
    breadcrumbs = []
    cur_path = ""
    # print(f"Building breadcrumbs for path: {path}")
    # print(f"navlinks: {navlinks}")
    parts = path.rstrip("/").split("/")
    for part in parts:
        if part == "." or part == "..":
            continue
        if part.find(".") != -1:
            cur_path += f"{part}"
        else:
            cur_path += f"{part}/"
        # print(f"Current path: {cur_path}")
        breadcrumbs.append(
            {
                "url": BASE_URL.rstrip("/") + cur_path,
                "name": navlinks[cur_path],
            }
        )
    return breadcrumbs


if __name__ == "__main__":
    parser = ArgumentParser(description="Build the project")
    parser.add_argument(
        "--clear-output",
        action="store_true",
        help="Clear notebook outputs",
        default=False,
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Development mode (no clear output)",
        default=False,
    )
    args = parser.parse_args()

    if args.dev:
        BASE_URL = ""

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    env.globals["url_for"] = url_for
    env.globals["year"] = datetime.datetime.now().year
    env.globals["base_url"] = BASE_URL

    markdown_template = env.get_template("markdown.j2")

    navlinks = {}

    if os.path.exists("build"):
        shutil.rmtree("build")
    os.makedirs("build")

    # Copy static folder into build folder
    shutil.copytree("static", "build/static")

    # Iterate recursively over project directory
    for root, _, filenames in os.walk("."):
        # pull index.md or README.md files to the top of the list
        filenames.sort(key=lambda x: (x != "index.md" and x != "README.md", x))
        for filename in filenames:
            if filename.endswith(".ipynb") and ".ipynb_checkpoints" not in root:
                nav_name = (filename.replace(".ipynb", "").replace("-", " ").title())[
                    :15
                ] + "..."
                nav_link = (
                    root.replace(".", "").replace(os.sep, "/")
                    + "/"
                    + filename.replace(".ipynb", ".html")
                )
                navlinks[nav_link] = nav_name
                breadcrumb_path = breadcrumb_builder(nav_link, navlinks)
                # print(breadcrumb_path)
                print(f"Converting {filename}...")
                nb_path = Path(os.path.join(root, filename))
                out_path = Path(os.path.join("build", nb_path.with_suffix(".html")))
                convert_notebook(
                    nb_path,
                    out_path,
                    clear_output=args.clear_output,
                    variables={"breadcrumbs": breadcrumb_path},
                )
                print(f"Converted {filename} to {out_path}")
            elif filename.endswith(".md"):
                print(f"Converting {filename}...")

                md_path = Path(os.path.join(root, filename))
                if filename == "README.md" or filename == "index.md":
                    if root == ".":
                        nav_name = "Home"
                        nav_link = "/"
                    else:
                        nav_name = (
                            os.path.basename(root)
                            .replace(".", "")
                            .replace(os.sep, "/")
                            .replace("-", " ")
                            .title()
                        )[:15] + "..."
                        nav_link = (
                            root.replace(".", "").replace(os.sep, "/") + "/"
                        )

                    navlinks[nav_link] = nav_name
                    breadcrumb_path = breadcrumb_builder(nav_link, navlinks)

                    html_path = Path(os.path.join("build", root, "index.html"))
                else:
                    html_path = Path(
                        os.path.join("build", md_path.with_suffix(".html"))
                    )
                with md_path.open("r", encoding="utf-8") as f:
                    md = f.read()
                    html = markdown.markdown(md)
                    html = html.replace(".ipynb", ".html")
                    title = get_title(html)
                    html = markdown_template.render(
                        body=html, title=title, breadcrumbs=breadcrumb_path
                    )

                html_path.parent.mkdir(parents=True, exist_ok=True)
                with html_path.open("w", encoding="utf-8") as f:
                    f.write(html)
                print(f"Converted {filename} to {html_path}")

    print("Done!")
