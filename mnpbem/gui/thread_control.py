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

    # NUMBA_NUM_THREADS needs care in both directions. Numba latches the value at
    # import, but re-reads the environment on every compile (config.reload_config()
    # from numba.core.compiler); if the two disagree after the thread pool is up it
    # raises, which is what setup_env() lowering the variable used to trigger on the
    # first jit call -- long after this function returned successfully. Note that
    # set_num_threads() itself launches the pool, so it must not run before the two
    # are reconciled.
    try:
        import numba

        from numba.core import config as numba_config

        try:
            from numba.np.ufunc import parallel as numba_parallel
            launched = bool(getattr(numba_parallel, '_is_initialized', False))
        except Exception:
            # Unknown state: assume launched, which is the conservative branch.
            launched = True

        if not launched:
            # The pool comes up at whatever the environment says, so asking numba to
            # re-read it now gives a genuine n_threads-wide pool rather than a wide
            # pool with threads masked off.
            os.environ['NUMBA_NUM_THREADS'] = str(n_threads)
            numba_config.reload_config()
        else:
            # The pool is already this wide and cannot be resized. Put the variable
            # back so the next reload_config() agrees with reality; the count the
            # user asked for is applied by masking below.
            os.environ['NUMBA_NUM_THREADS'] = str(int(numba_config.NUMBA_NUM_THREADS))

        ceiling = int(numba_config.NUMBA_NUM_THREADS)
        if n_threads > ceiling:
            notes.append(
                'Numba is capped at {} thread(s) for this process (its thread pool '
                'was already launched). Restart the GUI to raise the cap.'.format(ceiling))
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
