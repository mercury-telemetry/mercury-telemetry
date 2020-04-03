#!/usr/bin/env python3
import sys


def check(file):
    print(f"Check {file.name}")
    dic = {}
    for line in file.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if "=" not in line:
            continue
        comp = line.split("=")
        dic[comp[0]] = comp[1]

    for key in ["sync.url", "registration.url", "db.user", "db.password", "db.url"]:
        if not assert_key(dic, key):
            print(f"{key} is not set in {file.name}", file=sys.stderr)
            exit(1)


def assert_key(dic, key):
    if key not in dic:
        return False
    if not dic[key].strip():
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(1)
    with open(sys.argv[1]) as f:
        check(f)
