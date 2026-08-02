# PyMNPBEM v1.0.0

Python port of the [MATLAB MNPBEM toolbox](https://github.com/Nikolaos-Matthaiakakis/MNPBEM)
(Hohenester & Trügler) for simulating the electromagnetic properties of
metallic nanoparticles using the boundary element method (BEM).

> Original MATLAB: Hohenester & Trügler (Comp. Phys. Commun. 183, 370 (2012); 185, 1177 (2014); 193, 138 (2015)).
> The Python port targets bit-similar numerical agreement with MATLAB MNPBEM17
> and adds GPU acceleration, multi-GPU dispatch, and an iterative
> ACA / H-matrix solver for large meshes.

## What is this?

MNPBEM solves Maxwell's equations for dielectric environments in which bodies
with homogeneous and isotropic dielectric functions are separated by abrupt
interfaces. Typical applications include plasmonic nanoparticles in the
optical and near-infrared ranges, such as spheres, rods, cubes, dimers,
particles on substrates, and EELS probes.

The Python port preserves the public class structure and method names of the
MATLAB toolbox, allowing existing MATLAB scripts to be translated almost
mechanically. See [`docs/MIGRATION_GUIDE.md`](docs/MIGRATION_GUIDE.md).

The Python port adds the following features:

- **Python-native API** using `numpy` arrays instead of MATLAB structs.
- **GPU acceleration** through `cupy`, including single-GPU and multi-GPU wavelength dispatch.
- **Iterative solvers** (`BEMRetIter`, `BEMStatIter`) using ACA-compressed
  H-matrices and GMRES, enabling simulations with tens of thousands of boundary elements.
- **Multi-node MPI** wavelength dispatch for spectrum sweeps.
- **Numerical agreement with MATLAB MNPBEM17**, verified demo by demo
  across the complete set of 72 MNPBEM examples.

## Installation

```bash
conda create -n mnpbem python=3.11 -y
conda activate mnpbem

pip install mnpbem               # CPU only (default)
pip install "mnpbem[gpu]"        # GPU acceleration with CuPy and CUDA 12
pip install "mnpbem[gpu,mpi]"    # Multi-node MPI with mpi4py
pip install "mnpbem[all]"        # All optional features: GPU, MPI, and FMM
```

CPU-only installation is the default. GPU, MPI, and FMM dependencies are
installed only when the corresponding extras are requested. At runtime,
PyMNPBEM automatically detects the available capabilities and falls back to
NumPy when GPU dependencies are unavailable.

For complete prerequisites, multi-GPU VRAM sharing, multi-node MPI launch
instructions, environment variables, and troubleshooting, see
[`docs/INSTALL.md`](docs/INSTALL.md).

After installation, verify the package with:

```bash
python -c "import mnpbem; print(mnpbem.__version__)"
python -c "from mnpbem.utils.gpu import has_gpu_capability; has_gpu_capability(verbose=True)"
```

## Quick Start

```python
# Gold sphere extinction spectrum using retarded BEM
import numpy as np
from mnpbem.materials import EpsConst, EpsTable
from mnpbem.geometry import trisphere, ComParticle
from mnpbem.bem import BEMRet
from mnpbem.simulation import PlaneWaveRet

epstab = [EpsConst(1.0), EpsTable("gold.dat")]
p      = ComParticle(epstab, [trisphere(144, 20)], [[2, 1]], 1, interp="curv")
bem    = BEMRet(p)
exc    = PlaneWaveRet(
    np.array([[1.0, 0.0, 0.0]]),
    np.array([[0.0, 0.0, 1.0]])
)

enei = np.linspace(400, 800, 41)
ext  = np.zeros_like(enei)

for i, e in enumerate(enei):
    sig, bem = bem.solve(exc.potential(p, e))
    ext[i]   = float(np.real(np.ravel(exc.extinction(sig))[0]))

print("peak extinction at", enei[ext.argmax()], "nm")  # 510.0
```

A complete spectrum calculation and plotting example is available in
[`examples/01_sphere_extinction.py`](examples/01_sphere_extinction.py).

## Documentation

- [API Reference](docs/API_REFERENCE.md): Every public class and function.
- [Migration Guide from MATLAB](docs/MIGRATION_GUIDE.md): Line-by-line mapping.
- [Examples](examples/): Runnable Python scripts and a Jupyter tutorial.
- [Architecture](docs/ARCHITECTURE.md): Package layout and design notes.
- [Installation](docs/INSTALL.md): Prerequisites, GPU and MPI setup, and troubleshooting.
- [H-matrix on GPU](docs/H_MATRIX_GPU.md): ACA compression and the GPU H-matrix implementation.

## Repository Layout

```text
mnpbem/                  # Python package: geometry, BEM, Green functions, simulation, and related modules
docs/                    # User documentation: API, migration, installation, and architecture
examples/                # Runnable Python examples and a Jupyter tutorial
```

> The original MATLAB MNPBEM17 toolbox is not bundled with this repository.
> It is available from the [author's repository](https://github.com/Nikolaos-Matthaiakakis/MNPBEM).

## License

PyMNPBEM is free software licensed under the **GNU General Public License,
version 2 or, at your option, any later version**
(`SPDX-License-Identifier: GPL-2.0-or-later`).

This project is a Python implementation derived from and inspired by the
MNPBEM Toolbox developed by Ulrich Hohenester and Andreas Trügler. The
original toolbox is distributed under the GNU GPL, version 2 or any later
version. PyMNPBEM is released under the same terms to remain compatible with
the upstream code base.

```text
PyMNPBEM: Python implementation of the MNPBEM toolbox
Copyright (C) 2026 Jaekak Yoo and PyMNPBEM contributors

Based on the MNPBEM Toolbox
Copyright (C) 2017 Ulrich Hohenester and Andreas Trügler

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
```

See the [LICENSE](LICENSE) file, which is identical to `COPYING`, for the full
license text. The phrase "GPL v2" by itself is ambiguous because it does not
distinguish between "version 2 only" and "version 2 or later." Therefore,
every source file includes the
`SPDX-License-Identifier: GPL-2.0-or-later` tag to state the licensing intent
unambiguously.

Under the GPL, you are free to use, modify, redistribute, and commercially
deploy PyMNPBEM. If you distribute a modified version or a derived program,
you must make the corresponding source code available under the same GPL
terms.

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

Please also cite this Python port:

```bibtex
@software{pymnpbem_2026,
  author = {Yoo, Jaekak and Berwick, Ryan Thomas and Oh, Hyuncheol and Lin, Jiamu and Kim, Jae-Myoung and Link, Stephan and Landes, Christy F.},
  title  = {PyMNPBEM: GPU-accelerated boundary element simulations of metallic nanoparticles},
  year   = {TBU},
  url    = {TBU}
}
```
