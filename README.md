# proteomics

## What is this?
This proteomics tollset was created to help my sister analyze results for her PHD thesis. This toolset aims to automate tedious protetomics analysis that involves lots of clicking, copying and pasting data from various programs and excel sheets into a protein to mz value mathcing program. 

## So is this easier?
This replaces manually finding scan results, copying them and then pasting them into an excel sheet (one per scan) with manually batch exporting raw experiment results into mzXML and creating a few csv files. The results are stored as one csv file per scan number and can be opened in excel. 

## Usage:
```./main.py -h```: Displays all command line arguments. All arguments have defaults that will work with a clean clone of this repository

```./main.py```: Will use the sample experiment data in the repository and create the results files

```./main.py --infile foo.mzXML --scans scans.csv```: Use ```foo.mzXML``` as experiment data and look for scan numbers in ```scans.csv```. Creates output in ```results/foo.mzXML```


```./main.py --infile foo.mzXML --scans scans.csv``` --name test: Use ```foo.mzXML``` as experiment data and look for scan numbers in ```scans.csv```.set experiment name to name. Creates output in ```results/test```
