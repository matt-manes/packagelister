# packagelister
Determine what packages and versions a project imports.  

Install with:
<pre>pip install packagelister</pre>


# Usage

---

Can be used either programmatically or with the included cli.  

### Programmatic:  

<pre>
>>> from pathlib import Path
>>> import json
>>> from packagelister import packagelister
>>>
>>> project = packagelister.scan_dir(Path.cwd())
Scanning C:/python/packagelister...
[______________________________________________]-100.00%
>>>
>>> print(*project.packages, sep="\n")
Package(name='argparse', distribution_name=None, version=None, builtin=True)
Package(name='ast', distribution_name=None, version=None, builtin=True)
Package(name='dataclasses', distribution_name=None, version=None, builtin=True)
Package(name='importlib', distribution_name=None, version=None, builtin=True)
Package(name='pathier', distribution_name='pathier', version='1.3.4', builtin=False)
Package(name='printbuddies', distribution_name='printbuddies', version='1.4.1', builtin=False)
Package(name='pytest', distribution_name='pytest', version='7.2.1', builtin=False)
Package(name='sys', distribution_name=None, version=None, builtin=True)
Package(name='typing_extensions', distribution_name='typing_extensions', version='4.7.1', builtin=False)
>>>
>>> print(project.get_formatted_requirements("=>"))
['pathier=>1.3.4', 'printbuddies=>1.4.1', 'pytest=>7.2.1', 'typing_extensions=>4.7.1']
>>>
>>> print(json.dumps(project.get_files_by_package(), indent=2))
{
  "argparse": [
    "C:/python/packagelister/src/packagelister/packagelister_cli.py",
    "C:/python/packagelister/src/packagelister/whouses.py"
  ],
  "ast": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ],
  "dataclasses": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ],
  "importlib": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ],
  "pathier": [
    "C:/python/packagelister/src/packagelister/packagelister.py",
    "C:/python/packagelister/src/packagelister/packagelister_cli.py",
    "C:/python/packagelister/src/packagelister/whouses.py",
    "C:/python/packagelister/tests/test_packagelister.py"
  ],
  "printbuddies": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ],
  "pytest": [
    "C:/python/packagelister/tests/test_packagelister.py"
  ],
  "sys": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ],
  "typing_extensions": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ]
}
>>>
>>> print(json.dumps({k:v for k,v in project.get_files_by_package().items() if k in project.packages.third_party.names}, indent=2))
{
  "pathier": [
    "C:/python/packagelister/src/packagelister/packagelister.py",
    "C:/python/packagelister/src/packagelister/packagelister_cli.py",
    "C:/python/packagelister/src/packagelister/whouses.py",
    "C:/python/packagelister/tests/test_packagelister.py"
  ],
  "printbuddies": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ],
  "pytest": [
    "C:/python/packagelister/tests/test_packagelister.py"
  ],
  "typing_extensions": [
    "C:/python/packagelister/src/packagelister/packagelister.py"
  ]
}
</pre>

### CLI:

There are two cli tools included in this package: `packagelister` and `whouses`.  

#### packagelister:

For the current directory, can be used to print the packages used by the current directory,
generate a `requirements.txt` file, and view which files import a package.

<pre>
C:/python/packagelister>packagelister -h
usage: packagelister [-h] [-f] [-g] [-v {==,<,<=,>,>=,~=}] [-b] [-d]

Scan the current directory for imported packages.

options:
  -h, --help            show this help message and exit
  -f, --files           Show which files imported each of the packages.
  -g, --generate_requirements
                        Generate a requirements.txt file in the current directory.
  -v {==,<,<=,>,>=,~=}, --versions {==,<,<=,>,>=,~=}
                        When generating a requirements.txt file, include the versions of the packages using this relation. (You may need to put quotes around some of the options.)
  -b, --builtins        Include built in standard library modules in terminal display.
  -d, --debug           Print the Package objects found during the scan.

C:/python/packagelister>packagelister
Scanning C:/python/packagelister...
[______________________________________________]-100.00%
Packages imported by packagelister:
pathier v1.3.4
printbuddies v1.4.1
pytest v7.2.1
typing_extensions v4.7.1

C:/python/packagelister>packagelister -b
Scanning C:/python/packagelister...
[______________________________________________]-100.00%
Packages imported by packagelister:
pathier v1.3.4
printbuddies v1.4.1
pytest v7.2.1
typing_extensions v4.7.1
argparse
ast
dataclasses
importlib
sys

C:/python/packagelister>packagelister -f
Scanning C:/python/packagelister...
[______________________________________________]-100.00%
Packages imported by packagelister:
pathier v1.3.4
printbuddies v1.4.1
pytest v7.2.1
typing_extensions v4.7.1
Files importing each package:
pathier:
  C:/python/packagelister/src/packagelister/packagelister.py
  C:/python/packagelister/src/packagelister/packagelister_cli.py
  C:/python/packagelister/src/packagelister/whouses.py
  C:/python/packagelister/tests/test_packagelister.py
printbuddies:
  C:/python/packagelister/src/packagelister/packagelister.py
pytest:
  C:/python/packagelister/tests/test_packagelister.py
typing_extensions:
  C:/python/packagelister/src/packagelister/packagelister.py

C:/python/packagelister>packagelister -g
Scanning C:/python/packagelister...
[______________________________________________]-100.00%
Packages imported by packagelister:
pathier v1.3.4
printbuddies v1.4.1
pytest v7.2.1
typing_extensions v4.7.1
Generating `requirements.txt`.

C:/python/packagelister>type requirements.txt
pathier>=1.3.4
printbuddies>=1.4.1
pytest>=7.2.1
</pre>

#### whouses:

Given a package name, scan the current directory for which sub-directories use that package.  
Useful for knowing which projects you'll need to update when upgrading an installed package.  

<pre>
C:/python>whouses -h
usage: whouses [-h] [-i [IGNORE ...]] package

Determine what sub-folders in the current directory use the specified package. Useful for knowing which projects need to be updated when upgrading an installed package.

positional arguments:
  package               Scan the current working directory for project folders that use this package.

options:
  -h, --help            show this help message and exit
  -i [IGNORE ...], --ignore [IGNORE ...]
                        Ignore these folders.

C:/python>whouses pathier -i envs pkgs
[______________________________________________]-100.00% Scanning scriptcheck...

The following folders have files that use pathier:
recon
jobglob
getToTheGig
databased
packagelister
gearshed
homecloud
hassle
hailmary
conflict
codecount
quickdrop
play
wellversed
pressured
gitbetter
crosseyed
dupechecker
seating
tomfoolery
notes
morbin
requester
gruel
loggi
scriptcheck
</pre>
