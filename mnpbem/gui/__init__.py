"""PyMNPBEM desktop GUI.

Importing this subpackage requires the pymnpbem_simulation wrapper, which the
GUI uses for structure building, dispatch, config handling, post-processing and
I/O. That wrapper is a separate repository rather than a PyPI package, so
`pip install PyMNPBEM[gui]` cannot bring it in.

The check lives here, at package import, rather than inside gui_main.main():
gui_main imports .pages.start at module level, and that module imports
pymnpbem_simulation at module level too, so anything placed in main() would run
too late and the user would see a bare ModuleNotFoundError instead.
"""

try:
    import pymnpbem_simulation                          # noqa: F401
except ImportError:
    raise ImportError(
        "The PyMNPBEM GUI needs the pymnpbem_simulation wrapper, which is a "
        "separate repository and is not installed by pip install "
        "PyMNPBEM[gui]:\n"
        "    git clone https://github.com/LandesLinkLab/pymnpbem_simulation.git\n"
        "    pip install -e pymnpbem_simulation\n"
        "See docs/GUI_SETUP.md.")
