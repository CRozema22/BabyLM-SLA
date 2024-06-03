from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import re
import nltk
import pandas as pd
from nltk.tokenize import PunktSentenceTokenizer
import json


def score1(text, pos, child=False):

  if re.search("PRON (VERB )?(\w* )?VERB (PRON)?", pos):
    if child:
      return 0
    return 1
  return 0
  #pronoun case
  #he doesn't like him
  # pron-(Aux)-(Neg)-V-(Pron)

def score2(text, pos, child=False):
  articles = ["a", "the", "an", "A", "The", "An"]
  for art in articles:
    if art in text:
      if child:
        return 5
      return 2
  return 0
  #Article (check if determiner too)

def score3(text, pos, child=False):
  words = text.split(" ")
  if "'s" in words:
    inx = words.index("'s")
    pos_list = pos.split(" ")
    if pos_list[inx] == "VERB":
      if child:
        return 6
      return 3

  return 0
  #singular copula

def score4(text, pos, child=False):
  if re.search('VERB', pos):
    pos_list = pos.split(" ")
    inx = pos_list.index('VERB')
    inx_verb = text.split(" ")[inx]
    if inx_verb.endswith('ing'):
      if child:
        return 2
      return 4

  return 0
  # -ing
  #V+ing

def score5(text, pos, child=False):
  if re.search('NOUN', pos):
    pos_list = pos.split(" ")
    inx = pos_list.index('NOUN')
    inx_noun = text.split(" ")[inx]
    if inx_noun.endswith('s') and not inx_noun.endswith('es'):
      if child:
        return 1
      return 5

  return 0
  #plural
  #NP+pl

def score6(text, pos, child=False):
  if re.search('VERB VERB', pos):
    if re.search("((is)|('s)|(are)|('re)) \w*ing", text):
      if child:
        return 9
      return 6

  return 0
  #singular auxiliary
  #she is /she's dancing
  # -be-V+ing

def score7(text, pos, child=False):
  if re.search('VERB', pos):
    pos_list = pos.split(" ")
    inx = pos_list.index('VERB')
    inx_verb = text.split(" ")[inx]
    if inx_verb.endswith('ed'):
      if child:
        return 4
      return 7

  return 0
  #past regular
  #NP/Pron - (have) - V+pst - NP/Pron



def score8(text, pos, child=False):
  
  with open('irregular_verbs.txt') as infile:
    irregular_verbs = infile.read().split("\n")

  if re.search('VERB', pos):
    pos_list = pos.split(" ")
    inx = pos_list.index('VERB')
    inx_verb = text.split(" ")[inx]
    if inx_verb in irregular_verbs:
      if child:
        return 3
      return 8

  return 0
  #past irregular
  #NP/pron - V+pst - NP/Pron

def score9(text, pos, child=False):
  if re.search('NOUN', pos):
    pos_list = pos.split(" ")
    inx = pos_list.index('NOUN')
    inx_noun = text.split(" ")[inx]
    if inx_noun.endswith('es'):
      if child:
        return 0
      return 9

  return 0
  #long plural
  #houses


def score10(text, pos, child=False):
  if re.search('NOUN', pos):
    pos_list = pos.split(" ")
    inx = pos_list.index('NOUN')
    words = text.split(" ")
    if inx != len(words) -1:
      if words[inx + 1] == "'s":
        if pos_list[inx + 1] != 'VERB':
          if child:
            return 7
          return 10

  return 0


  #possessive
  #Det- (Adj) - N + poss-(N)
  #the king's

def score11(text, pos, child=False):
  pos_list = pos.split(" ")
  for p in pos_list:
    if p == 'VERB':
      if p.endswith("s"):
        if child:
          return 8
        return 11
  return 0
  #3rd person singular
  #NP/Pron+sing - V+tns - (Adv)

def total_score(sentence, pos_sentence, child=False):
  '''
  Calculates and returns total score by calling all scoring functions
  To be averaged over sentences or tokens
  '''

  score = 0
  score += score1(sentence, pos_sentence, child=child)
  score += score2(sentence, pos_sentence, child=child)
  score += score3(sentence, pos_sentence, child=child)
  score += score4(sentence, pos_sentence, child=child)
  score += score5(sentence, pos_sentence, child=child)
  score += score6(sentence, pos_sentence, child=child)
  score += score7(sentence, pos_sentence, child=child)
  score += score8(sentence, pos_sentence, child=child)
  score += score9(sentence, pos_sentence, child=child)
  score += score10(sentence, pos_sentence, child=child)
  score += score11(sentence, pos_sentence, child=child)

  return score

def diff_score(sequence, pos, sent_tokenizer, child=False):
  '''
  Calculates difficulty score for a sequence given sequence, pos and sentence_tokenizer trained on full dataset
  Returns sentence averaged difficulty score and token averaged difficulty score
  child=True if FLA
  '''
  
  #sentence tokenizer
  #chunk pos in equal lists as sentences
  sentences = sent_tokenizer.tokenize(sequence)
  lengths = []
  for sent in sentences:
    lengths.append(len(sent.split(" ")))

  splitpos = pos.split(" ")
  posses = []
  start = 0
  for i in lengths:
    posses.append(" ".join(splitpos[start:start + i]))
    start = i + start

  total = 0
  for sent, pos in zip(sentences, posses):
    if len(sent.split(" ")) == len(pos.split(" ")):
      total += total_score(sent, pos, child=child)
    else:
      print(sent, pos)

  diff_sent = total / len(sentences)
  diff_tokens = total / len(sequence.split(" "))

  return diff_sent, diff_tokens

