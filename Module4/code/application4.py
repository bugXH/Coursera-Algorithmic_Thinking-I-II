from alg_application4_provided import (HUMAN_EYELESS_URL,
                                       FRUITFLY_EYELESS_URL,
                                       CONSENSUS_PAX_URL,
                                       PAM50_URL,
                                       WORD_LIST_URL,
                                       read_scoring_matrix,
                                       read_protein,
                                       read_words)
from project4 import (compute_local_alignment, compute_alignment_matrix,
                      compute_global_alignment, build_scoring_matrix)
from collections import defaultdict
from random import shuffle
from matplotlib import pyplot as plt
import math


def question1():
    """
    Code for quetion 1
    """
    human = read_protein(HUMAN_EYELESS_URL)
    fruitfly = read_protein(FRUITFLY_EYELESS_URL)
    score_mat = read_scoring_matrix(PAM50_URL)
    align_mat = compute_alignment_matrix(human, fruitfly, score_mat, False)
    result = compute_local_alignment(human, fruitfly, score_mat, align_mat)
    return result


def question2():
    """
    Code for question 2
    """
    q1_result = question1()
    score_mat = read_scoring_matrix(PAM50_URL)
    human, fruitfly = q1_result[1], q1_result[2]
    human = human.replace('-', '')
    fruitfly = fruitfly.replace('-', '')
    consensus = read_protein(CONSENSUS_PAX_URL)
    align_m_h = compute_alignment_matrix(human, consensus, score_mat, True)
    align_m_f = compute_alignment_matrix(fruitfly, consensus, score_mat, True)
    global_align_hc = compute_global_alignment(human, consensus,
                                               score_mat, align_m_h)
    global_h, global_ch = global_align_hc[1], global_align_hc[2]
    per1, per2 = 0, 0
    for idx in range(len(global_h)):
        if global_h[idx] == global_ch[idx]:
            per1 += 1
    print float(per1) / len(global_h) * 100

    global_align_fc = compute_global_alignment(fruitfly, consensus,
                                               score_mat, align_m_f)
    global_f, global_cf = global_align_fc[1], global_align_fc[2]
    for idx in range(len(global_f)):
        if global_f[idx] == global_cf[idx]:
            per2 += 1
    print float(per2) / len(global_f) * 100


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Calculate a dictionary scoring_distribution that represents
    an un-normalized distribution generated by performing the following
    process num_trials times:

    Generate a random permutation rand_y of the sequence seq_y
    using random.shuffle().
    Compute the maximum value score for the local alignment of
    seq_x and rand_y using the score matrix scoring_matrix.
    Increment the entry score in the dictionary scoring_distribution by one.

    Parameters
    ----------
    seq_x: str
    a sequence

    seq_y: str
    another sequence

    scoring_matrix: dict of dicts
    the scoring matrix

    num_trials: int
    the number of trials


    Returns
    -------
    scoring_distribution: dict
    a dictionary scoring_distribution that represents
    an un-normalized distribution
    """
    scoring_distribution = defaultdict(int)
    for _ in range(num_trials):
        rand_y = list(seq_y)
        shuffle(rand_y)
        align_mat = compute_alignment_matrix(seq_x, rand_y,
                                             scoring_matrix, False)
        alignment = compute_local_alignment(seq_x, rand_y,
                                            scoring_matrix, align_mat)
        score = alignment[0]
        scoring_distribution[score] += 1
    return scoring_distribution


def question4_plot():
    """
    Code for question 4
    """
    human = read_protein(HUMAN_EYELESS_URL)
    fruitfly = read_protein(FRUITFLY_EYELESS_URL)
    score_mat = read_scoring_matrix(PAM50_URL)
    dist = generate_null_distribution(human, fruitfly, score_mat, 1000)
    y = []
    for count in dist.itervalues():
        y.append(count / 1000.0)
    plt.bar(dist.keys(), y)
    plt.title("Normalized score distribution")
    plt.ylabel("Fractions of total trials")
    plt.xlabel("Scores of local alignments")
    plt.show()
    print dist


def question5():
    """
    Code for question 5
    """
    human = read_protein(HUMAN_EYELESS_URL)
    fruitfly = read_protein(FRUITFLY_EYELESS_URL)
    score_mat = read_scoring_matrix(PAM50_URL)
    dist = generate_null_distribution(human, fruitfly, score_mat, 1000)
    scores = []
    for score, count in dist.iteritems():
        scores.extend([score] * count)
    N = len(scores)
    mean = float(sum(scores)) / N
    std = math.sqrt(float(sum([(score - mean) ** 2 for score in scores])) / N)
    z_score = (875 - mean) / std
    print mean, std, z_score


def check_spelling(checked_word, dist, word_list):
    """
    Iterates through word_list and returns the set
    of all words that are within edit distance dist
    of the string checked_word.

    Parameters
    ----------
    checked_word: str
    the word to be checked

    dist: int
    the edit distance

    word_list: list
    a list of words


    Returns
    -------
    result: list
    the list of words that are within edit distance
    of the checked_word.
    """
    alphabets = "abcdefghijklmnopqrstuvwxyz"
    score_mat = build_scoring_matrix(alphabets, 2, 1, 0)
    result = []
    for word in word_list:
        align_mat = compute_alignment_matrix(checked_word, word,
                                             score_mat, True)
        score = compute_global_alignment(checked_word, word,
                                         score_mat, align_mat)[0]
        current_dist = len(checked_word) + len(word) - score
        if current_dist <= dist:
            result.append(word)
    return result


def question8():
    """
    Code for question 8
    """
    word_list = read_words(WORD_LIST_URL)
    print check_spelling('humble', 1, word_list)
    print check_spelling('firefly', 2, word_list)


if __name__ == '__main__':
    question8()
