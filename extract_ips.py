import re

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

ips = re.findall(pattern, text)

unique_ips = set(ips)

with open("hosts.txt", "w") as f:
    for ip in unique_ips:
        f.write(ip + "\n")

print("IP addresses extracted and written to hosts.txt")