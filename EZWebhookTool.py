import os
import time
import base64
import requests
import threading
import webbrowser
from tkinter import filedialog as fd


class Colors:
    BLACK = "\033[1;30m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    PURPLE = "\033[1;35m"
    CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"


SOCIAL_LINKS = {
    "discord": "discord.gg/fKyEAuJ3Fg",
    "GitHub" : "https://github.com/Asticsss",
}






LOGO = """
                                            ██╗      ██╗    ███████╗███████╗
                                            ██║     ██╔╝    ██╔════╝╚══███╔╝
                                            ██║    ██╔╝     █████╗    ███╔╝ 
                                            ╚═╝    ╚██╗     ██╔══╝   ███╔╝  
                                            ██╗     ╚██╗    ███████╗███████╗
                                            ╚═╝      ╚═╝    ╚══════╝╚══════╝
"""

for platform, link in SOCIAL_LINKS.items():
    LOGO += f"      > [{platform.capitalize()}]: {link}\n"


def display_logo():
    print(f"{Colors.CYAN}{LOGO}{Colors.WHITE}")

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def pause_console(text: str = ""):
    if text:
        print(text)
    os.system('read -n 1 -s -r -p ""' if os.name != 'nt' else 'pause >nul')

def menu_options():
    options = """
    [1] Send Message
    [2] Delete Webhook
    [3] Rename Webhook
    [4] Spam Webhook
    [5] Webhook Information
    [6] Log Out
    [7] Change Profile Picture
    """
    print(options)


def change_profile_picture(webhook_url):
    input(f"{Colors.YELLOW}[?] Press Enter to select a file or skip this to enter the path/URL{Colors.WHITE}")
    image_path = fd.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])

    if not image_path:
        clear_screen()
        image_path = input(f"{Colors.YELLOW}[?] Path/URL to image: {Colors.WHITE}")

    try:
        if image_path.startswith(('http://', 'https://')):
            response = requests.get(image_path)
            response.raise_for_status()
            encoded_image = base64.b64encode(response.content).decode('utf-8')
        else:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        response = requests.patch(webhook_url, json={"avatar": f"data:image/jpeg;base64,{encoded_image}"})
        response.raise_for_status()
        print(f"{Colors.GREEN}[+] Profile picture changed successfully.{Colors.WHITE}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.WHITE}")

def delete_webhook(webhook_url):
    try:
        response = requests.delete(webhook_url)
        response.raise_for_status()
        print(f"{Colors.GREEN}[+] Webhook deleted successfully.{Colors.WHITE}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.WHITE}")

def send_message(webhook_url):
    message = input(f"{Colors.YELLOW}[?] Message: {Colors.WHITE}")
    try:
        response = requests.post(webhook_url, json={"content": message})
        response.raise_for_status()
        print(f"{Colors.GREEN}[+] Message sent successfully.{Colors.WHITE}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.WHITE}")

def rename_webhook(webhook_url):
    new_name = input(f"{Colors.YELLOW}[?] New webhook name: {Colors.WHITE}")
    try:
        response = requests.patch(webhook_url, json={"name": new_name})
        response.raise_for_status()
        print(f"{Colors.GREEN}[+] Webhook name changed successfully.{Colors.WHITE}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.WHITE}")

def get_webhook_info(webhook_url):
    try:
        response = requests.get(webhook_url)
        response.raise_for_status()
        webhook_data = response.json()
        print(f"{Colors.GREEN}[+] Webhook Information:{Colors.WHITE}")
        print(f" Name: {webhook_data['name']}")
        print(f" Channel ID: {webhook_data['channel_id']}")
        print(f" Guild ID: {webhook_data['guild_id']}")
        print(f" Application ID: {webhook_data['application_id']}")
        print(f" Token: {webhook_data['token']}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.WHITE}")

def spam_webhook(webhook_url, message, duration, delay):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            response = requests.post(webhook_url, json={"content": message})
            response.raise_for_status()
            print(f"{Colors.GREEN}[+] Message sent successfully.{Colors.WHITE}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {str(e)}{Colors.WHITE}")
        time.sleep(delay)

def log_out(webhook_url):
    delete_webhook(webhook_url)

def open_source_code():
    print(f"{Colors.YELLOW}[?] Opening source code...{Colors.WHITE}")
    webbrowser.open('https://github.com')


def main_menu():
    clear_screen()
    display_logo()
    menu_options()

def main():
    main_menu()
    while True:
        try:
            user_choice = int(input(f"{Colors.YELLOW}[?] Enter your choice: {Colors.WHITE}"))
            webhook_url = input(f"{Colors.YELLOW}[?] Webhook URL: {Colors.WHITE}")

            if user_choice == 1:
                send_message(webhook_url)
            elif user_choice == 2:
                delete_webhook(webhook_url)
            elif user_choice == 3:
                rename_webhook(webhook_url)
            elif user_choice == 4:
                message = input(f"{Colors.YELLOW}[?] Message: {Colors.WHITE}")
                duration = int(input(f"{Colors.YELLOW}[?] Duration (in seconds): {Colors.WHITE}"))
                delay = int(input(f"{Colors.YELLOW}[?] Delay (in seconds): {Colors.WHITE}"))
                threading.Thread(target=spam_webhook, args=(webhook_url, message, duration, delay)).start()
            elif user_choice == 5:
                get_webhook_info(webhook_url)
            elif user_choice == 6:
                log_out(webhook_url)
            elif user_choice == 7:
                change_profile_picture(webhook_url)
            elif user_choice == 0:
                open_source_code()
            else:
                print(f"{Colors.RED}[!] Invalid choice. Please try again.{Colors.WHITE}")
        except ValueError:
            print(f"{Colors.RED}[!] Please enter a valid number.{Colors.WHITE}")
        except Exception as e:
            print(f"{Colors.RED}[!] Unexpected error: {str(e)}{Colors.WHITE}")

if __name__ == "__main__":
    main()
