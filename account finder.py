import random
import requests
import time
from datetime import datetime

# Doom was here
# https://github.com/Codopalm

def calculate_green(user_id):
    green_value = 128 + ((user_id - 10000) / (500000 - 10000)) * (255 - 128)
    green_value = max(128, min(255, green_value))
    return int(green_value)

def has_20_or_more_hats(user_id):
    try:
        inventory_url = f"https://catalog.roblox.com/v1/users/{user_id}/assets/collectibles?assetType=hat&limit=50"
        inventory_response = requests.get(inventory_url)

        if inventory_response.status_code == 200:
            inventory_data = inventory_response.json()
            hats = inventory_data.get("data", [])

            if len(hats) >= 20:
                return True
            else:
                return False
        else:
            print(f"Failed to fetch inventory for user {user_id}. Status code: {inventory_response.status_code}")
            return False
    except Exception as e:
        print(f"Error fetching inventory for user {user_id}: {e}")
        return False

def get_user_info(user_id):
    try:
        user_info_url = f"https://users.roblox.com/v1/users/{user_id}"
        avatar_url_api = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=352x352&format=Png&isCircular=false"
        headshot_url_api = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=352x352&format=Png&isCircular=false"

        user_info_response = requests.get(user_info_url)
        avatar_url_response = requests.get(avatar_url_api)
        headshot_url_response = requests.get(headshot_url_api)

        if user_info_response.status_code == 200 and avatar_url_response.status_code == 200 and headshot_url_response.status_code == 200:
            user_data = user_info_response.json()
            avatar_data = avatar_url_response.json()
            headshot_data = headshot_url_response.json()

            username = user_data.get("name")
            avatar_url = avatar_data["data"][0]["imageUrl"]
            headshot_url = headshot_data["data"][0]["imageUrl"]

            return username, avatar_url, headshot_url
        else:
            print(f"Failed to fetch user info. Status code: {user_info_response.status_code}, {avatar_url_response.status_code}, {headshot_url_response.status_code}")
            return None, None, None
    except Exception as e:
        print(f"Error retrieving user info: {e}")
        return None, None, None

def send_random_user_id(webhook_url):
    user_id = random.randint(10000, 500000)
    has_20_hats = has_20_or_more_hats(user_id)
    username, avatar_url, headshot_url = get_user_info(user_id)
    if username is None or avatar_url is None or headshot_url is None:
        return

    roblox_profile_url = f"https://www.roblox.com/users/{user_id}/profile"
    embed_color = calculate_green(user_id) if has_20_hats else 16711680

    payload = {
        "content": None,
        "embeds": [
            {
                "title": "Account Found!",
                "url": roblox_profile_url,
                "color": embed_color,
                "fields": [
                    {
                        "name": "username",
                        "value": username,
                        "inline": True
                    },
                    {
                        "name": "id",
                        "value": str(user_id),
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "cryptozoo.pg",
                    "icon_url": "https://cdn.discordapp.com/icons/1133441692196950101/a_bd28b1fbfa19500af04bc96a62e9a344.gif?size=1024"
                },
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "thumbnail": {
                    "url": headshot_url
                },
                "image": {
                    "url": avatar_url
                }
            }
        ],
        "username": "cryptozoo pg bot",
        "avatar_url": "https://cdn.discordapp.com/icons/1133441692196950101/a_bd28b1fbfa19500af04bc96a62e9a344.gif?size=1024",
        "attachments": []
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 204:
        print(f"Successfully sent: {roblox_profile_url}")
    else:
        print(f"Failed to send: {roblox_profile_url}, Status code: {response.status_code}")

def main():
    webhook_url = input("Please enter your Discord webhook URL: ")

    try:
        delay = float(input("Enter the delay between messages in seconds: "))
    except ValueError:
        print("Invalid input. Using a default delay of 2 seconds.")
        delay = 2

    try:
        while True:
            send_random_user_id(webhook_url)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()
