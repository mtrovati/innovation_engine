# import csv
# from multiprocessing import Process
import nltk
from nltk.corpus import wordnet as wn
import nltk.data
import networkx as nx
import matplotlib.pyplot as plt


def split_texts_into_sentences(text):
    # Split the inut text into sentences, which will populate a list
    temp = []
    list_sentences = []
    temp = text.split(".")
    for item in temp:
        if item != '':
            list_sentences.append(item)
    return list_sentences


def tagger(sentence):
    # Carry out tokenisation and POS (Part-of-Speech) tagging for an input sentence
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    return tagged


def text_analysis(sentence):
    # Identify nouns in a sentence. 
    nouns = []
    analysis = tagger(sentence)  # Tokenise and POS tag the input sentence
    for item in analysis:
        if 'NN' in item[1]:
            nouns.append(item[0])
    return nouns


def couples_graph_complete(nouns_list):
    # Create a complete graph (every node connected to any other node)
    # from a list of nouns. Each node corresponds to a noun
    final_list = []
    while len(nouns_list) > 0:
        temp = []
        i = 1
        while i < len(nouns_list):
            temp.append([nouns_list[0], nouns_list[i]])
            i = i + 1
        final_list.extend(temp)
        nouns_list.pop(0)
    return final_list


def synonyms(word):
    # Find the synonyms of an input word
    list_lemmas = []
    for synset in wn.synsets(word):
        if '.n.' in str(synset):
            for lemma in synset.lemmas():
                if lemma.name() not in list_lemmas:  # I don't want duplicates
                    list_lemmas.append(lemma.name())
    return list_lemmas


def couples_tree_graph(nouns_list):
    # Create a tree graph, where the first item (noun) in the input list will be the root of the tree
    # The root node will be connected to all the other nodes. These are not connected with one another
    couples = []
    i = 1
    while i < len(nouns_list):
        couples.append([nouns_list[0], nouns_list[i]])
        i = i + 1
    return couples


def get_tree_graph_list_syn(word):
    # Create a list where the firt item is the input word and the next ones are its synonyms.
    # This method needs to be used in conjunction with the above method.
    temp = list(synonyms(word))
    if word not in temp:
        return [word] + temp
    else:
        return temp


def semantic_network(sentence):
    # Create the edges and nodes of a semantic network defined by the nouns identified in a text.
    syns = []
    analysis = text_analysis(sentence)
    text_analysis_nouns = couples_graph_complete(analysis)
    for couple in text_analysis_nouns:
        if couple != []:
            G.add_edge(couple[0], couple[1])
    for couple in text_analysis_nouns:
        for noun in couple:
            syns.extend(couples_tree_graph(get_tree_graph_list_syn(noun)))
    for syn in syns:
        G.add_edge(syn[0], syn[1])


if __name__ == "__main__":
    G = nx.Graph()
    text = "Paul loves cats. Worms hate birds and humans. John likes burgers."  # input sentences.
    sentences = split_texts_into_sentences(text)
    for sentence in sentences:
        semantic_network(sentence)
    print G.nodes()
    # Optional: print nodes and edges
    print G.edges()
    nx.draw(G, with_labels=True)
    plt.show()
