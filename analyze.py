#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# This string contains all the things that count as a letter, in order.
# You could experiment here with including spaces, punctuation, or lower
# case letters, or see how encryption changes if your alphabet is in a
# different order.

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# It is common in alphabetic ciphers to represent strings as arrays of
# numbers, to make them more convenient to manipulate.  The numbers()
# function converts a string like 'ABCXYZ' to an array of numbers like
# [0, 1, 2, 23, 24, 25], and the letters() function converts back.
#
# I use NumPy arrays rather than Python lists, because they support
# resizing by repeating the elements as necessary as well as vectorized
# addition, subtraction, and remainder, which make the encryption and
# decryption functions more elegant to read.
#
# (Could you rewrite this code and the encryption and decryption functions
# to use lists instead of arrays?)

def numbers(msg):
    return np.fromiter((alphabet.find(x) for x in msg if x in alphabet), int)

def letters(msg):
    return ''.join(alphabet[x] for x in msg)


# The Vigenère cipher is a generalization of the Cæsar cipher; rather
# than rotating the alphabet the same amount in every part of the message,
# it rotates each letter independently.  Where the Cæsar cipher uses a
# single letter key, the Vigenère cipher uses a key string that is the
# same length as the message; each letter is encrypted as in a Cæsar
# cipher, according to its corresponding key letter.  In practice, one
# often uses a short key word or phrase, repeated as necessary to make
# it the same length as the message.  (Note that by this convention,
# a one-letter key word results in an ordinary Cæsar cipher.)

def Vigenère_encrypt(msg, key):
    msg, key = numbers(msg), numbers(key)
    key = np.resize(key, len(msg))  # repeat to correct length
    return letters((msg + key) % len(alphabet))

def Vigenère_decrypt(msg, key):
    msg, key = numbers(msg), numbers(key)
    key = np.resize(key, len(msg))  # repeat to correct length
    return letters((msg - key) % len(alphabet))


# These functions use Matplotlib to visualize letter frequencies, in
# order to analyze the result of Vigènere encryption.  The details of
# Matplotlib are outside the scope of the analysis, but the the plot_key()
# function fills a single axis with a histogram of letter frequencies
# for a particular plaintext and key, while the plot_keys() function
# produces a complete plot comparing a single plaintext encrypted under
# a variety of keys.

def plot_key(ax, plaintext, key):
    ciphertext = Vigenère_encrypt(plaintext, key)
    counts = Counter(letter for letter in ciphertext)
    if ciphertext == Vigenère_decrypt(ciphertext, key):
        ax.set_ylabel("plain")
    else:
        ax.set_ylabel(key)
    ax.bar(range(len(alphabet)), [counts[x] for x in alphabet])
    ax.set_xticks(range(len(alphabet)))
    ax.set_xticklabels(alphabet)
    ax.set_yticks([])
    ax.label_outer()

def plot_keys(msg, *keys):
    fig, axes = plt.subplots(len(keys), sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0})
    fig.suptitle('Letter frequency analysis')
    for ax, key in zip(axes, keys):
        plot_key(ax, msg, key)
    plt.show()


# An example of how these functions can be used, which tests that decryption
# correctly recovers the message, and provides informative messages.
#
# You can follow along with the example used in the Wikipedia page for the
# Vigenère cipher by running:
#
#    Vigenère_test('ATTACKATDAWN', 'LEMON')

def Vigenère_test(plaintext, key):
    ciphertext = Vigènere_encrypt(plaintext, key)
    decrypted = Vigenère_decrypt(ciphertext, key)

    print('Encrypted "{}" with key "{}".'.format(plaintext, key))
    print('Ciphertext is "{}".'.format(ciphertext))
    if recovered == plaintext:
        print('Decryption produced the original plaintext.')
    else:
        print('Decryption produced "{}".'.format(recovered))


# Encrypt a file of sample text using some related keys to show how
# patterns in the plaintext are spread out and combined according to the
# keyword in the ciphertext.  (You can try other sample texts; perhaps
# see how the letter frequencies are different for different authors or
# in non-English text.)

with open('sample') as f:
    plaintext = ''.join(x for x in f.read().upper() if x in alphabet)
    plot_keys(plaintext, 'A', 'B', 'F', 'BF', 'BEFORE')
    # Can you see patterns that would be hints for a cryptologist?
    # Try other keys!  Can you make the letter frequencies in the
    # ciphertext look flat?
