# -*- coding: utf-8 -*-

import jieba
from functools import reduce
from naive_bayes_classify.util.data_process import *

CATEGORY_ITEM = {'1': '体育', '2': '军事', '3': '经济社会'}

TEST_FILE_PATH = '../data/test.txt'
TRAIN_FILE_PATH = '../data/data.txt'

CATEGORY_DATA = []


# Deal with the data to words
def deal_data(file_path):
    global CATEGORY_DATA
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        while True:
            line = f.readline()
            if line:
                lines = line.split(' ')
                if len(lines) > 2:
                    correct_str = reduce(lambda x, y: x + y, lines[1:])
                else:
                    correct_str = lines[1]
                items = ' '.join(jieba.cut(correct_str))
                items = items.split(' ')
                CATEGORY_DATA.append(list(set(items)))
            else:
                break
    data = []
    for item in CATEGORY_DATA:
        words = []
        for word in item:
            if word not in STOP_WORDS and not judge_number_or_letter(word):
                words.append(word)
        data.append(words)

    CATEGORY_DATA = data


# Calculate the probability of P(ci) and P(xi|ci)

def calculate_prob():
    train_data = DataProcess(TRAIN_FILE_PATH)
    train_data.read_file_to_words()
    train_data.process_category()

    deal_data(TEST_FILE_PATH)
    category_one_words = train_data.category_one_words
    category_two_words = train_data.category_two_words
    category_three_words = train_data.category_three_words
    total_words_num = 0
    # calculate the sum of train data
    for item1 in category_one_words:
        total_words_num += len(item1)
    for item2 in category_two_words:
        total_words_num += len(item2)
    for item3 in category_three_words:
        total_words_num += len(item3)

    # calculate the P(ci)
    class_one_pro = train_data.class_data_num['1'] / train_data.total_data_num
    class_two_pro = train_data.class_data_num['2'] / train_data.total_data_num
    class_three_pro = train_data.class_data_num['3'] / train_data.total_data_num

    # calculate the P(xi|c1))
    print('In processing...')
    for category in CATEGORY_DATA:
        prob_one = 1
        prob_two = 1
        prob_three = 1

        for word in category:

            word_in_category_one_num = 0
            word_in_category_two_num = 0
            word_in_category_three_num = 0

            for item in category_one_words:
                if word in item:
                    word_in_category_one_num += 1
            p1 = (word_in_category_one_num + 1) / (train_data.class_data_num['1'] + total_words_num)
            prob_one = prob_one * p1

            for item in category_two_words:
                if word in item:
                    word_in_category_two_num += 1
            p2 = (word_in_category_two_num + 1) / (train_data.class_data_num['2'] + total_words_num)
            prob_two = prob_two * p2

            for item in category_three_words:
                if word in item:
                    word_in_category_three_num += 1
            p3 = (word_in_category_three_num + 1) / (train_data.class_data_num['3'] + total_words_num)
            prob_three = prob_three * p3

        probs = [prob_one * class_one_pro, prob_two * class_two_pro, prob_three * class_three_pro]
        category_index = probs.index(max(probs))
        print('The news belong to category: ' + '{}'.format(CATEGORY_ITEM[str(category_index + 1)]))


if __name__ == '__main__':
    start = time.time()
    calculate_prob()
    end = time.time()
    print('Total run time: %.4f' % (end - start))
