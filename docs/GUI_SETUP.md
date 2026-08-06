# PyMNPBEM GUI - setup

## You need two repositories

The GUI is a front end for the **simulation wrapper**, not for the solver alone.
It imports `pymnpbem_simulation` in about a dozen places (structure building,
dispatch, config handling, post-processing, I/O), and that wrapper is a separate
repository rather than a PyPI package.

`pip install PyMNPBEM[gui]` therefore installs the GUI and its Qt dependencies
but **not** the wrapper, and the GUI will refuse to start without it.

Clone both, into separate folders (installing two packages from the same folder
conflicts):

```bash
git clone https://github.com/LandesLinkLab/PyMNPBEM.git
git clone https://github.com/LandesLinkLab/pymnpbem_simulation.git
```

## Environment

Python 3.11 or newer.

```bash
conda create -n mnpbem python=3.11
conda activate mnpbem
```

`mnpbem/gui/mnpbem_environment_windows.yml` pins an exact, working Windows
environment. It is Windows-only -- it lists `vs2015_runtime`, `vc14` and `ucrt`
-- so on Linux or macOS use the conda command above instead.

```bash
conda env create -f mnpbem/gui/mnpbem_environment_windows.yml --solver=libmamba
```

`--solver=libmamba` matters: the default solver takes a very long time on this
dependency set.

## Install

Install the wrapper first, then PyMNPBEM with the `gui` extra. Editable
installs (`-e`) mean a `git pull` updates the code with no reinstall.

```bash
pip install -e ./pymnpbem_simulation
pip install -e "./PyMNPBEM[gui]"
```

For GPU acceleration add the `gpu` extra and set the environment variable:

```bash
pip install -e "./PyMNPBEM[gui,gpu]"
set MNPBEM_GPU=1          # Windows
export MNPBEM_GPU=1       # Linux / macOS
```

Other install options are in [INSTALL.md](./INSTALL.md).

## Run

```bash
pymnpbem-gui
```

or, from a source checkout:

```bash
python -m mnpbem.gui.gui_main
```

If the wrapper is missing, the GUI exits immediately with a message naming the
repository to clone, rather than a traceback from a page import.

### One-click launcher

**`PyMNPBEM_GUI.bat`** (Windows)

```bat
@echo off
call "C:\Users\USER\Anaconda3\condabin\conda.bat" activate mnpbem
set MNPBEM_GPU=1
pymnpbem-gui
pause
```

**`pymnpbem-gui.sh`** (Linux / macOS)

```bash
#!/usr/bin/env bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate mnpbem
export MNPBEM_GPU=1
pymnpbem-gui
```

## User-defined materials

The GUI reads custom dielectric functions from
`mnpbem/gui/user-defined/materials/`, and the "Open User-Defined Content Folder"
button on the setup screen opens it. `vacuum.py` is the example to copy for a
function-defined material; `.dat` files are tabulated `[eV, n, k]`.

With an editable install this folder is the one in your clone, so files you add
there survive a `git pull`. With a normal (non-editable) install it lives inside
site-packages instead, which is why editable is recommended above.

## Updating

Both packages are installed editable, so:

```bash
cd PyMNPBEM              && git pull
cd ../pymnpbem_simulation && git pull
```

No reinstall is needed unless the dependencies change.

## [Using the GUI](./GUI_GUIDE.md)
