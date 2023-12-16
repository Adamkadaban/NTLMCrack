# NTLMCrack
Use ntlm.pw to automatically convert hash dumps to credentials


## Usage

```
usage: main.py [-h] [-s] [-n N] file_path

Use ntlm.pw to automatically convert hash dumps to credentials

positional arguments:
  file_path             Path to the file containing hash dumps

options:
  -h, --help            show this help message and exit
  -s, --separate-files  Output credentials in separate files
  -n N                  Limit to the first n lines of the file
```

## Examples

Output to one file:
```bash
python3 main.py example_hashes/hashes -n 100
```

Output to separate files:
```bash
python3 main.py example_hashes/hashes -n 100 -s
```

