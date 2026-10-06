"""
Google IT Automation with Python - Course 1: Crash Course on Python
Module 4: Strings, Lists, and Dictionaries

Covers:
- String operations, slicing, formatting (.format and f-strings)
- List manipulation, slicing, tuples, list comprehensions
- Dictionary mappings, iteration, key-value manipulation, inverted indexes
"""

from typing import Dict, List, Tuple, Any


# -------------------------------------------------------------
# STRING OPERATIONS
# -------------------------------------------------------------

def is_palindrome(input_string: str) -> bool:
    """
    Checks if a string is a palindrome, ignoring casing and spaces.
    """
    cleaned = "".join([ch.lower() for ch in input_string if ch.isalnum()])
    return cleaned == cleaned[::-1]


def replace_ending(sentence: str, old: str, new: str) -> str:
    """
    If sentence ends with `old`, replaces the ending with `new`.
    Otherwise returns the original sentence.
    """
    if sentence.endswith(old):
        return sentence[:-len(old)] + new
    return sentence


def nametag(first_name: str, last_name: str) -> str:
    """
    Returns formatted nametag string: 'First L.'
    """
    if not first_name or not last_name:
        return (first_name or last_name).strip()
    return f"{first_name.strip()} {last_name.strip()[0]}."


def initials(phrase: str) -> str:
    """
    Extracts uppercase initials for each word in the phrase.
    """
    words = phrase.strip().split()
    return "".join(word[0].upper() for word in words if word)


def convert_distance_formatted(miles: float) -> str:
    """
    Formats distance conversion to exactly 2 decimal places.
    """
    km = miles * 1.6
    return f"{miles:.1f} miles equals {km:.2f} km"


# -------------------------------------------------------------
# LIST OPERATIONS & LIST COMPREHENSIONS
# -------------------------------------------------------------

def skip_elements(elements: List[Any]) -> List[Any]:
    """
    Returns every other element from the list, starting from index 0.
    Implemented using list comprehension with enumerate.
    """
    return [elem for idx, elem in enumerate(elements) if idx % 2 == 0]


def pig_latin(text: str) -> str:
    """
    Transforms sentence into Pig Latin by moving first letter of each
    word to the end and appending 'ay'.
    """
    words = text.split()
    transformed = [f"{w[1:]}{w[0]}ay" for w in words]
    return " ".join(transformed)


def octal_to_string(octal: int) -> str:
    """
    Converts a three-digit octal permission integer (e.g. 755) to Unix string (e.g. 'rwxr-xr-x').
    """
    result = []
    value_letters = [(4, "r"), (2, "w"), (1, "x")]
    for digit_char in str(octal):
        digit = int(digit_char)
        for value, letter in value_letters:
            if digit >= value:
                result.append(letter)
                digit -= value
            else:
                result.append("-")
    return "".join(result)


def group_list(group: str, users: List[str]) -> str:
    """
    Formats a user group as 'Group: user1, user2, ...'
    """
    return f"{group}: {', '.join(users)}"


def guest_list(guests: List[Tuple[str, int, str]]) -> List[str]:
    """
    Formats a list of guest tuples (name, age, profession) into announcement strings.
    """
    return [f"{name} is {age} years old and works as {job}" for name, age, job in guests]


def squares(start: int, end: int) -> List[int]:
    """
    Computes squares of integers between start and end inclusive using list comprehension.
    """
    return [x**2 for x in range(start, end + 1)]


def odd_numbers(maximum: int) -> List[int]:
    """
    Returns all odd numbers up to maximum using list comprehension.
    """
    return [x for x in range(1, maximum + 1) if x % 2 != 0]


# -------------------------------------------------------------
# DICTIONARY OPERATIONS
# -------------------------------------------------------------

def email_list(domains: Dict[str, List[str]]) -> List[str]:
    """
    Converts a dictionary mapping domain -> list of users into a flat list of 'user@domain'.
    """
    emails = []
    for domain, users in domains.items():
        for user in users:
            emails.append(f"{user}@{domain}")
    return emails


