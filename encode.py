import string
import random

def encode(message, corpus_length):
    
    alphabet = [x for x in string.printable[:95]]

    variation = corpus_length // len(alphabet)
    

    encoded_message = []
    for character in message:
        encoded_message.append(alphabet.index(character.lower())*variation)
#    encoded_message.append(random.choice(range(alphabet.index(character), 
#                corpus_length, len(alphabet))))

    return encoded_message, len(message)

