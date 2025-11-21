# Repository Inventory

This document lists every top-level directory and Python module in the repository, together with a short description so you can decide which building blocks to re‑implement or keep when rebuilding the GUI.

## Top-Level Directories & Files

| Path | Description |
| --- | --- |
| `README.md` | Project overview, install instructions, and a short description of the processing stack. |
| `MANUAL.md` | User workflow notes (CLI usage, data locations, etc.). |
| `pyproject.toml` / `setup.py` | Build metadata for the `openseismicprocessing` package. |
| `requirements.txt` / `requirements-cpu.txt` | Dependency lists (GPU-enabled vs CPU-only). |
| `build/` | Build artifacts from previous `pip install .` or `python -m build` runs. |
| `catalog/golem_catalog.db` | SQLite database used by `catalog.steps` for pipeline templates. |
| `examples/` | Runnable notebooks/scripts demonstrating SEG-Y reading and wavelet estimation. |
| `gui/` | Currently empty; previously hosted the PySide/PyQt interface. Safe to repopulate. |
| `lib/` | CUDA source (`eikonal2D.cu`), compiled `libEikonal.so`, and the compile command used to produce it. |
| `scripts/` | Reserved for helper scripts (currently empty). |
| `src/` | Source tree for the Python package plus egg-info metadata. |
| `tmp_usage.py` | Scratch file showing how to instantiate processing pipelines. |

## Python Package (`src/openseismicprocessing`)

Public modules mirror private underscore-prefixed implementations; most public files expose friendly APIs while the underscored counterparts host the heavy lifting.

| Module | Purpose |
| --- | --- |
| `__init__.py` | Declares the package version and re-exports `SignalProcessing`. |
| `SignalProcessing.py` | Convenience façade exporting all public API functions (I/O, processing, plotting, pipeline, zarr helpers). Import this when users call `from openseismicprocessing import …`. |
| `_io.py` | Low-level SEG-Y reading utilities built around `segyio` (open files, parse text/binary headers, gather trace headers/data). |
| `io.py` | High-level I/O helpers that operate on a shared `context` dict: read traces, store geometry to Parquet, fetch headers, map `.npy`/Parquet data, etc. |
| `_processing.py` | Core numerical routines (resampling, muting, stacking, designing wavelets/convolution operators, applying designature filters, coordinate scaling, etc.). |
| `processing.py` | User-facing wrappers that validate context, call the `_processing` primitives, and add domain-specific helpers such as `generate_local_coordinates` or `kill_traces_outside_box`. |
| `_plotting.py` | Matplotlib/plotly plotting primitives for sections, comparisons, spectra, and acquisition maps. |
| `plotting.py` | Thin wrappers that expose plotting calls with consistent signatures for notebooks/CLI scripts. |
| `_migration.py` | Interfaces with the CUDA `libEikonal.so` library (traveltime tables, eikonal solvers). |
| `migration.py` | Friendly API around `_migration`, selecting CPU/GPU paths depending on availability. |
| `pipeline.py` | Declarative pipeline runner: executes ordered `(function, kwargs)` steps, resolves `@context` references, and materializes a context dictionary. Includes `print_pipeline_steps`. |
| `catalog/steps.py` | Defines reusable pipeline step groups (ingestion, QC, migration) referenced by the SQLite catalog. Useful for templating user-defined flows. |
| `processing.py` helpers | Functions like `subset_geometry_by_condition`, `scale_coordinate_units`, `zero_phase_wavelet`, `apply_designature`, etc., ready to be chained inside pipelines. |
| `plotting.py` helpers | Visualization entry points: `plot_seismic_image`, `plot_seismic_comparison_with_trace`, `plot_spectrum`, `plot_acquisition`, `plot_seismic_image_interactive`. |
| `migration.py` helpers | Functions for numerical migration/matrix building that offload compute to `libEikonal.so` when available. |
| `zarr_utils.py` | Zarr/SEG-Y interoperability utilities: convert SEG-Y directories to Zarr, preview headers, slice datasets, extract metadata, and scale coordinates. |
| `catalog/__init__.py` | Exposes catalog helpers for building GUIs or CLIs that need human-readable step lists. |
| `lib/libEikonal.so` | Bundled shared library (loaded at runtime). |

## Supporting Metadata

| Path | Description |
| --- | --- |
| `src/openseismicprocessing/golem.egg-info/` | Installed-package metadata (entry points, dependency lists). |
| `src/openseismicprocessing/relation.csv` | Lookup table mapping SEG-Y header mnemonics to descriptions/units. |
| `build/lib/...` | Previously built copies of the `openseismicprocessing` package; can be regenerated. |

## Examples & Utilities

| Path | Description |
| --- | --- |
| `examples/SegyRead.ipynb` | Guided SEG-Y ingest tutorial using the I/O helpers. |
| `examples/segyRead2D.py` | CLI example that reads a 2D SEG-Y file and plots a section. |
| `examples/WaveletEstimation.ipynb` | Notebook demonstrating `zero_phase_wavelet`/`calculate_convolution_operator`. |
| `tmp_usage.py` | Minimal script showing how to assemble a pipeline and inspect outputs. |

Use this inventory to decide which functional areas (I/O, processing, plotting, migration, pipelines, zarr conversion) you want to expose in the future GUI. Each Python module listed above already provides the core functions; a new interface can import from `openseismicprocessing.SignalProcessing` and call the necessary helpers without depending on the removed PySide/PyQt files.
