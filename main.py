
import socket
import argparse
import exrex
import whois


def is_dns_active(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


def is_domain_used(domain_name):
    try:
        whois.whois(domain_name)
        return True
    except Exception:
        return False


def test_domain(domain):
    oks = open("domains_ok.txt", "r").read().split("\n")
    kos = open("domains_ko.txt", "r").read().split("\n")
    if domain in oks:
        print(domain, "ok")
        return
    if domain in kos:
        print(domain, "ko")
        return

    result_dns = is_dns_active(domain)
    if result_dns:
        print(domain, "ko dns")
        open("domains_ko.txt", "a").write(domain + "\n")
        return

    result_whois = is_domain_used(domain)
    if result_whois:
        print(domain, "ko whois")
        open("domains_ko.txt", "a").write(domain + "\n")
        return

    print(domain, "ok")
    open("domains_ok.txt", "a").write(domain + "\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='Search for domain names and save them to .txt',
        epilog='Text at the bottom of help')

    parser.add_argument('domain_regex')
    parser.add_argument('-r', '--random', action='store_true')
    
    args = parser.parse_args()

    if args.random:
        while True:
            test_domain(exrex.getone(args.domain_regex))
    else:
        for domain in exrex.generate(args.domain_regex):
            test_domain(domain)
        print("---over---")
