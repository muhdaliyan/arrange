"""arrange notebook — Data science workspace with Jupyter notebooks."""

import os

from arrange.utils import (
    check_uv,
    create_dirs,
    ensure_venv_exists,
    print_banner,
    print_done,
    print_step,
    run,
    write_file,
)

SAMPLE_NOTEBOOK = '''\
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# Exploration Notebook\\n", "\\n", "Start your analysis here."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": ["import pandas as pd\\n", "import numpy as np\\n", "import matplotlib.pyplot as plt\\n", "\\n", "print(\\"Ready to go!\\")"]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (project)",
   "language": "python",
   "name": "project-kernel"
  },
  "language_info": {
   "name": "python",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
'''

DEMO_NOTEBOOK = '''\
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# Demo Notebook\\n", "\\n", "This notebook demonstrates the capabilities of your new workspace."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "\\n",
    "# Create some sample data\\n",
    "df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))\\n",
    "df.head()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (project)",
   "language": "python",
   "name": "project-kernel"
  },
  "language_info": {
   "name": "python",
   "version": "3.12.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
'''

GITKEEP = ""


def run_command() -> None:
    """Scaffold a data science workspace with Jupyter notebooks."""
    print_banner("notebook", "Data science workspace with Jupyter")

    check_uv()
    ensure_venv_exists()

    # Install data science dependencies
    run("uv add ipykernel pandas numpy matplotlib")

    # Create directory structure
    create_dirs("notebooks", "data/raw", "data/processed")

    # Keep empty data dirs in git
    write_file("data/raw/.gitkeep", GITKEEP)
    write_file("data/processed/.gitkeep", GITKEEP)

    # Create notebooks
    write_file("notebooks/exploration.ipynb", SAMPLE_NOTEBOOK)
    write_file("notebooks/demo.ipynb", DEMO_NOTEBOOK)

    # Register Jupyter kernel
    project_name = os.path.basename(os.getcwd())
    print_step("Registering Jupyter kernel...")
    run(f"uv run python -m ipykernel install --user --name={project_name} --display-name=\"Python ({project_name})\"")

    print_done()
