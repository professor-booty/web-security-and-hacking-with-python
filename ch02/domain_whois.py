import whois
from domain_validator import is_registered

domain_name = "google.com"

if is_registered(domain_name):
    whois_info = whois.whois(domain_name)
    # registrar
    print("Domain Registrar:", whois_info.registrar)
    # WHOIS server
    print("WHOIS Server:", whois_info.whois_server)
    # creation date
    print("Creation Date:", whois_info.creation_date)
    # expiration date
    print("Expiration Date:", whois_info.expiration_date)
    # all other info
    print(whois_info)
