import re

# Convert text into lowercase word tokens
def tokenise(text):
    text = text.lower()
    return re.findall(r"[a-z0-9]+", text)