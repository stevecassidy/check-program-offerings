# Checking Degree Offerings

A utility script for checking whether a sequence of units 
can be completed for a degree. Useful in designing new 
degree programs and deciding when an how many offerings of units
are needed.  

## Usage

```bash
python3 curric.py mitai.json
```

output is CSV formatted text that could be saved as a CSV file.  The
degree units are shown first followed by study plans found for
students starting in S1 and then S2.

## Input

The input file defines the units in the degree, when they are offered
and their pre-requisites.  It is specific to MQ IT Masters degrees
which are four semesters long and have a two-unit project in the final
semester.  

```JSON
{
    "COMP6200": {"offered": ["S1", "S2"], "prereq": []}, 
    "COMP6350": {"offered": ["S2"], "prereq": []}, 
    "STAT6170": {"offered": ["S1", "S2"], "prereq": []}, 
    "COMP6010": {"offered": ["S1", "S2"], "prereq": []}, 
    "COMP6400": {"offered": ["S1"], "prereq": []}, 
    "COMP6410": {"offered": ["S2"], "prereq": ["COMP6200"]}, 
    "COMP6420": {"offered": ["S1", "S2"], "prereq": ["COMP6200"]}, 
    "BUSA6430": {"offered": ["S1"], "prereq": ["COMP6200"]}, 
    "COMP8221": {"offered": ["S1", "S2"], "prereq": ["COMP6420"]}, 
    "COMP8400": {"offered": ["S2"], "prereq": ["COMP6400"]}, 
    "COMP8410": {"offered": ["S2"], "prereq": ["COMP6400"]}, 
    "COMP8420": {"offered": ["S1", "S2"], "prereq": ["COMP6420"]}, 
    "COMP8430": {"offered": ["S2"], "prereq": ["COMP6420"]}, 
    "COMP8440": {"offered": ["S1"], "prereq": ["COMP6200"]}
}```
