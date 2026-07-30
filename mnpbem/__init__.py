# PyMNPBEM - Python implementation of the MNPBEM toolbox
#
# Copyright (C) 2026 Jaekak Yoo and PyMNPBEM contributors
#
# Based on the MNPBEM Toolbox
# Copyright (C) 2017 Ulrich Hohenester and Andreas Truegler
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
MNPBEM - Metallic Nanoparticle Boundary Element Method
Python implementation of the MATLAB MNPBEM toolbox

Main modules:
- materials: Dielectric functions (EpsConst, EpsTable, EpsDrude)
- geometry: Particle geometries and mesh generation
- greenfun: Green's functions (static and retarded)
- bem: BEM solvers
- simulation: External excitations (plane wave, dipole, EELS)
- spectrum: Far-field and scattering cross sections
- mie: Mie theory for spherical and ellipsoidal particles
- misc: Math, distance, plotting, and other utilities
"""

__version__ = "1.0.0"

# Materials: dielectric functions
from .materials import EpsConst, EpsTable, EpsDrude, EpsFun, epsfun, EpsNonlocal, make_nonlocal_pair

# Geometry: particles, mesh generators, and connectivity
from .geometry import (
    Particle,
    ComParticle,
    ComParticleMirror,
    CompStructMirror,
    Point,
    ComPoint,
    EdgeProfile,
    Polygon,
    Polygon3,
    trisphere,
    trirod,
    tricube,
    tritorus,
    trispheresegment,
    trispherescale,
    tripolygon,
    fvgrid,
    connect,
)

# Green's functions: static, retarded, mirror, layer, ACA
from .greenfun import (
    GreenStat,
    CompGreenStat,
    CompGreenRet,
    CompStruct,
    CompGreenStatMirror,
    CompGreenRetMirror,
    CompGreenStatLayer,
    CompGreenRetLayer,
    CompGreenTabLayer,
    GreenRetLayer,
    GreenTabLayer,
    ClusterTree,
    HMatrix,
    ACACompGreenStat,
    ACACompGreenRet,
    ACACompGreenRetLayer,
    greenfunction,
)

# BEM: abstract base class
from .bem import BemBase

# BEM solvers: static, retarded, mirror, layer, iterative
from .bem import (
    BEMStat,
    BEMRet,
    BEMStatMirror,
    BEMRetMirror,
    BEMStatEig,
    BEMStatEigMirror,
    BEMLayerMirror,
    BEMStatLayer,
    BEMRetLayer,
    BEMIter,
    BEMStatIter,
    BEMRetIter,
    BEMRetLayerIter,
    plasmonmode,
)

# Simulation: plane wave, dipole, EELS excitations
from .simulation import (
    PlaneWaveStat,
    PlaneWaveRet,
    DipoleStat,
    DipoleRet,
    PlaneWaveStatMirror,
    PlaneWaveRetMirror,
    DipoleStatMirror,
    DipoleRetMirror,
    EELSBase,
    EELSStat,
    EELSRet,
    PlaneWaveStatLayer,
    PlaneWaveRetLayer,
    DipoleStatLayer,
    DipoleRetLayer,
    MeshField,
    dipole,
    planewave,
    electronbeam,
)

# Spectrum: far-field and cross section calculations
from .spectrum import (
    SpectrumRet,
    SpectrumStat,
    SpectrumRetLayer,
    SpectrumStatLayer,
    spectrum,
)

# Mie theory: spherical harmonics, Mie solvers
from .mie import (
    spharm,
    sphtable,
    vecspharm,
    MieGans,
    MieStat,
    MieRet,
    mie_solver,
)

# Misc: math, distance, units, options, shapes, plotting, etc.
from .misc import (
    matmul,
    inner,
    outer,
    matcross,
    vec_norm,
    vec_normalize,
    spdiag,
    pdist2,
    bradius,
    bdist2,
    distmin3,
    EV2NM,
    BOHR,
    HARTREE,
    FINE,
    bemoptions,
    getbemoptions,
    getfields,
    Tri,
    Quad,
    lglnodes,
    lgwt,
    IGrid2,
    IGrid3,
    ValArray,
    VecArray,
    QuadFace,
    triangle_unit_set,
    trisubdivide,
    BemPlot,
    arrowplot,
    coneplot,
    coneplot2,
    mycolormap,
    particlecursor,
    nettable,
    patchcurvature,
    memsize,
    round_left,
    Mem,
    multi_waitbar,
)

# Utils: parallel computation
from .utils import (
    compute_spectrum,
    compute_spectrum_parallel,
)

__all__ = [
    # Materials
    "EpsConst",
    "EpsTable",
    "EpsDrude",
    "EpsFun",
    "epsfun",
    "EpsNonlocal",
    "make_nonlocal_pair",
    # Geometry
    "Particle",
    "ComParticle",
    "ComParticleMirror",
    "CompStructMirror",
    "Point",
    "ComPoint",
    "EdgeProfile",
    "Polygon",
    "Polygon3",
    "trisphere",
    "trirod",
    "tricube",
    "tritorus",
    "trispheresegment",
    "trispherescale",
    "tripolygon",
    "fvgrid",
    "connect",
    # Green's functions
    "GreenStat",
    "CompGreenStat",
    "CompGreenRet",
    "CompStruct",
    "CompGreenStatMirror",
    "CompGreenRetMirror",
    "CompGreenStatLayer",
    "CompGreenRetLayer",
    "CompGreenTabLayer",
    "GreenRetLayer",
    "GreenTabLayer",
    "ClusterTree",
    "HMatrix",
    "ACACompGreenStat",
    "ACACompGreenRet",
    "ACACompGreenRetLayer",
    "greenfunction",
    # BEM base
    "BemBase",
    # BEM solvers
    "BEMStat",
    "BEMRet",
    "BEMStatMirror",
    "BEMRetMirror",
    "BEMStatEig",
    "BEMStatEigMirror",
    "BEMLayerMirror",
    "BEMStatLayer",
    "BEMRetLayer",
    "BEMIter",
    "BEMStatIter",
    "BEMRetIter",
    "BEMRetLayerIter",
    "plasmonmode",
    # Simulation
    "PlaneWaveStat",
    "PlaneWaveRet",
    "DipoleStat",
    "DipoleRet",
    "PlaneWaveStatMirror",
    "PlaneWaveRetMirror",
    "DipoleStatMirror",
    "DipoleRetMirror",
    "EELSBase",
    "EELSStat",
    "EELSRet",
    "PlaneWaveStatLayer",
    "PlaneWaveRetLayer",
    "DipoleStatLayer",
    "DipoleRetLayer",
    "MeshField",
    "dipole",
    "planewave",
    "electronbeam",
    # Spectrum
    "SpectrumRet",
    "SpectrumStat",
    "SpectrumRetLayer",
    "SpectrumStatLayer",
    "spectrum",
    # Mie theory
    "spharm",
    "sphtable",
    "vecspharm",
    "MieGans",
    "MieStat",
    "MieRet",
    "mie_solver",
    # Misc: math utilities
    "matmul",
    "inner",
    "outer",
    "matcross",
    "vec_norm",
    "vec_normalize",
    "spdiag",
    # Misc: distance utilities
    "pdist2",
    "bradius",
    "bdist2",
    "distmin3",
    # Misc: units / constants
    "EV2NM",
    "BOHR",
    "HARTREE",
    "FINE",
    # Misc: options
    "bemoptions",
    "getbemoptions",
    "getfields",
    # Misc: shapes
    "Tri",
    "Quad",
    # Misc: Gauss-Legendre
    "lglnodes",
    "lgwt",
    # Misc: grids
    "IGrid2",
    "IGrid3",
    # Misc: arrays
    "ValArray",
    "VecArray",
    # Misc: quadface
    "QuadFace",
    "triangle_unit_set",
    "trisubdivide",
    # Misc: plotting
    "BemPlot",
    "arrowplot",
    "coneplot",
    "coneplot2",
    "mycolormap",
    "particlecursor",
    # Misc: other utilities
    "nettable",
    "patchcurvature",
    "memsize",
    "round_left",
    "Mem",
    "multi_waitbar",
    # Utils: parallel
    "compute_spectrum",
    "compute_spectrum_parallel",
]
