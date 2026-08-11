# SPDX-License-Identifier: GPL-2.0-or-later
#
# Runtime thread-count control for the GUI.
#
# The GUI cannot use pymnpbem_simulation.assert_pre_import(): the package that
# hosts it (mnpbem) is necessarily imported before any GUI code runs, so NumPy,
# MKL/OpenBLAS and Numba have already latched their thread pools by the time the
# user picks a thread count on the Start page. pymnpbem_gui.py raises the ceiling
# to os.cpu_count() before those imports happen; this module narrows the count
# afterwards, which is the only part that can still respond to the user.
#
# Environment variables are still exported by pymnpbem_simulation.setup_env():
# MNPBEM_GPU and MNPBEM_NUMBA are read per call rather than at import, and any
# subprocess spawned later inherits the whole set.

import os

from typing import List, Tuple

# threadpool_limits restores the original limits when the returned object is
# collected, so the handle has to outlive the call that created it.
_BLAS_LIMIT_HANDLE = None


def apply_thread_limit(n_threads: int) -> Tuple[bool, List[str]]:
    # Returns (fully_applied, notes). A note is recorded for every knob that
    # could not be honoured, so the caller can tell the user instead of silently
    # running at a different width than the one they selected.
    n_threads = max(1, int(n_threads))
    notes = []

    global _BLAS_LIMIT_HANDLE
    try:
        from threadpoolctl import threadpool_limits
        # BLAS only. The dense solve is where the BEM run spends its time, and
        # the remaining OpenMP pool is the layer Numba schedules its own kernels
        # on -- that one is set through numba.set_num_threads() below, so
        # clamping it here as well would mean two owners for one knob.
        _BLAS_LIMIT_HANDLE = threadpool_limits(limits = n_threads, user_api = 'blas')
    except ImportError:
        notes.append(
            'threadpoolctl is not installed, so BLAS (MKL / OpenBLAS) keeps the '
            'process-wide thread count from {}={}. Install threadpoolctl to make '
            'the Threads setting affect BLAS as well.'.format(
                'OMP_NUM_THREADS', os.environ.get('OMP_NUM_THREADS', 'unset')))
    except Exception as exc:
        notes.append('Could not limit BLAS threads: {}'.format(exc))

    try:
        import numba
        ceiling = int(numba.config.NUMBA_NUM_THREADS)
        if n_threads > ceiling:
            notes.append(
                'Numba is capped at {} thread(s) for this process (NUMBA_NUM_THREADS '
                'is fixed at import). Restart the GUI to raise the cap.'.format(ceiling))
        numba.set_num_threads(min(n_threads, ceiling))
    except ImportError:
        pass
    except Exception as exc:
        notes.append('Could not set the Numba thread count: {}'.format(exc))

    return (not notes), notes


def apply_thread_limit_in_worker(n_threads: int) -> None:
    # Numba's thread count is thread-local from 0.53 on, so the value set on the
    # Qt main thread does not carry into the thread the solver runs in.
    try:
        import numba
        numba.set_num_threads(min(max(1, int(n_threads)),
                                  int(numba.config.NUMBA_NUM_THREADS)))
    except Exception:
        pass
