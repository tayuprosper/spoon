import nltk
from nltk.tokenize import sent_tokenize

# Download the required punctuation model (only needs to be run once)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True) 

def split_into_sentences(text: str) -> list[str]:
    return sent_tokenize(text)

text = "Hello there! My name is Dr. Smith. I love coding, e.g., in Python."
print(split_into_sentences(text))
# Output: ['Hello there!', 'My name is Dr. Smith.', 'I love coding, e.g., in Python.']