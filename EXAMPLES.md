# Command line examples

Note: The command line examples below are wrapped with a python helper function,
so that they can be tested the same way as other python code.
Just remove the wrapping `shell('...')` to use in BASH or another shell.

```
>>> import subprocess
>>> def shell(command):
...     result = subprocess.run(
...         command, shell=True, check=True, 
...         capture_output=True, text=True)
...     print(result.stdout.strip())

```

`concertina-helper` is a command line tool to help find good fingerings.
Only two arguments are required: An input file, and a layout:

```
>>> shell('concertina-helper tests/g-major.abc --layout_name 30_wheatstone_cg --input_format ABC | tail')
Measure 2 - F#5
PULL:
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    F#5 --- --- --- ---
Measure 2 - G5
PUSH:
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    --- --- G5  --- ---
--- --- --- --- ---    --- --- --- --- ---

```