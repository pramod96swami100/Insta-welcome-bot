from instagrapi import Client
from flask import Flask
from threading import Thread
import time
import os

# =========================
# FLASK SERVER FOR RENDER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Instagram Multi GC Welcome Bot Running ✅"

# =========================
# INSTAGRAM LOGIN
# =========================
cl = Client()

sessionid = os.getenv("SESSION_ID")

cl.login_by_sessionid(sessionid)

print("✅ Instagram Login Successful!")

# =========================
# MULTIPLE GROUP IDS
# =========================
TARGET_GROUP_IDS = [
    "1384445266434510",
    "9853140578080649",
    "1879481356017940"
]

# =========================
# WELCOME MESSAGE
# =========================
def get_stylish_welcome(name):
    message = f"""
╔═══════════════╗
║ ✨ WELCOME ✨ ║
╚═══════════════╝

🔥 Hey {name}! 🔥
🥳 Group me welcome!
✨ Happy Chatting! ✨
"""
    return message.strip()

# =========================
# BOT LOGIC
# =========================
def run_welcome_bot():

    print("🤖 Multi GC Welcome Bot Started")

    known_users = {}

    while True:

        try:

            for group_id in TARGET_GROUP_IDS:

                # First time load
                if group_id not in known_users:

                    known_users[group_id] = set()

                    try:
                        thread = cl.direct_thread(group_id)

                        if thread and thread.users:

                            for user in thread.users:
                                known_users[group_id].add(str(user.pk))

                            print(f"✅ Loaded users for GC: {group_id}")

                    except Exception as e:
                        print(f"⚠️ Initial Load Error ({group_id}): {e}")

                # Refresh thread
                thread = cl.direct_thread(group_id)

                if thread and thread.users:

                    for user in thread.users:

                        user_pk = str(user.pk)

                        # Ignore old users and bot itself
                        if (
                            user_pk not in known_users[group_id]
                            and user_pk != str(cl.user_id)
                        ):

                            name = (
                                user.full_name
                                if user.full_name
                                else user.username
                            )

                            welcome_msg = get_stylish_welcome(name)

                            # Send welcome message
                            cl.direct_send(
                                welcome_msg,
                                thread_ids=[group_id]
                            )

                            print(f"🎉 Welcomed {name} in {group_id}")

                            known_users[group_id].add(user_pk)

                            time.sleep(3)

            print("⏳ Checking all groups again in 45 sec...")
            time.sleep(45)

        except Exception as e:
            print(f"⚠️ Main Loop Error: {e}")
            time.sleep(15)

# =========================
# START BOT THREAD
# =========================
bot_thread = Thread(target=run_welcome_bot)
bot_thread.start()

# =========================
# RENDER PORT FIX
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
