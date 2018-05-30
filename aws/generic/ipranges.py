import requests


def get_awsipranges(region=None, service=None):
    r = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
    if r.status_code != 200:
        raise Exception(r.status_code)
    return_list = [ip["ip_prefix"] for ip in r.json()['prefixes']]
    if region:
        return_list = [ip for ip in return_list if ip["region"] == region]
    if service:
        return_list = [ip for ip in return_list if ip["service"] == service]
    return return_list


if __name__ == '__main__':
    for ip in get_awsipranges():
        if ip.startswith('54.239.22'):
            print ip
