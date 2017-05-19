# i3 configger

Generate i3 config files from a set of partial config files in a config folder.

Either as script or a deamon watching the folder and triggering a build on changes of one of the .i3config files.

##  Features

* build config as one shot script
* watch a folder for changes and build automatically
* run as deamon or in foreground

##  Planned

* substitution of variables
* dynamic stuff yet to be determined

# Installation

    $ pip install -e "git+https://github.com/obestwalter/i3-configger.git#egg=i3-configger"

# Usage

**Default uses `.i3config` files in `~/.i3/config.d` and writes to `~/.i3/config`.**

one shot:

    $ i3-configger

as daemon:

    $ i3-configger --daemon


more info:

    $ i3-configger --help

# Ideas

## Replace variables

Everything that is set with `set $<whatever> <value>` can be replaced using string template substitutions

It is then possible to switch sets of seetings by simply replacing the source of variables.

## Dynamic settings

Have settings.py instead of (or addtionally to) settings.i3conf that can then automatically adjust to environment changes.

Environment changes that are interesting need to be polled then (e.g. number of connected monitors, processes being spawned, whatever)

... or turn this into a py3status module after all ...
