import requests
import subprocess
from decouple import config

# Subfinder scan.
# Check HTTP is live and delete duplicate and non live http.
# Nuclei scan with threat
# Save result.

class Tool:
    # Function: Subfinder
    def subfinder(self):
        command = subprocess.Popen(f"subfinder -silent -recursive -nW -d siberaman.id",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = command.communicate()[0].decode('UTF-8')
        return output

    # Function: HTTPx
    def httpx(self):
        command = subprocess.Popen(f"httpx -silent -l results/domains.txt",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = command.communicate()[0].decode('UTF-8')
        return output

    # Function: Nuclei
    def nuclei(self):
        command = subprocess.Popen(f"nuclei -l results/lives.txt -silent -nc -nts -severity critical,medium,high,low -o results/vulnerability.txt",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        return command

    # Function: Telegram Notification
    def notification(self, textMessage = ""):
        return requests.post('https://api.telegram.org/bot{token}/sendMessage'.format(token=config("TELEGRAM_TOKEN_BOT")), json={"chat_id": config("TELEGRAM_CHAT_ID"), "text": textMessage})

    def writeFile(self, nameFile, content):
        f = open(nameFile, "w")
        f.write(content)
        f.close()
        return f

def main():
    tools = Tool()
    scanSubdomain = tools.subfinder()
    tools.writeFile('results/domains.txt', scanSubdomain)
    scanSubdomainLive = tools.httpx()
    tools.writeFile('results/lives.txt', scanSubdomainLive)
    tools.notification("List subdomain found:\n" + scanSubdomain)
    tools.notification("List subdomain live found:\n" + scanSubdomainLive)
    scanVulnerability = tools.nuclei()
    while scanVulnerability.poll() is None:
        line = scanVulnerability.stdout.readline()
        tools.notification(line)
    
    if scanSubdomainLive is None:
        sendNotification = tools.notification("Not found vuln!")

if __name__ == "__main__":
    main()
