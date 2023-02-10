# assessed-cloud-fbks

[![DOI](https://zenodo.org/badge/353136800.svg)](https://zenodo.org/badge/latestdoi/353136800)

## Description
This code performs the analysis of [Zelinka et al. (2022)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021JD035198). It computes GCM cloud feedback components and compares them to the expert-assessed values from [Sherwood et al. (2020)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019RG000678). 

## Instructions
To use, follow these steps:

1. Activate the environment for diag_feedback_E3SM:
```
conda activate diagfbk
```
3. Clone this repo:
```
git clone https://github.com/qinyia/assessed-cloud-fbks.git
```
4. cd to assessed-cloud-fbks/code/

5. link the cases_lookup.py from diag_feedback_E3SM:
```
ln -s /dir/of/diag_feedback_E3SM/cases_lookup.py .
```

6. In main.py, update the "User Input" section so it points to your model's amip and amip-p4K files.

7. Run the code:
```
python main.py
```

8. Inspect the generated figures and tables in the /figures/[version]/ directory.


## History
- Oct 19, 2021: modified by Yi Qin to read raw E3SM model data.

=======

## References
- Zelinka et al. (2022): [Evaluating climate models’ cloud feedbacks against expert judgement](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021JD035198), <em>J. Geophys. Res.</em>, 127, e2021JD035198, doi:10.1029/2021JD035198.

- Sherwood et al. (2020): [A combined assessment of Earth’s climate sensitivity](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2019RG000678), <em>Rev. Geophys.</em>, 58, e2019RG000678, doi:10.1029/2019RG000678.
