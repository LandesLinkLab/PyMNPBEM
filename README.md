# PyMNPBEM v1.0.0

Python port of the [MATLAB MNPBEM toolbox](https://physik.uni-graz.at/de/mnpbem/)
(Hohenester & Trügler) for the simulation of electromagnetic properties of
metallic nanoparticles using the boundary element method (BEM).

> Original MATLAB: Hohenester & Trügler (Comp. Phys. Commun. 183, 370 (2012); 185, 1177 (2014); 193, 138 (2015)).
> Python port targets bit-similar numerical agreement with MATLAB MNPBEM17,
> while adding GPU acceleration, multi-GPU dispatch, and an iterative
> ACA / H-matrix solver for large meshes.

## What is this?

MNPBEM solves Maxwell's equations for dielectric environments where bodies
with homogeneous and isotropic dielectric functions are separated by abrupt
interfaces. Typical applications are plasmonic nanoparticles in the optical
and near-infrared range (sphere, rod, cube, dimer, particles on substrate,
EELS probes, ...).

The Python port keeps the public class structure and method names of the
MATLAB toolbox so that existing MATLAB scripts can be translated almost
mechanically (see `docs/MIGRATION_GUIDE.md`). What the Python port adds:

- **Python-native API** with `numpy` arrays instead of MATLAB structs.
- **GPU acceleration** via `cupy` (single GPU and multi-GPU wavelength dispatch).
- **Iterative solver** (`BEMRetIter`, `BEMStatIter`) using ACA-compressed
  H-matrices and GMRES — scales to tens of thousands of boundary elements.
- **Multi-node MPI** wavelength dispatch for spectrum sweeps.
- **Numerical agreement with MATLAB MNPBEM17**, verified demo by demo over
  the full set of 72 MNPBEM demos.


## Installation

```bash
conda create -n mnpbem python=3.11 -y
conda activate mnpbem

pip install mnpbem               # CPU only (default)
pip install "mnpbem[gpu]"        # + GPU acceleration (cupy / CUDA 12)
pip install "mnpbem[gpu,mpi]"    # + multi-node MPI (mpi4py)
pip install "mnpbem[all]"        # everything (gpu + mpi + fmm)
```

CPU-only is the default — GPU / MPI / FMM dependencies are pulled only
when the matching extra is requested. The runtime auto-detects what is
available and falls back to NumPy when GPU dependencies are missing.

For full prerequisites, multi-GPU VRAM share, multi-node MPI launch,
environment variables, and troubleshooting, see
[docs/INSTALL.md](docs/INSTALL.md).

After install, verify:

```bash
python -c "import mnpbem; print(mnpbem.__version__)"
python -c "from mnpbem.utils.gpu import has_gpu_capability; has_gpu_capability(verbose=True)"
```

## Quick Start

```python
# Gold sphere extinction spectrum (retarded BEM)
import numpy as np
from mnpbem.materials import EpsConst, EpsTable
from mnpbem.geometry import trisphere, ComParticle
from mnpbem.bem import BEMRet
from mnpbem.simulation import PlaneWaveRet

epstab = [EpsConst(1.0), EpsTable("gold.dat")]
p      = ComParticle(epstab, [trisphere(144, 20)], [[2, 1]], 1, interp="curv")
bem    = BEMRet(p)
exc    = PlaneWaveRet(np.array([[1.0, 0.0, 0.0]]), np.array([[0.0, 0.0, 1.0]]))

enei   = np.linspace(400, 800, 41)
ext    = np.zeros_like(enei)
for i, e in enumerate(enei):
    sig, bem = bem.solve(exc.potential(p, e))
    ext[i]   = float(np.real(np.ravel(exc.extinction(sig))[0]))

print("peak extinction at", enei[ext.argmax()], "nm")   # 510.0
```

A complete worked spectrum + plot is in [`examples/01_sphere_extinction.py`](examples/01_sphere_extinction.py).

## Documentation

- [API Reference](docs/API_REFERENCE.md) — every public class and function.
- [Migration Guide (from MATLAB)](docs/MIGRATION_GUIDE.md) — line-by-line mapping.
- [Examples](examples/) — runnable Python scripts and a Jupyter tutorial.
- [Architecture](docs/ARCHITECTURE.md) — package layout and design notes.
- [Installation](docs/INSTALL.md) — prerequisites, GPU / MPI setup, troubleshooting.
- [H-matrix on GPU](docs/H_MATRIX_GPU.md) — ACA compression and the GPU H-matrix path.

## Repository Layout

```
mnpbem/                  # Python package (geometry, bem, greenfun, simulation, ...)
docs/                    # User documentation (API, migration, install, architecture)
examples/                # Runnable Python examples + Jupyter tutorial
```

> The original MATLAB MNPBEM17 toolbox is **not** bundled here. It is available
> from the [author's site](https://physik.uni-graz.at/de/mnpbem/).

## License

PyMNPBEM is free software licensed under the **GNU General Public License,
version 2 or, at your option, any later version**
(`SPDX-License-Identifier: GPL-2.0-or-later`).

This project is a Python implementation derived from and inspired by the
MNPBEM Toolbox developed by Ulrich Hohenester and Andreas Trügler, which is
itself distributed under the GNU GPL, version 2 or any later version.
PyMNPBEM is released under the same terms to remain compatible with the
upstream code base.

```
PyMNPBEM - Python implementation of the MNPBEM toolbox
Copyright (C) 2026 Jaekak Yoo and PyMNPBEM contributors

Based on the MNPBEM Toolbox
Copyright (C) 2017 Ulrich Hohenester and Andreas Trügler

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
```

See the [LICENSE](LICENSE) file (identical to `COPYING`) for the full license
text. "GPL v2" on its own would be ambiguous between *only* and *or later*, so
every source file carries an `SPDX-License-Identifier: GPL-2.0-or-later` tag
to state the intent unambiguously.

Under the GPL you are free to use, modify, redistribute, and commercially
deploy PyMNPBEM. If you distribute a modified version or a derived program,
you must make its source available under the same GPL terms.

## Citation

When publishing results obtained with this Python port, please cite the
original MNPBEM papers:

```bibtex
@article{hohenester2012mnpbem,
  author  = {Hohenester, U. and Tr\"ugler, A.},
  title   = {{MNPBEM} -- A {Matlab} toolbox for the simulation of plasmonic nanoparticles},
  journal = {Comput. Phys. Commun.},
  volume  = {183},
  pages   = {370--381},
  year    = {2012}
}
@article{hohenester2014simulation,
  author  = {Hohenester, U.},
  title   = {Simulating electron energy loss spectroscopy with the {MNPBEM} toolbox},
  journal = {Comput. Phys. Commun.},
  volume  = {185},
  pages   = {1177--1187},
  year    = {2014}
}
@article{waxenegger2015plasmonics,
  author  = {Waxenegger, J. and Tr\"ugler, A. and Hohenester, U.},
  title   = {Plasmonics simulations with the {MNPBEM} toolbox: Consideration of substrates and layer structures},
  journal = {Comput. Phys. Commun.},
  volume  = {193},
  pages   = {138--150},
  year    = {2015}
}
```

In addition, please cite this Python port:

```bibtex
@software{pymnpbem_2026,
  author = {Yoo, Jaekak},
  title  = {{PyMNPBEM} (v1.0.0)},
  year   = {2026},
  url    = {https://github.com/Yoo-JK/PyMNPBEM},
  note   = {Python port of MNPBEM17 with GPU acceleration and ACA / H-matrix solvers.}
}
```

## Bug Reports & Contributions

Please open an issue on GitHub. When reporting a numerical discrepancy
against MATLAB MNPBEM17, include:
- Python version, `mnpbem.__version__`, `numpy.__version__`
- Mesh parameters (e.g. `trisphere(144, 20)`)
- A minimal script that reproduces the discrepancy
- Expected MATLAB output (preferably from the same demo file in `Demo/`)
