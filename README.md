A simple JSON to XML converter written in Python for Comédie-Française, using the 'actors' data from Marine Tiger. 

This repository works as follows: there are a number of exported JSONs from the CF project, which live in `json_exports`. 

These files are parsed by the two scripts under `/src`, `generate_prosopography.py` and `generate_plays.py`. 

There are also a number of class files under `/src`, like `attributions.py`, `authors.py`, `comedians.py`, `plays.py`, and `roles.py`. 

Running `generate_prosopography.py` generates the prosopography, but note that there are a few hard-coded paths in there, which would be better off parameterized using `argparse` to pass in from the command line in the future. This would allow the user to pass in values for the template file path, the comedians file path, the authors file path, and the output file path. 

Same goes for the `generate_plays.py`, there are a number of hard-coded file paths in here, such as the location of the template file, the JSONs that are consumed (`json_exports/pièces.json`,`json_exports/auteurs.json`,`json_exports/attributions.json`, `json_exports/rôles.json`), and the output file location. If you need to convert new files, you'll need to update these lines. 
