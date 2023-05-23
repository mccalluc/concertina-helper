# Command line examples

(Note: Remove the wrapping `shell('...')` in the examples to use in BASH or another shell.)

<details>

The command line examples are wrapped with a python helper function,
so that they can be tested the same way as other python code.

```
>>> import subprocess
>>> def shell(command):
...     result = subprocess.run(
...         command, shell=True, check=True, 
...         capture_output=True, text=True)
...     print(result.stdout.strip())

```

</details>

`concertina-helper` is a command line tool to help find good fingerings.
Only two arguments are required: An input file, and a layout:

```
>>> shell('cat tests/g-major.txt | tail')
G4
A4
B4
C5
D5
E5
F#5
G5

>>> shell('concertina-helper tests/g-major.txt --layout_name 30_wheatstone_cg | tail')
Measure 1 - F#5
PULL:
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    F#5 --- --- --- ---
Measure 1 - G5
PUSH:
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    --- --- G5  --- ---
--- --- --- --- ---    --- --- --- --- ---

```

Files in ABC notation are also supported. (The program looks at the first line to infer format.)

```
>>> shell('cat tests/g-major.abc')
X: 1
T: G major scale
M: 4/4
L: 1/4
K: Gmaj
GABc|defg||

```

If you want a layout that is not provided,
you can specify a whole layout manually in a format like this:

```
>>> shell('cat concertina_helper/layouts/20_cg.yaml')
push:
  left:
    - C3 G3 C4  E4 G4
    - G3 D4 G4  B4 D5
  right:
    - C5  E5  G5  C6  E6
    - G5  B5  D6  G6  B6
pull:
  left:
    - G3 B3  D4  F4 A4
    - D4 F#4 A4  C5 E5
  right:
    - B4  D5  F5  A5 B5
    - F#5 A5  C6  E6 F#6

```

There is also a `--layout_transpose` flag:
We can transpose up 7 semitones to go from CG layout to a GD.
Putting these options together:

```
>>> shell('concertina-helper tests/g-major.txt --layout_path concertina_helper/layouts/30_wheatstone_cg.yaml --layout_transpose 7 | tail')
Measure 1 - F#5
PUSH:
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    --- --- --- --- ---
--- --- --- F#5 ---    --- --- --- --- ---
Measure 1 - G5
PUSH:
--- --- --- --- ---    --- --- --- --- ---
--- --- --- --- ---    G5  --- --- --- ---
--- --- --- --- ---    --- --- --- --- ---

```

Other, more compact output formats are also available:

```
>>> shell('concertina-helper tests/g-major.txt --layout_name 30_wheatstone_cg --output_format ASCII | tail')
Measure 1 - F#5
PULL:
.....   .....
.....   .....
.....   @....
Measure 1 - G5
PUSH:
.....   .....
.....   ..@..
.....   .....

```

```
>>> shell('concertina-helper tests/g-major.txt --layout_name 30_wheatstone_cg --output_format UNICODE | tail')
Measure 1 - F#5
<- PULL ->:
○ ○ ○ ○ ○    ○ ○ ○ ○ ○
○ ○ ○ ○ ○    ○ ○ ○ ○ ○
○ ○ ○ ○ ○    ● ○ ○ ○ ○
Measure 1 - G5
-> PUSH <-:
○ ○ ○ ○ ○    ○ ○ ○ ○ ○
○ ○ ○ ○ ○    ○ ○ ● ○ ○
○ ○ ○ ○ ○    ○ ○ ○ ○ ○

```

Finally, different fingering strategies can be explored.
Note that if different fingering have the same cost,
different results may be retured on successive runs.
Adding more cost parameters tends to produce more stable results.

```
>>> shell('concertina-helper tests/g-major.abc --layout_name 30_wheatstone_cg --output_format COMPACT --bellows_change_cost 10')
. . . ➊ .   . ➑ . . .
. . . . .   ➌ ➎ . . .
. . ➋ ➍ ➏   ➐ . . . .

>>> shell('concertina-helper tests/g-major.abc --layout_name 30_wheatstone_cg --output_format COMPACT --pull_at_start_of_measure_cost 5 --finger_in_same_column_cost 10 --outer_fingers_cost 5')
. . . ➊ .   . . . . .
. . . . .   ➃ ➅ ➇ . .
. . ➋ ➂ ➄   ➐ . . . .

```

If you need more flexibility than this,
check out the [API documentation](https://mccalluc.github.io/concertina-helper),
or contribute a PR.