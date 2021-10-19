# assessed-cloud-fbks

[![DOI](https://zenodo.org/badge/353136800.svg)](https://zenodo.org/badge/latestdoi/353136800)


This code compares GCM cloud feedback components to expert-assessed feedbacks from [Sherwood et al. (2020)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019RG000678). To use, follow these steps:

1. Install CDAT via conda following [these instructions](https://github.com/CDAT/cdat/wiki/install#installing-latest-cdat---821)

2. Activate this environment:
```
conda activate cdat
```
3. Clone this repo:
```
git clone https://github.com/qinyia/assessed-cloud-fbks.git
```
4. cd to assessed-cloud-fbks/code/

5. In main.py, update the "User Input" section so it points to your model's amip and amip-p4K files.

6. Run the code:
```
python main.py
```
7. Inspect the generated figures and tables in the /figures/ directory.
