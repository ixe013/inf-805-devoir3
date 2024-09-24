import fileinput
import re
import sys

protonmail = re.compile("mail(sec){0,1}\.protonmail\.ch\.$")
spf1 = re.compile("^v=spf1.+")

import dns.resolver

def resolve(domain, record):
    values = set()
    try:
        answers = dns.resolver.resolve(domain, record)
        for rdata in answers:
            values.add(rdata.to_text().strip('"'))

        return list(values)
    except:
        return []


def find_regex_value_in_records(regex, records):
    for record in records:
        if regex.search(record):
            return f"✅ {str(record)}"
    else:
        return None


def is_proton_mail(mx):
    return find_regex_value_in_records(protonmail, mx)

        
def has_spf1(txt):
    return find_regex_value_in_records(spf1, txt)

def verify_domain(domain):
    print(f"MX:  {is_proton_mail(resolve(domain, 'MX'))}")
    print(f"TXT: {has_spf1(resolve(domain, 'TXT'))}")

def main(argv):
    if len(argv) > 1:
        for domain in argv[1:]:
            verify_domain(domain)
    else:
        for domain in fileinput.input():
            verify_domain(domain.strip())


if __name__ == '__main__':
    main(sys.argv)
