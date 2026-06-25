# EvE

## Installing
//Coming soon™//

## Running
After installation running EvE is pretty straightforward.
1. Place all files you wish to process in a dedicated directory. (Importation is done by file name so any file structure within this directory will work.)
2. Decide on an output directory. This should be separate from the input directory. If no output directory is specified one will be automatically created in the same directory as the input directory.
3. Run EvE like so: `python eve.py -i [your input directory] -o [your output directory]`

You can optionally set the number of parallel workers to use with the '-w' flag.

## Auto Importer
The import works by first looking for all files ending in ".tif"

Then finds all annotation files ending in .geojson containing the same image name

### Mask File
Mask files should follow this naming pattern:

`[image name].ome.tif - Image[optional number]_[model name]_label.tif`

### Annotations File
Annotation files should follow this naming pattern:

`[image name].ome.tif - Image[optional number].geojson`



