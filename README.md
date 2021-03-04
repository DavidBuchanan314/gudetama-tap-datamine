# gudetama-tap-datamine
Datamining scripts and information for the Gudetama Tap! mobile app.

`scripts/download_latest_data.py` is a python script which downloads the latest
game data archive from the servers (to `./datfiles/`), parses all the game data out
into semi-human-readable JSON files (to `./jsonfiles/`).

### How it works

The game uses a custom object serialisation format, referred to internally as
`CompatibleDataIO`. There are a whole bunch of different object types (see
`scripts/obj_ids.py` for a list), and each one has its own read/write function,
for deserialisation/serialisation.

The code is all written in ActionScript3, which can be trivially decompiled using
`ffdec`. With the decompiled source code written to `./decompiled/`, the python
script `scripts/parser_generator.py` ingests the AS3 source, extracts all the
type information, and then spits out a new python source file -
`scripts/compound_obj_parser.py`. This auto-generated file will now contain
parsers for all objects used by the game data files.
