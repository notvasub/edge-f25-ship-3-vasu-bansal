"""Simple password manager (stub).

This module provides placeholder functions for a command‑line password
manager.  Eventually it will allow users to register with a master
password, store encrypted passwords for various sites and retrieve them.
For now, it contains stubs that raise `NotImplementedError` and prints
a greeting when executed.
"""

import hashlib
import json
import os
import getpass


def _get_user_data_path() -> str:
    """Return the path to the user data JSON file."""
    return os.path.join(os.path.dirname(__file__), "data", "user_data.json")


def _load_user_db() -> dict:
    """Load user database from disk, returning an empty dict if missing/corrupt."""
    path = _get_user_data_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def _save_user_db(db: dict) -> None:
    """Save user database to disk (creates the file if it does not exist)."""
    path = _get_user_data_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, sort_keys=True)


def _hash_master_password(master_password: str) -> dict:
    """Create a PBKDF2-SHA256 hash record for the given master password.

    Returns a dict containing the KDF name, iterations, salt, and hash.
    """
    iterations = 200_000
    salt = os.urandom(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256", master_password.encode("utf-8"), salt, iterations
    )
    return {
        "kdf": "pbkdf2_sha256",
        "iterations": iterations,
        "salt": salt.hex(),
        "hash": derived_key.hex(),
    }

def register_user(username: str, master_password: str) -> None:
    """Register a new user with a master password.

    You will hash and store the master password in a
    JSON file for authentication.  This stub does nothing.

    Args:
        username: The username for the account.
        master_password: The master password to use.
    """
    if not username:
        raise ValueError("username must not be empty")
    if not master_password:
        raise ValueError("master_password must not be empty")

    db = _load_user_db()
    if username in db:
        raise ValueError("user already exists")

    db[username] = _hash_master_password(master_password)
    _save_user_db(db)


def add_password(site: str, username: str, password: str) -> None:
    """Store a password for a given site.

    You will encrypt the password and save it to a JSON file,
    associating it with the site and username.  This stub does nothing.

    Args:
        site: The website or service name.
        username: The account username for the site.
        password: The password to store.
    """
    if not site:
        raise ValueError("site must not be empty")
    if not username:
        raise ValueError("username must not be empty")
    if not password:
        raise ValueError("password must not be empty")

    passwords_path = os.path.join(os.path.dirname(__file__), "data", "passwords.json")
    os.makedirs(os.path.dirname(passwords_path), exist_ok=True)

    try:
        with open(passwords_path, "r", encoding="utf-8") as f:
            records = json.load(f)
            if not isinstance(records, list):
                records = []
    except FileNotFoundError:
        records = []
    except json.JSONDecodeError:
        records = []

    records.append({
        "site": site,
        "username": username,
        "password": password, 
    })

    with open(passwords_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, sort_keys=False)


def get_passwords() -> list[dict]:
    """Retrieve all stored passwords.

    This will read from an encrypted JSON file and return a list
    of dictionaries containing site, username and password.  For now
    it raises `NotImplementedError`.

    Returns:
        A list of stored passwords.
    """
    passwords_path = os.path.join(os.path.dirname(__file__), "data", "passwords.json")
    try:
        with open(passwords_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if not isinstance(records, list):
        return []

    cleaned: list[dict] = []
    for item in records:
        if not isinstance(item, dict):
            continue
        site = item.get("site")
        username = item.get("username")
        password = item.get("password")
        if isinstance(site, str) and isinstance(username, str) and isinstance(password, str): # AI implemented the "isinstance" part for better error handling. 
            cleaned.append({
                "site": site,
                "username": username,
                "password": password,
            })

    return cleaned


def main() -> None:
    """Entry point for the password manager.

    Simple interactive menu to register users, add passwords, and view
    stored passwords. This is a minimal, easy-to-use entry point.
    """
    while True:
        print("\nPassword Manager")
        print("1) Register user")
        print("2) Add password")
        print("3) View passwords")
        print("4) Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            try:
                username = input("Username: ").strip()
                master_password = getpass.getpass("Master password: ")
                register_user(username, master_password)
                print("User registered.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "2":
            try:
                site = input("Site: ").strip()
                site_username = input("Site username: ").strip()
                site_password = getpass.getpass("Site password: ")
                add_password(site, site_username, site_password)
                print("Password saved.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "3":
            records = get_passwords()
            if not records:
                print("No passwords stored.")
            else:
                for i, rec in enumerate(records, start=1):
                    site = rec.get("site", "")
                    uname = rec.get("username", "")
                    pwd = rec.get("password", "")
                    print(f"{i}. Site: {site} | Username: {uname} | Password: {pwd}")
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()