# Diagram Manual Assistant

Answer upstream, downstream and directed-path questions about labeled manual figures. The bundled SVG shows all six figures and identifies each cited connector.

## Quick start

From this directory, run these commands with Python 3.12 or 3.13. The example corpus is fictional and runs offline with the standard library.

```sh
python3 core.py ask 'What follows hopper in figure 1?'
python3 core.py build data/source.json snapshot.json
python3 core.py ask 'What feeds sorter in figure 1?' --snapshot snapshot.json
python3 -m unittest discover -v
python3 evaluate.py
```

## Asking questions

Specify a figure in every question. Ask “What feeds sorter in figure 1?” or “Path from hopper to sorter in figure 1”.

## Using your own sources

Use the records in `data/source.json` as a schema example. Supply unique citation IDs and usable source locators. Build a new snapshot after additions, edits, or deletions. A successful build atomically replaces the previous snapshot. Results contain the answer, retrieval method and source locators. Unsupported queries return `insufficient_evidence`.

Input is a manually transcribed directed edge list. The assistant uses figure labels and connectivity. It does not interpret arbitrary raster images.

See [QA.md](QA.md) for measured results, review status and release limits.

For a labeled SVG, run `python3 import_figure.py data/manual.svg > edges.json` and build the snapshot from `edges.json`. Each connector carries its evidence ID, figure label, starting component and ending component in XML attributes. The included diagram serves as a working example.
