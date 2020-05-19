# bw_recipe_2016

Import the official ReCiPe characterization factors into Brightway.

## Installation

Use `pip` or `conda`.

## Parsing ReCiPe output files

This library goes as far as possible to avoid making any subjective judgments. It does, however, correct or amend data to provide consistent outputs across impact categories. For example, it fixes the following issues:

* Elementary flows are called different things in different impact categories
* Column labels are inconsistent across impact categories
* Given CAS numbers are not actually CAS numbers
* Ecotoxicity factors are repeated across three separate worksheets.

## Contributing

Details on how to contribute
