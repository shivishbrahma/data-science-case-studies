# US Baby Names

## Dataset Description

This dataset contains all of the baby names in the United States from 1880 to 2024. The data is provided by the Social Security Administration (SSA) and includes the name, year of birth, gender, and number of births.

## Data Source

For each year of birth YYYY after 1879, we created a comma-delimited file called yobYYYY.txt. Each
record in the individual annual files has the format "name,sex,number," where name is 2 to 15 characters,
sex is M (male) or F (female) and "number" is the number of occurrences of the name. Each file is sorted
first on sex and then on number of occurrences in descending order. When there is a tie on the number of
occurrences, names are listed in alphabetical order. This sorting makes it easy to determine a name's rank.
The first record for each sex has rank 1, the second record for each sex has rank 2, and so forth.  

### Citation

US Baby Names 1880-2024, Version 1. Retrieved September 21, 2025 from [https://www.ssa.gov/oact/babynames/limits.html](https://www.ssa.gov/oact/babynames/limits.html).

## Notebooks

* [Data Analysis from O&#39; Reilly Book](./01_pydata_analysis_notebook.ipynb)
