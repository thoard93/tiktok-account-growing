"""
Credential Generator
====================
Generates natural, believable usernames, emails, and passwords for TikTok accounts.
"""

import random
import string
import secrets
from typing import Tuple

# Real first names for natural usernames
FIRST_NAMES = [
    # Female names
    "emma", "olivia", "ava", "sophia", "mia", "isabella", "charlotte", "luna",
    "harper", "ella", "mila", "aria", "scarlett", "penelope", "layla", "chloe",
    "riley", "zoey", "nora", "lily", "eleanor", "hannah", "addison", "aubrey",
    "stella", "natalie", "zoe", "leah", "hazel", "violet", "aurora", "savannah",
    "audrey", "brooklyn", "bella", "claire", "skylar", "lucy", "paisley", "everly",
    # Male names
    "liam", "noah", "oliver", "james", "elijah", "william", "henry", "lucas",
    "benjamin", "theo", "jack", "levi", "alex", "mason", "logan", "aiden",
    "ethan", "jacob", "michael", "daniel", "matthew", "anthony", "joseph", "david",
    "jackson", "sebastian", "owen", "gabriel", "carter", "jayden", "luke", "dylan",
    "grayson", "luca", "isaac", "layton", "julian", "leo", "lincoln", "jace"
]

# Last name initials or short suffixes
LAST_INITIALS = list("abcdefghjklmnpqrstuvwxyz")

# Fun suffixes that TikTok users actually use
NATURAL_SUFFIXES = [
    "", "x", "xx", "xo", "oo", "ie", "y", "ey", "ly", "ee",
    "_", "__", ".", "..", "._.", "_x", "x_"
]

# Year patterns (birth years, current trends)
YEAR_PATTERNS = [
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "99", "98", "97", "96", "95", "94", "93", "2k", "22", "23", "24", "25"
]

# Activity/interest tags common on TikTok
INTEREST_TAGS = [
    "vibes", "life", "daily", "official", "real", "the", "itz", "its",
    "just", "only", "that", "ur", "ya", "yo", "hey", "hi", "luv"
]

# Email domains
EMAIL_DOMAINS = [
    "gmail.com", "outlook.com", "yahoo.com", "icloud.com", "proton.me"
]


def generate_username(style: str = "random") -> str:
    """
    Generate a natural, TikTok-style username.
    
    Styles:
    - "name_year": emma_02, liam.99
    - "name_initial": olivia.j, noah_k
    - "name_double": emmaxemma, noahnoah
    - "name_tag": justliam, itzava
    - "random": any of the above randomly
    
    Returns:
        Natural-looking username
    """
    if style == "random":
        style = random.choice(["name_year", "name_initial", "name_double", "name_tag"])
    
    name = random.choice(FIRST_NAMES)
    
    if style == "name_year":
        # emma02, liam_99, olivia.05
        sep = random.choice(["", "_", "."])
        year = random.choice(YEAR_PATTERNS)
        return f"{name}{sep}{year}"
    
    elif style == "name_initial":
        # emma.j, liam_k, noahb
        sep = random.choice(["", "_", "."])
        initial = random.choice(LAST_INITIALS)
        suffix = random.choice(NATURAL_SUFFIXES[:5])  # Use simpler suffixes
        return f"{name}{sep}{initial}{suffix}"
    
    elif style == "name_double":
        # emmaxemma, noahxnoah, olivia.olivia
        sep = random.choice(["x", "_", ".", ""])
        suffix = random.choice(NATURAL_SUFFIXES[:3])
        return f"{name}{sep}{name}{suffix}"
    
    elif style == "name_tag":
        # justliam, itzava, theemma
        tag = random.choice(INTEREST_TAGS)
        suffix = random.choice(NATURAL_SUFFIXES[:5])
        # 50% chance tag goes first or last
        if random.random() > 0.5:
            return f"{tag}{name}{suffix}"
        else:
            return f"{name}{tag}{suffix}"
    
    # Fallback
    return f"{name}{random.randint(10, 99)}"


def generate_email(username: str = None) -> str:
    """
    Generate a matching email address.
    
    Args:
        username: Optional username to base email on
        
    Returns:
        Natural-looking email
    """
    if not username:
        username = generate_username()
    
    # Clean username for email (remove special chars except underscore)
    email_name = username.replace(".", "").replace("x", "_").replace(" ", "")
    
    # Add some uniqueness
    suffix = random.randint(1, 999)
    domain = random.choice(EMAIL_DOMAINS)
    
    return f"{email_name}{suffix}@{domain}"


def generate_password(length: int = 14) -> str:
    """
    Generate a secure but typeable password.
    
    Returns:
        Password like: Sunny$Tiger847
    """
    # Use a memorable pattern: Word + Symbol + Word + Numbers
    words = ["Sunny", "Happy", "Lucky", "Swift", "Brave", "Bright", "Cool", "Wild",
             "Star", "Moon", "Fire", "Ocean", "Cloud", "Storm", "Dream", "Magic"]
    symbols = ["!", "@", "#", "$", "%", "&", "*"]
    
    word1 = random.choice(words)
    symbol = random.choice(symbols)
    word2 = random.choice(words)
    numbers = random.randint(100, 999)
    
    return f"{word1}{symbol}{word2}{numbers}"


def generate_credentials(name_prefix: str = "") -> Tuple[str, str, str]:
    """
    Generate a complete set of credentials for a TikTok account.
    
    Args:
        name_prefix: Optional prefix (currently unused for natural names)
        
    Returns:
        Tuple of (username, email, password)
    """
    username = generate_username()
    email = generate_email(username)
    password = generate_password()
    
    return username, email, password


def generate_batch_credentials(count: int, name_prefix: str = "") -> list:
    """
    Generate multiple sets of credentials.
    
    Args:
        count: Number of credential sets to generate
        name_prefix: Optional prefix for usernames (unused for natural names)
        
    Returns:
        List of dicts with username, email, password
    """
    credentials = []
    used_usernames = set()
    
    for _ in range(count):
        # Ensure unique usernames
        for _ in range(10):  # Max 10 attempts
            username, email, password = generate_credentials(name_prefix)
            if username not in used_usernames:
                used_usernames.add(username)
                break
        
        credentials.append({
            "username": username,
            "email": email,
            "password": password
        })
    
    return credentials
