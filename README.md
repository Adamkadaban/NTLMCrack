# NTLMCrack
Use [ntlm.pw](https://ntlm.pw) (by [@lkarlslund](https://github.com/lkarlslund/)) to automatically convert hash dumps to credentials

[![asciicast](https://asciinema.org/a/ZXIpK3LfqdH3LAuOxRKvYQfTw.svg)](https://asciinema.org/a/ZXIpK3LfqdH3LAuOxRKvYQfTw)

## Usage

```
usage: NTLMCrack.py [-h] [-s] [-n N] [-f] file_path

Use ntlm.pw to automatically convert hash dumps to credentials

positional arguments:
  file_path             Path to the file containing hash dumps

options:
  -h, --help            show this help message and exit
  -s, --separate-files  Output credentials in separate files
  -n N                  Limit to the first n lines of the file
  -f, --filter-not-found
                        Filter hashes that can't be cracked
```

## Examples

Output to one file:
```bash
./NTLMCrack.py example_hashes/hashes -n 100
```

Output to separate files:
```bash
./NTLMCrack.py example_hashes/hashes -n 100 -s
```

Filter hashes that can't be cracked:
```bash
./NTLMCrack.py example_hashes/hashes -f
```
