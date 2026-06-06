import os
import time
from dotenv import load_dotenv
from google import genai
from termcolor import colored

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def send_with_retry(chat, user_input, max_retries=2):
    for attempt in range(max_retries):
        try:
            response = chat.send_message(user_input)
            return response
        except Exception as e:
            if "429" in str(e):
                if attempt < max_retries - 1:
                    wait = 60 * (attempt + 1)  # 60s, 120s
                    print(colored(f"\n[System]: Rate limit hit! Waiting {wait}s before retry... (attempt {attempt+1}/{max_retries})", "yellow"))
                    time.sleep(wait)
                    print(colored("System: Retrying now!", "green"))
                else:
                    print(colored("\n[System]: Still rate limited after retries.", "red"))
                    print(colored("[System]: You may have hit your daily limit (20 req/day on free tier).", "red"))
                    print(colored("[System]: Resets at midnight Pacific Time. Try again tomorrow!", "yellow"))
            else:
                raise
    return None

def start_chat():
    print(colored("--- Gemini Helper: Ready ---", "cyan", attrs=["bold"]))

    chat = client.chats.create(model="gemini-2.5-flash")

    while True:
        user_input = input(colored("\nYou: ", "green")).strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            break

        response = send_with_retry(chat, user_input)
        if response:
            print(f"\n{colored('AI Bot:', 'magenta', attrs=['bold'])} {response.text}")

if __name__ == "__main__":
    start_chat()