def groups_per_user(group_dictionary: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Inverts group-to-users dictionary to user-to-groups dictionary.
    """
    user_groups: Dict[str, List[str]] = {}
    for group, users in group_dictionary.items():
        for user in users:
            if user not in user_groups:
                user_groups[user] = []
            user_groups[user].append(group)
    return user_groups


def add_prices(basket: Dict[str, float]) -> float:
    """
    Calculates total price of items in grocery basket.
    """
    return round(sum(basket.values()), 2)


def count_letters(text: str) -> Dict[str, int]:
    """
    Counts frequency of alphabetical letters in text (case-insensitive).
    """
    counts: Dict[str, int] = {}
    for char in text.lower():
        if char.isalpha():
            counts[char] = counts.get(char, 0) + 1
    return counts


def highlight_word(sentence: str, word: str) -> str:
    """
    Highlights occurrences of `word` in `sentence` by converting them to UPPERCASE.
    """
    words = sentence.split()
    highlighted = [w.upper() if w == word else w for w in words]
    return " ".join(highlighted)


def combine_guests(guests1: Dict[str, int], guests2: Dict[str, int]) -> Dict[str, int]:
    """
    Combines two party guest dictionaries with their guest count, prioritizing guests2.
    """
    combined = guests1.copy()
    combined.update(guests2)
    return combined


def test_module4() -> None:
    """
    Validation assertion test suite for Module 4.
    """
    # 1. Strings
    assert is_palindrome("Never Odd Or Even") is True
    assert is_palindrome("abc") is False
    assert is_palindrome("kayak") is True

    assert replace_ending("She sells seashells by the seashore", "sea", "ocean") == "She sells seashells by the seashore"
    assert replace_ending("The weather is nice in May", "may", "april") == "The weather is nice in May"
    assert replace_ending("The weather is nice in May", "May", "April") == "The weather is nice in April"

    assert nametag("Jane", "Doe") == "Jane D."
    assert initials("Universal Serial Bus") == "USB"
    assert convert_distance_formatted(5) == "5.0 miles equals 8.00 km"

    # 2. Lists
    assert skip_elements(["a", "b", "c", "d", "e", "f", "g"]) == ["a", "c", "e", "g"]
    assert skip_elements([]) == []
    assert pig_latin("hello how are you") == "ellohay owhay reaay ouyay"

    assert octal_to_string(755) == "rwxr-xr-x"
    assert octal_to_string(644) == "rw-r--r--"
    assert octal_to_string(777) == "rwxrwxrwx"

    assert group_list("admin", ["root", "ahmed"]) == "admin: root, ahmed"
    guests = [("Ken", 30, "Chef"), ("Pat", 35, "Lawyer")]
    assert guest_list(guests) == [
        "Ken is 30 years old and works as Chef",
        "Pat is 35 years old and works as Lawyer"
    ]
    assert squares(2, 5) == [4, 9, 16, 25]
    assert odd_numbers(7) == [1, 3, 5, 7]

    # 3. Dictionaries
    emails = email_list({"gmail.com": ["clark.kent", "bruce.wayne"], "yahoo.com": ["diana.prince"]})
    assert emails == ["clark.kent@gmail.com", "bruce.wayne@gmail.com", "diana.prince@yahoo.com"]

    groups = {"local": ["admin", "userA"], "public": ["admin", "userB"], "administrator": ["admin"]}
    inverted = groups_per_user(groups)
    assert inverted["admin"] == ["local", "public", "administrator"]
    assert inverted["userA"] == ["local"]
    assert inverted["userB"] == ["public"]

    assert add_prices({"groceries": 32.44, "meat": 15.10}) == 47.54
    letter_freq = count_letters("AaBbCc123!")
    assert letter_freq == {"a": 2, "b": 2, "c": 2}

    assert highlight_word("Have a nice day", "nice") == "Have a NICE day"
    g1 = {"Rick": 2, "Morty": 1}
    g2 = {"Summer": 1, "Rick": 3}
    assert combine_guests(g1, g2) == {"Rick": 3, "Morty": 1, "Summer": 1}

    print("[PASS] Module 4: All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module4()
