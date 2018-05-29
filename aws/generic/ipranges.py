import requests


def get_awsipranges(region, service):
    r = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
    if r.status_code != 200:
        raise Exception(r.status_code)
    return [ip["ip_prefix"] for ip in r.json()['prefixes'] if ip["region"] == region and ip["service"] == service]


if __name__ == '__main__':
    print get_awsipranges("eu-west-2", "EC2")
