# Changelog

## v2.2.0 (2025-06-26)

#### New Features

* add excludes option to cli and `scan_dir()`

## v2.1.0 (2025-04-09)

#### New Features

* implement local scanner

#### Refactorings

* add exports to import file
* use argshell package arguement parser instead of built in
* remove progress bar description
* change various symbol names

#### Docs

* update readme

## v2.0.1 (2024-02-18)

#### Refactorings

* improve type annotation coverage
* update printbuddies usage

## v2.0.0 (2024-01-12)

#### New Features

* BREAKING
* add `Package.from_distribution_name()` method
* add option to suppress scan progress printout

#### Fixes

* fix scan_dir output formatting
* fix showing builtins when using --files without --builtins

#### Performance improvements

* condense terminal printout and add a progress bar
* rewrite core so that it's better organized, faster, and more accurate

#### Refactorings

* change `Package.format_requirement()` to `Package.get_formatted_requirement()`
* change progbar display width to 0.3
* edit printout to include package versions event when including builtin packages
* rename `Project.unique_packages` to `Project.packages`

#### Docs

* edit typo in readme
* change type annotation for `Package.distribution_name` and `Package.version`
* update readme
* add function and class docstrings

## v1.6.2 (2023-07-02)

#### Performance improvements

* add exception hadling and reporting to `whouses` script

## v1.6.1 (2023-06-10)

#### Fixes

* cli no longer lists the package being scanned in the results

#### Performance improvements

* remove redundant list sort

## v1.6.0 (2023-06-10)

#### New Features

* replace package names with pip name when they don't match when generating requirements

#### Fixes

* fix not getting package versions

#### Performance improvements

* use ast module to extract packages

#### Refactorings

* add default value to ignore arg in find()
* replace pathlib with pathier
* rename top_dir to root
* remove recursive option from get_packages_from_source

#### Docs

* update help message
* improve docstrings

#### Others

* add missing version prefix
* remove invalid assertion

## v1.5.1 (2023-05-02)

#### Fixes

* fix crash when trying to import something that isn't a module

## v1.5.0 (2023-05-01)

#### New Features

* add recursive option to get_packages_from_source

#### Others

* build v1.5.0
* update changelog

## v1.4.0 (2023-05-01)

#### New Features

* add get_packages_from_source()

#### Refactorings

* remove pathcrawler usage
* refactor scan to use get_packages_from_source

#### Others

* build v1.4.0
* update changelog

## v1.3.1 (2023-04-28)

#### Fixes

* update printbuddies.ProgBar usage to new version

#### Others

* build v1.3.1
* update changelog

## v1.3.0 (2023-04-15)

#### New Features

* add whosuses to scripts table

#### Refactorings

* move bulk of work into seperate function

#### Others

* build v1.3.0
* update changelog

## v1.2.0 (2023-04-12)

#### New Features

* add switch to add package versions with chosen relation when generating requirements.txt

#### Others

* build v1.2.0
* update changelog

## v1.1.3 (2023-03-22)

#### Others

* build v1.1.3

## v1.1.2 (2023-02-04)

#### Fixes

* (cli): change == to ~= when generating requirements.txt

#### Others

* update to build v1.1.2
* update changelog

## v1.1.1 (2023-01-25)

#### Fixes

* pyproject.toml indentation issue

#### Others

* build 1.1.1 dist files
* (cli): change abbreviated switches to single letters
