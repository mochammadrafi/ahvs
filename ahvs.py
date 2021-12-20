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
        print("Subfinder")

    # Function: HTTPx
    def httpx(self):
        print("Httpx")

    # Function: Nuclei
    def nuclei(self):
        print("Nuclei")

    # Function: Telegram Notification
    def notification(self, textMessage = ""):
        return requests.post('https://api.telegram.org/bot{token}/sendMessage'.format(token=config("TELEGRAM_TOKEN_BOT")), json={"chat_id": config("TELEGRAM_CHAT_ID"), "text": textMessage});

def main():
    scanner = Tool()
    scanner.notification()

if __name__ == "__main__":
    main()
