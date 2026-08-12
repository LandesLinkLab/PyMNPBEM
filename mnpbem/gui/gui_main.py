"""PyMNPBEM GUI window and page router.

Launch through the top-level launcher, never this module directly::

    pymnpbem-gui                  # console script -> pymnpbem_gui:main
    python pymnpbem_gui.py        # from a source checkout

``python -m mnpbem.gui.gui_main`` still opens the window, but it skips the
thread-count ceiling that pymnpbem_gui.py sets before NumPy and Numba are
imported, so the Threads value on the Start page cannot be raised past whatever
the shell already had configured. See the comment at the top of pymnpbem_gui.py.

The GUI drives the pymnpbem_simulation wrapper, which is a separate repository
and not a PyPI dependency, so `pip install PyMNPBEM[gui]` alone is not enough.
See docs/GUI_SETUP.md.
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QStackedWidget, QToolBar)
from PySide6.QtGui import QIcon, QAction



from .simulation_state import SimulationState
from .pages.start import StartPage
from .widgets.state_dialog import StateDebugDialog

# Import all the pages here

# GENERIC LAMBDA FOR CHANGING STATE: lambda val: setattr(self.state, 'state_property', val)
# useful if you don't need anything to happen other than the value change
class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyMNPBEM GUI")
        
        
        self.resize(800, 700)
        self.showMaximized()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.state = SimulationState() # this is where all the data gets stored (may become RAM heavy when it stores the sim data)

        self.page1 = StartPage(self.state)
        self.page2 = None
        self.page3 = None

        self.stacked_widget.addWidget(self.page1)

        self.toolbar = QToolBar("Debug Toolbar")
        self.addToolBar(self.toolbar)

        state_action = QAction("View State", self)
        state_action.setStatusTip("View Pop-Out State Dialog")
        state_action.triggered.connect(self.toolbar_view_state)
        self.toolbar.addAction(state_action)

        self.page1.settings_completed.connect(self.go_to_sim)
    def _ensure_runtime_pages(self):
        if self.page2 is not None and self.page3 is not None:
            return True

        from .widgets.import_loading import ImportProgressDialog
        import_dialog = ImportProgressDialog(self)
        import_dialog.exec() # will block until import is done, (which means these pages should load fine)

        # A failed import leaves the pages unbuilt; staying on the Start page is
        # the only safe move, and the reason has to reach the user.
        try:
            if import_dialog.error is not None:
                raise RuntimeError(import_dialog.error)

            # in case something failed, import again (python should skip it if it is already imported so no performance hit)
            from .pages.simulation import SimulationPage
            from .pages.post_processing import ProcessingPage

            self.page2 = SimulationPage(self.state)
            self.page3 = ProcessingPage(self.state)

        except Exception as exc:
            self.page2 = None
            self.page3 = None
            QMessageBox.critical(
                self,
                "Could Not Open Simulation Page",
                "Loading the simulation and post-processing pages failed:\n\n{}".format(exc),
                QMessageBox.Ok)
            return False

        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        self.page2.sim_completed.connect(self.go_to_post)
        return True

    def go_to_sim(self):
        if not self._ensure_runtime_pages():
            return
        self.page2.setup_ui_from_state()  # not really using this, but could be useful later (so leaving it in)
        self.stacked_widget.setCurrentWidget(self.page2)
    def go_to_post(self):
        #self._ensure_runtime_pages() # already done in go to sim so redundant
        self.page3.setup_ui_from_state()
        self.stacked_widget.setCurrentWidget(self.page3)
    def toolbar_view_state(self): # freezes up the main window (close when done)
        dlg = StateDebugDialog(self.state, self)
        dlg.exec()
        


def main():
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent

    icon_path = base_dir / "images" / "Landes_group_logo_cropped.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    else:
        print(f"Warning: Icon not found at {icon_path}")

    qss_path = base_dir / "style.qss"
    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {qss_path}. Using default style.")

    window = MainController()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
