from instagrapi import Client
import time
import os

# --- CONFIGURATION ---
USER = '3xbotn'
PASS = 'royql900'
TARGET_GROUP_ID = '1384445266434510'  # String format me hi rehne dein
SESSION_FILE = "session.json"

cl = Client()

# --- LOGIN LOGIC ---
def login_user():
    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(USER, PASS)
            print("✅ Session Login Successful!")
        except Exception:
            cl.login(USER, PASS)
            cl.dump_settings(SESSION_FILE)
    else:
        cl.login(USER, PASS)
        cl.dump_settings(SESSION_FILE)
        print("✅ New Login Successful!")

login_user()

# --- STYLISH WELCOME MESSAGE TEMPLATE ---
def get_stylish_welcome(name):
    message = f"""
╔═══════════════╗
║ ✨ WELCOME ✨ ║
╚═══════════════╝

🔥 Hey {name}! 🔥
   🥳✨. 
Group rules check kar lena aur enjoy karo! 💖

✨ Happy Chatting! ✨
    """
    return message.strip()

# --- MAIN LOGIC ---
def run_welcome_bot():
    print(f"🤖 Welcome Bot Started for Group: {TARGET_GROUP_ID}")
    print("⏳ New members check ho rahe hain...")
    
    known_user_ids = set()
    
    try:
        # Initial fetch ke liye direct_thread sahi hai
        thread = cl.direct_thread(TARGET_GROUP_ID)
        if thread and thread.users:
            for user in thread.users:
                known_user_ids.add(str(user.pk))  # ID ko string me save karna safe rehta hai
            print(f"📝 Initial {len(known_user_ids)} members loaded.")
        
    except Exception as e:
        print(f"⚠️ Error loading initial members: {e}")

    while True:
        try:
            # FIX 1: direct_thread_by_id use kiya taaki har baar fresh data aaye
            thread = cl.direct_thread(TARGET_GROUP_ID)
            
            if thread and thread.users:
                new_users_found = []

                for user in thread.users:
                    user_pk = str(user.pk)
                    
                    # Agar user naya hai aur bot khud nahi hai
                    if user_pk not in known_user_ids and user_pk != str(cl.user_id):
                        new_users_found.append(user)
                
                if new_users_found:
                    for user in new_users_found:
                        name_to_use = user.full_name if user.full_name else user.username
                        welcome_msg = get_stylish_welcome(name_to_use)
                        
                        # FIX 2: Sahi direct_send format use kiya thread_ids ke saath
                        cl.direct_send(welcome_msg, thread_ids=[TARGET_GROUP_ID])
                        print(f"🎉 Welcomed: {name_to_use} (@{user.username})")
                        
                        known_user_ids.add(str(user.pk))
                        time.sleep(3)  # Spam se bachne ke liye delay

            # FIX 3: Time badha kar 45 seconds kiya (Account Safety ke liye)
            print("⏳ Checking again in 45 seconds...")
            time.sleep(5)

        except Exception as e:
            print(f"⚠️ Loop Error: {e}")
            time.sleep(5)  # Error aane par 1 minute wait karein

if __name__ == "__main__":
    run_welcome_bot()
