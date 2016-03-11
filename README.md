# Dichalcogenides Plots

[![MIT License](https://img.shields.io/github/license/evansosenko/dichalcogenides-plots.svg)](./LICENSE.txt)

## Description

Plots for dichalcogenide systems.

## Requirements

- [Python 3](http://www.python.org/)
  with [pip](http://www.pip-installer.org/).
  Tested with Python 3.5.1 and pip 8.1.0.

## Setup

Install the required Python packages with

```bash
$ pip install -r requirements.txt.lock
```

## Usage

Generate the plots with

```bash
$ make
```

Output will be saved in the `build` directory.

Python output will be redirected to `stdout.log`
and errors to `stderr.log`.

Remove the build and logs with

```bash
$ make clean
```

## License

This code is Copyright © 2015-2016 Evan Sosenko.

## Warranty

This software is provided "as is" and without any express or
implied warranties, including, without limitation, the implied
warranties of merchantibility and fitness for a particular
purpose.
