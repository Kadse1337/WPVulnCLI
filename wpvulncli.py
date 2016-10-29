import argparse
import json
import sys
from colorama import init, Fore
import urllib.request as urllib

version = "1.0.0"


def main():
    init()

    parser = argparse.ArgumentParser()
    parser.add_argument("--wpversion", "-v", help="Find all exploits for a specific WP version")
    parser.add_argument("--plugin", "-p", help="Find all exploits for a specific WP plugin")
    parser.add_argument("--theme", "-t", help="Find all exploits for a specific WP theme")
    parser.add_argument("--info", help="Shows the version", action="store_true")

    args = parser.parse_args()

    if args.info:
        print(Fore.LIGHTWHITE_EX + "[*] WPVulnCLI v" + version)
        sys.exit(0)

    if args.wpversion is None and args.plugin is None and args.theme is None:
        print(Fore.LIGHTRED_EX + "[*] No arguments found! Use wpvulncli.py --help")
        sys.exit(0)

    if args.wpversion is not None:
        printvulns("https://wpvulndb.com/api/v2/wordpresses/" + args.wpversion.replace(".", ""))

    if args.plugin is not None:
        printvulns("https://wpvulndb.com/api/v2/plugins/" + args.plugin)

    if args.theme is not None:
        printvulns("https://wpvulndb.com/api/v2/themes/" + args.theme)


def printvulns(url):
    headers = {'User-Agent': 'WPVulnCLI-Client'}
    request = urllib.Request(url, headers=headers)
    response = json.loads(urllib.urlopen(request).read().decode('utf-8'))
    print(Fore.LIGHTGREEN_EX + "[*] ID | Type | Title | Fixed in | Link")
    for vuln in response[next(iter(response.keys()))]["vulnerabilities"]:
        if vuln.get("fixed_in") is None:
            fixed = "Unfixed / Unknown"
            color = Fore.LIGHTGREEN_EX
        else:
            fixed = vuln.get("fixed_in")
            color = Fore.LIGHTRED_EX

        print(color + str(vuln.get("id")) + " | " + vuln.get("vuln_type") + " | " + vuln.get(
            "title") + " | " + fixed + " | https://wpvulndb.com/vulnerabilities/" + str(vuln.get("id")))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
