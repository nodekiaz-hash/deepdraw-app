from supabase import create_client
import os

# -------------------------
# 🔐 SUPABASE INIT
# -------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------------
# 👤 USER LEKÉRÉS EMAIL ALAPJÁN
# -------------------------
def get_user(email):
    response = supabase.table("users").select("*").eq("email", email).execute()
    
    if response.data:
        return response.data[0]
    return None


# -------------------------
# 🆕 USER REGISZTRÁCIÓ
# -------------------------
def create_user(email):
    data = {
        "email": email,
        "credit": 3
    }

    response = supabase.table("users").insert(data).execute()

    if response.data:
        return response.data[0]
    return None


# -------------------------
# 🔄 GET OR CREATE (EZT HASZNÁLD!)
# -------------------------
def get_or_create_user(email):
    user = get_user(email)

    if user:
        return user, False  # már létezett

    user = create_user(email)
    return user, True  # új user


# -------------------------
# 💳 CREDIT LEKÉRÉS
# -------------------------
def get_credit(email):
    user = get_user(email)

    if user:
        return user["credit"]
    return 0


# -------------------------
# ➖ CREDIT LEVONÁS
# -------------------------
def decrement_credit(email):
    user = get_user(email)

    if not user:
        return False

    new_credit = user["credit"] - 1

    if new_credit < 0:
        return False

    supabase.table("users").update({"credit": new_credit}).eq("email", email).execute()
    return True


# -------------------------
# ➕ CREDIT NÖVELÉS (későbbre)
# -------------------------
def add_credit(email, amount):
    user = get_user(email)

    if not user:
        return False

    new_credit = user["credit"] + amount

    supabase.table("users").update({"credit": new_credit}).eq("email", email).execute()
    return True