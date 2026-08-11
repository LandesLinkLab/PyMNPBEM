# SPDX-License-Identifier: GPL-2.0-or-later
#
# Launcher for the PyMNPBEM GUI.
#
# This module deliberately lives OUTSIDE the mnpbem package. Python executes a
# package's __init__ before it can reach any submodule, so an entry point of
# "mnpbem.gui.gui_main:main" runs mnpbem/__init__.py -- which eagerly imports
# the whole library, and with it NumPy and Numba -- before a single line of GUI
# code. MKL/OpenBLAS/Numba latch their thread pools at import, so by then the
# thread count the user is about to pick on the Start page can no longer take
# effect, and pymnpbem_simulation.assert_pre_import() can never pass.
#
# Setting the ceiling here, before importing anything heavy, is the same fix
# run_simulation.py already applies to the CLI. The Start page then narrows the
# count at runtime to whatever the user actually chose.

import os
import sys


def _set_thread_ceiling() -> None:
    # Upper bound only. setdefault keeps an externally configured value (a
    # cluster scheduler, a user's shell) authoritative; the Start page lowers
    # the effective count afterwards via mnpbem.gui.thread_control.
    n_cpu = str(os.cpu_count() or 1)
    for key in ('MKL_NUM_THREADS', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'NUMBA_NUM_THREADS'):
        os.environ.setdefault(key, n_cpu)


_set_thread_ceiling()


def main() -> int:
    from mnpbem.gui.gui_main import main as gui_main
    return gui_main()


if __name__ == '__main__':
    sys.exit(main())
