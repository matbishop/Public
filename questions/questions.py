import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory, file)) as f:
            contents = f.read()
            files[file] = contents
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document.lower())
    tokenized = []
    stopwords = nltk.corpus.stopwords.words("english")
    punctuation = string.punctuation
    for word in words:
        if word not in stopwords and word not in punctuation:
            tokenized.append(word)
    return tokenized


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num_docs = len(documents)
    idfs = {}
    for doc in documents:
        words = []
        for word in documents[doc]:
            if word in words:
                continue
            elif word in idfs.keys():
                idfs[word] += 1
            else:
                idfs[word] = 1
    for word in idfs:
        idfs[word] = math.log(num_docs / idfs[word])
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_tf_idfs = {
        doc: 0
        for doc in files
    }
    for file in files:
        for word in query:
            if word in files[file]:
                file_tf_idfs[file] += files[file].count(word) * idfs[word]
        if file_tf_idfs[file] == 0:
            file_tf_idfs.pop(file)
    top_files = sorted(file_tf_idfs, key=lambda x: file_tf_idfs[x])
    return top_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_values = {
        sentence: {
            "idf": 0,
            "qtd": 0.0
        }
        for sentence in sentences
    }
    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                sentences_values[sentence]["idf"] += idfs[word]
                sentences_values[sentence]["qtd"] += 1
    for sentence in sentences_values:
        sentences_values[sentence]["qtd"] /= len(sentences[sentence])
    sorted_sentences = sorted(
        sentences_values, 
        key=lambda x: (sentences_values[x]["idf"], sentences_values[x]["qtd"]), 
        reverse=True
        )
    return sorted_sentences[:n]


if __name__ == "__main__":
    main()
