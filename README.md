# PDF Password Recovery Tool

A multi-threaded Python utility designed to recover lost or forgotten passwords from PDF files using dictionary-based and brute-force attack vectors.

## Features

* Dual Attack Modes: Supports both wordlist parsing (Dictionary Attack) and programmatic sequence generation (Brute-Force).
* Optimised Engine: Leverages pikepdf and QPDF bindings for fast file I/O operations.
* Parallel Processing: Utilises ThreadPoolExecutor to scale password verification across multiple CPU streams.
* Memory Management: Implements Python generators to process large keyspaces without memory overhead.
* Progress Tracking: Uses tqdm to provide real-time cracking statistics, processing speeds, and time estimates.

## Installation

Ensure Python 3.8 or higher is installed on your system.

git clone [https://github.com/username/pdf-recovery-tool.git](https://github.com/username/pdf-recovery-tool.git)
cd pdf-recovery-tool
pip install -r requirements.txt

## Usage

python pdf_cracker.py [options]

## Options
* -f,  --file FILE        Path to the target password-protected PDF file (Required)
* -w, --wordlist PATH    Path to the text file containing password candidates
* -b, --brute            Enable brute-force generation mode
* -c, --charset STR      Characters for brute force: l (lowercase), u (uppercase), d (digits), s (symbols) [Default: d]
* --min INT              Minimum password length for brute-force [Default: 1]
* --max INT              Maximum password length for brute-force [Default: 4]
* -t, --threads INT      Number of concurrent execution threads [Default: 4]

## Examples

### Dictionary Attack
python pdf_cracker.py -f confidential.pdf -w wordlist.txt -t 8

### Brute-Force Digits (Length 1-6)
python pdf_cracker.py -f confidential.pdf -b -c d --min 1 --max 6 -t 12

### Brute-Force Alpha-Numeric (Length 3-5)
python pdf_cracker.py -f confidential.pdf -b -c lud --min 3 --max 5 -t 16

## Architecture Notes

### Concurrency
Standard Python multi-threading is constrained by the Global Interpreter Lock (GIL). However, because pikepdf executes its heavy cryptographic operations within underlying C++ bindings, the GIL is released, allowing true parallel speed gains.
### Session Control
As soon as a thread identifies a valid decryption key, the script triggers an active worker shutdown sequence to stop pending processing tasks instantly and preserve system resources.

## Disclaimer 
This project is created for authorized security analysis, educational purposes, and personal data recovery. Unauthorized testing or accessing files without explicit ownership or permission is strictly prohibited.