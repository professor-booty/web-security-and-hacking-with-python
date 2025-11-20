import requests

# the domain to scan
domain = "google.com"

# read subdomain file
with open("subdomains.txt") as file:
    # read content
    content = file.read()

    # split by new lines
    subdomains = content.splitlines()

discovered_subdomains = []
for subdomain in subdomains:
    # construct the url
    url = f"http://{subdomain}.{domain}"
    try:
        requests.get(url, timeout=3)
    except requests.ConnectionError:
        # if the subdomain does not exist just pass 6 7
        #pass
        print("[X] No subdomain:", url)
    else:
        print("[+] Discovered subdomain:", url)
        # append to the discovered list
        discovered_subdomains.append(url)

with open("discovered_subdomains.log", "w") as f:
    for subdomain in discovered_subdomains:
        print(subdomain, file = f)
