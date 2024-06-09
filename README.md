# missing-version-streams

Scans a package directory, and looks for applications which 'may' be missing
version streams.

## Pre-requisites

Local clones of the following repositories:
- [wolfi-dev/os](https://github.com/wolfi-dev/os)
- [chainguard-dev/package-version-metadata](https://github.com/chainguard-dev/package-version-metadata)
- [endoflife-date/endoflife.date](https://github.com/endoflife-date/endoflife.date)

## Usage

Run the script using the following command:

```bash
python3 missing_version_streams.py \
  --package-repo ~/work/wolfi-os \
  --version-streams-repo ~/work/package-version-metadata/version_streams \
  --endoflife-repo ~/work/scratch/endoflife.date/products
```

## Output

The script will generate two files with the results:

**wolfi-versioned-but-missing-version-stream.txt**: Lists Wolfi packages with
version numbers in their names but missing a version stream.

**endoflife-versioned-but-missing-in-wolfi.txt:** Lists packages found on
endoflife.date but missing a version stream in Wolfi.

The summary will be printed to the console:

```bash
Summary:
  Wolfi packages with version numbers in their name, but missing a version stream: 59
  Wolfi packages found on endoflife.date, but missing a version stream: 37

See the individual files for details:
  - wolfi-versioned-but-missing-version-stream.txt
  - endoflife-versioned-but-missing-in-wolfi.txt
```