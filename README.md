###_//// RapidExtractor ReadMe \\\_###

## Overview

RapidExtractor is live data push-button forensic tool for on Windows target devices. It is designed to 
automatically collect specified artefacts using so-called extractor modules in an automated manner.

## Current Extractor Modules implemented

- bet_extractor
- browser_history_extractor
- dir_tree_extractor
- installed_programs_extractor
- prefetch_extractor
- process_extractor
- teamviewer_extractor


## Funcionality of Extractor modules
"BET": "Extracts logfiles from BET betting software for proving betting activities on target device.",
"Browser History": "Extracts browsing history from target device for Chrome, Edge and Firefox (if installed)."
"DirTree": "Shows the directory tree structure of the target device in a simple .txt format.",
"Installed Programs": "Shows the list of installed programs on target device.",
"Prefetch": "Extracts all prefetch files from target device from the following path: %SystemRoot%\\Windows\\Prefetch.",
"Processes": "Lists the currently running processes on the target device.",
"TeamViewer": "Extracts data from TeamViewer logs on target device.",


## Dependencies

- tqdm (Install using `pip install tqdm`)

## Installation

## Required File Structure on external drive

%DriveLetter%\
│
├── WPy64-31241\                 --> portable Python distribution
│ └── python-3.12.4.amd64\
│     └── python.exe             --> open properties and make sure it always starts with administrative privileges!
|     └── [...]
│
└── RapidExtractor\              --> RapidExtractor Tool
   ├── cases\
   ├── documents\
   ├── scripts\
   │    ├── main.py
   │    ├── dir_tree_extractor.py
   │    ├── prefetch_extractor.py
   │    ├── process_extractor.py
   │    ├── installed_programs_extractor.py
   │    ├── teamviewer_extractor.py
   │    ├── bet_extractor.py
   │    ├── browser_history_extractor.py
   │    ├── gui.py
   │    └── *.py (other scripts)
   └─── start_RapidExtractor.bat

Other portable Python than WinPython can be used. Just don't forget to adapt the path to the portable interpreter in the code. 
Also make sure, that the executable is always run with administrative privileges.


### Usage

1. Run `start_RapidExtractor.bat` from %DriveLetter%:\RapidExtractor
2. Insert casename and device name then select extractor modules and generate a batch file. 
3. Attach external drive to target device and start the generated batch-file to automatically collect evidence.
	
	--> standard path to batch file: %DriveLetter%:\RapidExtractor\cases\<case_name>_<YYYY-MM-DD>\<case_name>_<device_name>.bat
	
	
	
	
rapidextractor@proton.me