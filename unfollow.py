import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

def get_all_pages(url):
    results = []
    while url:
        response = requests.get(url, auth=(USERNAME, TOKEN))
        response.raise_for_status()
        results.extend(response.json())
        url = response.links.get('next', {}).get('url')
    return results

def get_following():
    url = f"https://api.github.com/users/{USERNAME}/following"
    data = get_all_pages(url)
    return {user['login'] for user in data}

def get_followers():
    url = f"https://api.github.com/users/{USERNAME}/followers"
    data = get_all_pages(url)
    return {user['login'] for user in data}

def main():
    print("Fetching followers and following lists...")
    following = get_following()
    followers = get_followers()

    not_following_back = following - followers

    print(f"\nYou are following {len(following)} users.")
    print(f"You have {len(followers)} followers.")
    print(f"\nUsers not following you back ({len(not_following_back)}):")
    for user in sorted(not_following_back):
        print(f"- {user}")

if __name__ == "__main__":
    main()
