# Oceanography dataset choices and notebook notes

Checked October 13, 2026. Primary environment: CloudBank Classroom JupyterHub; also portable to local Jupyter or Colab.

## Recommended: CCHDO GO-SHIP P02W 2022 CTD profiles

The notebook uses real observations from R/V Roger Revelle, cruise `33RR20220430`, stations 3, 50, and 100, cast 1, restricted to pressure <=600 dbar. The 83 KB source CSV is bundled and retained exactly, including its units row. There are 682 pressure-level observations: 679 have acceptable temperature and salinity flags (2); three surface rows are interpolated (flag 6). The strict analysis keeps flag 2 only. Station 3 ends at 158 dbar, while the other selected casts reach 600 dbar. This supplies a useful lesson about unequal sampling coverage.

Primary sources:

- [CCHDO cruise, investigators, history, and full data](https://cchdo.ucsd.edu/cruise/33RR20220430).
- [NOAA PMEL ERDDAP variable metadata, units, QC conventions, and explicit CC0-1.0 declaration](https://data.pmel.noaa.gov/generic/erddap/info/cchdo_ctd/index.html).
- The exact subset request, hash, and scientific credit are in `../data/oceanography/provenance.json`.

Credit CCHDO, GO-SHIP P02W investigators, NOAA PMEL ERDDAP, and chief scientists Alison Macdonald and Shuwen Tan. The NOAA endpoint declares [CC0-1.0](https://creativecommons.org/publicdomain/zero/1.0/). A cached copy is reproducible; a fresh download may change after scientific reprocessing.

Data dictionary: pressure is sea-water pressure in dbar; temperature is in-situ °C on ITS-90; practical salinity is dimensionless PSS-78. Latitude/longitude are degrees north/east and timestamps are UTC. **Do not equate pressure with depth or practical salinity with grams per kilogram.** WOCE CTD flag 6 means interpolation over more than 2 dbar, not a replicate average.

Teaching/research questions:

1. How do temperature and salinity vary vertically, and where do the profiles diverge?
2. How does lower-minus-upper temperature differ between casts using a common pressure interval?
3. How does the answer change with an interpolation policy or incomplete vertical coverage?
4. What additional repeated observations would test a temporal trend at a fixed location?

The notebook includes two profile charts, band means with coverage status and counts, an interactive chart tool, four participant AI prompts, and CSV/PNG/JSON exports. It treats pressure levels as samples within casts, not independent spatial replicates. Comparisons describe these casts only.

## Alternative: NOAA OISST v2.1

Use a cached 30–90 day subset at one fixed grid cell or a small region for a second session. Questions: what is the seasonal temperature pattern, and how do anomalies differ from absolute SST? Daily global 0.25° values combine observations and interpolate gaps; they are not individual sensor measurements. The notebook would need a different loader and treatment of uncertainty/land mask. Select final historical files instead of preliminary recent data.

- [NOAA OISST product and methods](https://www.ncei.noaa.gov/products/optimum-interpolation-sst).
- [NCEI metadata and dataset citation/constraints](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01606).
- [Dataset DOI](https://doi.org/10.25921/RE9P-PT57).

The metadata directs users to cite the dataset and its CDR use agreement; check those terms with the selected download endpoint. Use °C for SST and report the anomaly reference period. Full global daily files are unnecessary for a short workshop; pre-subset with ERDDAP and cache the result.

## Alternative: Argo profiling-float observations

Use one float, two or three historical cycles, and pressure/temperature/salinity adjusted variables with documented flags. Questions: how does upper-ocean structure vary across successive float profiles, and what is confounded by float movement? Teach real-time versus delayed-mode QC and trajectory before comparing cycles.

- [NOAA AOML Argo program and free data access](https://www.aoml.noaa.gov/proj/argo/).
- [Argo international data access](https://argo.ucsd.edu/data/).
- [Argo data acknowledgement](https://argo.ucsd.edu/data/acknowledging-argo/).

Argo's program pages describe freely available data; retain the required scientific acknowledgement and check the float/product metadata rather than assuming every source has the same license. NetCDF decoding requires `xarray` and a NetCDF backend, or use an ERDDAP CSV subset. Those dependencies are not needed by the supplied CTD notebook.

## Requirements and verification

Core notebook packages: `numpy>=1.24`, `pandas>=1.5`, `matplotlib>=3.7`, `ipywidgets>=8.0`. No GPU, model downloads, secrets, cloud credentials, or paid APIs. Setup installs missing packages only; run it in the classroom image before participants arrive. The complete workshop folder runs without source network access after packages are available. Standalone notebook fallback fetches the same public NOAA subset with a 45-second timeout and tells users to upload the cache if the source is unavailable.

Execution results and figure inspection are recorded in `../verification/02_oceanography_verification.json`. On the original cache, the three lower-minus-upper temperature differences are approximately -4.195, -3.672, and -4.325°C for stations 3, 50, and 100 respectively; regenerate the comparison to check the values. These differences compare pressure bands in casts at different locations/dates and do not establish a warming trend.
