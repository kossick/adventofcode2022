# Advent of Code entries 2022

My entries into the 2022 [advent of code](https://adventofcode.com/2022) challenge. The code is written in python 3.11 with the intent of relying on the standard library as much as possible. In addition, I am aiming to follow `PEP 8` via `Flake8` linting and relying on considerable type hinting. 

In addition to the code for the daily challenges there exists two additional files. The first is a shell script, `build_directories.sh`, for building a directory for each day; these directories contain a file for test data, one for the input data for the day (not copied here), and one for the python code. The script is also responsible for populating the built python file with boilerplate code for reading in either test or input data, as provided in the file `python_boilerplate.py`. 

None of the code here is of particularly good quality, but I am treating this as good practise nonetheless. If you're insane enough to want to run this code, it _should_ be capable of running with python 3.10 (I think the only potential issue for earlier versions is the use of `X | None` instead of `Optional[X]` when type-hinting).