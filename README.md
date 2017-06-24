# Dichalcogenides Plots

[![MIT License](https://img.shields.io/github/license/evansosenko/dichalcogenides-plots.svg)](./LICENSE.txt)

## Description

Plots for dichalcogenide systems.

## Requirements

- [Python 3](http://www.python.org/)
  with [pip](http://www.pip-installer.org/).
  Tested with Python 3.5.1 and pip 8.1.1.

## Setup

Install the required Python packages with

```bash
$ pip install -r requirements.txt.lock
```

Alternatively, install the unlocked (untested) dependencies with,

```bash
$ pip install -r requirements.txt
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

This code is licensed under the MIT license.

Any figures or other output generated to be identical or otherwise indistinguishable
to the figures submitted to APS are Copyright © 2017 by the American Physical Society.

## Warranty

This software is provided by the copyright holders and contributors "as is" and
any express or implied warranties, including, but not limited to, the implied
warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall the copyright holder or contributors be liable for
any direct, indirect, incidental, special, exemplary, or consequential damages
(including, but not limited to, procurement of substitute goods or services;
loss of use, data, or profits; or business interruption) however caused and on
any theory of liability, whether in contract, strict liability, or tort
(including negligence or otherwise) arising in any way out of the use of this
software, even if advised of the possibility of such damage.
