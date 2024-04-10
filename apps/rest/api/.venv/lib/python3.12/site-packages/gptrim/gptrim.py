import re
from typing import Optional, List

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer

nltk.download('punkt')
nltk.download('stopwords')

s = "But don’t humans also have genuinely original ideas?” Come on, read a fantasy book. It’s either a Tolkien clone, or it’s A Song Of Ice And Fire. Tolkien was a professor of Anglo-Saxon language and culture; no secret where he got his inspiration. A Song Of Ice And Fire is just War Of The Roses with dragons. Lannister and Stark are just Lancaster and York, the map of Westeros is just Britain (minus Scotland) with an upside down-Ireland stuck to the bottom of it – wake up, sheeple! Dullards blend Tolkien into a slurry and shape it into another Tolkien-clone. Tolkien-level artistic geniuses blend human experience, history, and the artistic corpus into a slurry and form it into an entirely new genre. Again, the difference is how finely you blend and what spices you add to the slurry."

ARTICLES_PREPOSITIONS = {
    "english": ['the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of']
}

NEGATION_WORDS = {
    "spanish": [
        'no',
        'ni',
        'nunca',
        'jamas',
        'tampoco',
        'nadie',
        'nada',
        'ninguno',
        'ninguna',
        'ningunos',
        'ningunas',
        'ningun',
    ],
    "english": [
        'no',
        'nor',
        'not',
        'don',
        "dont",
        'ain',
        'aren',
        "arent",
        'couldn',
        "couldnt",
        'didn',
        "didnt",
        'doesn',
        "doesnt",
        'hadn',
        "hadnt",
        'hasn',
        "hasnt",
        'haven',
        "havent",
        'isn',
        "isnt",
        'mightn',
        "mightnt",
        'mustn',
        "mustnt",
        'needn',
        "neednt",
        'shan',
        "shant",
        'shouldn',
        "shouldnt",
        'wasn',
        "wasnt",
        'weren',
        "werent",
        'won',
        "wont",
        'wouldn',
        "wouldnt",
    ],
}

PUNCTUATION = [".", ",", "'", '"', "!", "?", ";", ":", "-"]


def trim(
    text: str, stemmer: Optional[str] = None, language: str = "english", remove_spaces: bool = True,
        remove_stopwords: bool = True, remove_punctuation: bool = False) -> str:

    if language not in stopwords.fileids():
        raise ValueError("Unsupported language")

    accepted_stemmers = ("snowball", "porter", "lancaster")
    if stemmer and stemmer not in accepted_stemmers:
        raise ValueError("Stemmer must be one of", accepted_stemmers)

    # merge contractions
    text: str = text.replace("'", "").replace("’", "")

    # tokenize words, keep uppercase
    tokenized: List = nltk.word_tokenize(text)

    if remove_punctuation:
        tokenized = [word for word in tokenized if word not in PUNCTUATION]

    if remove_stopwords:
        nltk_stopwords = stopwords.words(language)
        words_to_exclude = set(
            nltk_stopwords + ARTICLES_PREPOSITIONS.get(language, [])
        ) - set(NEGATION_WORDS.get(language, []))

        tokenized = [word for word in tokenized if word.lower() not in words_to_exclude]

    words = tokenized

    if stemmer:
        if stemmer == "porter":
            stemmer = PorterStemmer()
        elif stemmer == "snowball":
            stemmer = SnowballStemmer(language)
        elif stemmer == "lancaster":
            stemmer = LancasterStemmer()
        words = [stemmer.stem(word) for word in tokenized]

        # restore title_case and uppercase after stemming
        case_restored = []
        for i, word in enumerate(words):
            if tokenized[i].istitle():
                word = word.title()
            elif tokenized[i].isupper():
                word = word.upper()
            case_restored.append(word)

        words = case_restored

    # remove spaces
    join_str = "" if remove_spaces else " "
    trimmed: str = join_str.join(words).strip()
    if not remove_punctuation:
        # this is a hack to remove spaces before punctuation
        trimmed = re.sub(r"\s([?.!,:;])", r"\1", trimmed)

    return trimmed
