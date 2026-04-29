
import socket
import argparse
import exrex
import whois


ko_filename = "domains_ko.txt"
ok_filename = "domains_ok.txt"


def is_dns_active(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except (socket.gaierror, socket.herror, OSError):
        return False
    except Exception as e:
        return False


def is_domain_used(domain_name):
    try:
        whois.whois(domain_name)
        return True
    except Exception:
        return False


def print_result(domain, result=True, reason='', verbose=False):
    str = domain
    if verbose:
        str += f" {'O' if result else 'X'}"
    if reason and verbose:
        str += f" {reason}"
    if result or verbose:
        print(str)


def test_domain(domain, verbose):
    oks = open(ok_filename, "r").read().split("\n")
    kos = open(ko_filename, "r").read().split("\n")
    if domain in oks:
        print_result(domain, result=True, reason='cache', verbose=verbose)
        return
    if domain in kos:
        print_result(domain, result=False, reason='cache', verbose=verbose)
        return

    result_dns = is_dns_active(domain)
    if result_dns:
        print_result(domain, result=False, reason='dns', verbose=verbose)
        open(ko_filename, "a+").write(domain + "\n")
        return

    result_whois = is_domain_used(domain)
    if result_whois:
        print_result(domain, result=False, reason='whois', verbose=verbose)
        open(ko_filename, "a+").write(domain + "\n")
        return

    print_result(domain, result=True, reason='', verbose=verbose)
    open(ok_filename, "a+").write(domain + "\n")


if __name__ == "__main__":
    # ensure files exist
    open(ko_filename, "a+").write("")
    open(ok_filename, "a+").write("")

    parser = argparse.ArgumentParser(
        prog='domain_name_finder',
        description='Find domain names using regex'
    )

    parser.add_argument('domain_regex')
    parser.add_argument('-r', '--random', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    if args.random:
        while True:
            test_domain(exrex.getone(args.domain_regex), args.verbose)
    else:
        for domain in exrex.generate(args.domain_regex):
            test_domain(domain, args.verbose)
