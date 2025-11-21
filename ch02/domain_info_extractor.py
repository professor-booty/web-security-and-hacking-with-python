import requests
import whois
import dns.resolver
import argparse

def is_registered(domain_name):
    """A function that returns a boolean indicating wheather a 'domain_name' is registered """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

def get_discovered_subdomains(domain, subdomain_list, timeout=2):
    # list of discovered subdomains
    discovered_subdomains = []
    for subdomain in subdomain_list:
        # construct the url
        url = f"http://{subdomain}.{domain}"
        try:
            # if this raises an error, that means the subdomain does not exist
            requests.get(url, timeout=timeout)
        except requests.ConnectionError:
            # if the subdomain doesnt exist, just skip and do 6 7
            pass
        else:
            print("[+] Discovered Subdomain:", url)
            # append the discovered subdomain to our list
            discovered_subdomains.append(url)
    return discovered_subdomains

def resolve_dns_records(target_domain):
    """ A function thatresolves DNS records for a 'target_domain' """
    # List of record types
    record_types = ["A","AAAA","CNAME","MX","NS","SOA","TXT"]
    # create resolver
    resolver = dns.resolver.Resolver()
    for record_type in record_types:
        # perform dns lookups for domain and type
        try:
            answers = resolver.resolve(target_domain, record_type)
        except dns.resolver.NoAnswer:
            continue

        # print record found
        print(f"DNS records for {target_domain} ({record_type})")
        for rdata in answers:
            print(f"[*] {rdata}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Domain Name Info Extractor (WHOIS and Subdomain Scanner")
    parser.add_argument("domain", help="Domain to scan without http(s)")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="The timeout in seconds for prompting the connection. Default is 2")
    parser.add_argument("-s", "--subdomains", default="subdomains.txt", help="The file that contains a list of subdomains to scan. Default is subdomains.txt")
    parser.add_argument("-o", "--output", help="The output file of the discovered subdomains. Default is {domain}_subdomains.log")

    # parse the command line arguments
    args = parser.parse_args()
    if is_registered(args.domain):
        whois_info = whois.whois(args.domain)
        # registrar
        print("Domain Registrar:", whois_info.registrar )
        # WHOIS server
        print("WHOIS Server:", whois_info.whois_server)
        # creation date
        print("Domain Creation Date:", whois_info.creation_date)
        # expiration date
        print("Domain Expiration Date:", whois_info.expiration_date)
        # all other info
        print(whois_info)

    print("="*30, "DNS Records", "="*30)
    # read all subdomains
    with open(args.subdomains) as file:
        # read all content
        content = file.read()
        # split by new lines
        subdomains = content.splitlines()
    discovered_subdomains = get_discovered_subdomains(args.domain, subdomains)
    # make the discovered subdomains filename dependant on the domain
    discovered_subdomains_file = f"{args.domain.replace('.','_')}_subdomains.log"
    # save the discovered subdomains to a file
    with open(discovered_subdomains_file, "w") as f:
        for subdomain in discovered_subdomains:
            print(subdomain, file = f)
