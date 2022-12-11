# Advent of Code entries 2022

My entries into the 2022 [advent of code](https://adventofcode.com/2022) challenge. The code is written in python 3.11 with the intent of relying on the standard library as much as possible. In addition, I am aiming to follow `PEP 8` via `Flake8` linting and relying on considerable type hinting. 

In addition to the code for the daily challenges there exists two additional files. The first is a shell script, `build_directories.sh`, for building a directory for each day; these directories contain a file for test data, one for the input data for the day (not copied here), and one for the python code. The script is also responsible for populating the built python file with boilerplate code for reading in either test or input data, as provided in the file `python_boilerplate.py`. 

None of the code here is of particularly good quality, but I am treating this as good practise nonetheless. (This is especially true early on given that on day 10, when I started this repo, I accidentally _deleted every answer up to this point_ so this code is replications that also work.) If you're insane enough to want to run this code, it _should_ be capable of running with python 3.10 (I think the only potential issue for earlier versions is the use of `X | None` instead of `Optional[X]` when type-hinting).

Direct links to code for each day: 

+ [Day 1](https://github.com/kossick/adventofcode2022/blob/main/day_1/day_1.py)
+ [Day 2](https://github.com/kossick/adventofcode2022/blob/main/day_2/day_2.py)
+ [Day 3](https://github.com/kossick/adventofcode2022/blob/main/day_3/day_3.py)
+ [Day 4](https://github.com/kossick/adventofcode2022/blob/main/day_4/day_4.py)
+ Day 5
+ Day 6
+ Day 7
+ Day 8
+ Day 9
+ Day 10
+ Day 11
+ Day 12
+ Day 13
+ Day 14
+ Day 15
+ Day 16
+ Day 17
+ Day 18
+ Day 19
+ Day 20
+ Day 21
+ Day 22
+ Day 23
+ Day 24
+ Day 25