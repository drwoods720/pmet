# EvE
EvE - (EvE)aluates Various modEls

EvE is a cell segmentation model evaluation tool. The aim for EvE was to create 
a quantitative method to evaluate the results of a cell segmentation model without
requiring a manually generated segmentation mask to compare to.

## Inputs


## Outputs
Outputs are written to a specified output directory.
If no output directory is specified outputs will be written to a directory alongside
the input directory.

EvE produces 2 outputs:

# Installing

## Option 1: Run using the Apptainer container (recommended)

### Prerequisites
- Apptainer 1.5+
  
### Getting the container

#### Download pre-built container from Github
Download the .sif file from the [releases](https://github.com/drwoods720/EvE/releases) section.

#### Or build locally
Clone the repository
```bash
git clone https://github.com/drwoods720/EvE.git
```

Navigate to the apptainer directory
```bash
cd EvE/apptainer
```

Build the container
```bash
apptainer build eve.sif eve.def
```

### Run
```bash
apptainer run eve.sif --help
```

## Option 2: Run locally

### Prerequisites
- Python 3.14+
- pip

### Clone the repository
```bash
git clone https://github.com/drwoods720/EvE.git
cd EvE
```
### Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Run
```bash
python eve.py --help
```

# Usage

Running EvE can be done directly with python or using the Apptainer container.

## Apptainer container

Basic usage:
``` bash
apptainer run eve.sif -i [/path/to/input] -o [/path/to/output]
```

## Options
| Option | Description |
|----------|-------------|
| `-h` or `--help` | Show the help message and exit. |
| `-i` or `--input` | **(Required)** Specify the input directory. |
| `-o` or `--output` | Specify the output directory. |
| `-w` or `--workers` | Specify the maximum number of parallel processors. |

Future of this document:
1. How to install (done)
2. How to run
3. What inputs it takes
4. What outputs it gives
5. What processing it does
