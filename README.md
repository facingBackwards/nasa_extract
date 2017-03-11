# nasa_extract
Tool for extracting NASA data from binary archives

### Usage:
    $ ./nasa.py --help
    Usage: nasa.py [OPTIONS] DATA

      Read in NASA Nimbus 4 IRIS data and output to readable format

    Options:
      --json TEXT  Write records to file in JSON format
      -q, --quiet  Don't show record summary
      --help       Show this message and exit.

where DATA is the path to the data file.

---

Currently only output is the number of each type of record or as json

---
### Requirements

* Python 3.6 - Uses f-strings, the rest should be 3.x
* [Click](http://click.pocoo.org/5/) - for the command line stuff
