# EvE

EvE - (EvE)aluates Various modEls.

## Installing
//Coming soon™//

## Running
After installation, running EvE is straightforward.
1. **Input Directory** Place all files to process in a dedicated input directory. Import is done by file name so any directory structure is fine.
2. **Output Directory** Create a directory for the outputted files. If no output directory is specified one will be created alongside the input directory.
3. **Run EvE** with the following command:

`python eve.py -i [your input directory] -o [your output directory]`

Optionally, use the '-w' flag to set the number of parallel workers. If unset the default is 4.

## Auto Importer
The importer works by first looking for all files ending in ".tif"

Then finds all annotation files ending in .geojson containing the same image name

### Mask File
Mask files should follow this naming pattern:

`[image name].ome.tif - Image[optional number]_[model name]_label.tif`

### Annotations File
Annotation files should follow this naming pattern:

`[image name].ome.tif - Image[optional number].geojson`


Future of this document:
1. How to install
2. How to run
3. What inputs it takes
4. What outputs it gives
5. What processing it does
