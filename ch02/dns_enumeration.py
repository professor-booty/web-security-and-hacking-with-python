import dns.resolver

# set target domain and dns record types
target_domain = "thepythoncode.com"
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
