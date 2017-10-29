# -*- coding: utf-8 -*-

import jieba
import time
import re

STOP_WORDS = ["—", "】", "【", "/", "。", "\n", ".", "的", "一", "不", "在", "人", "有", "是", "为", "以", "于", "上", "他",
              "而", "后", "之", "来", "及", "了", "因", "下", "可", "到", "由", "这", "与", "也", "此", "但", "并", "个", "其",
              "已", "无", "小", "我", "们", "起", "最", "再", "今", "去", "好", "只", "又", "或", "很", "亦", "某", "把", "那",
              "你", "乃", "它", "要", "将", "应", "位", "新", "两", "中", "更", "我们", "自己", "没有", "“", "”", "，", "(", ")",
              "", "-", ":", "％", "#", "《", "》", "@", "；", "）", "（", "、", "？", "：", "...", "\""]


# Determine whether it is a combination of Numbers or letters
def judge_number_or_letter(s):
    # Judge s is int number
    if s.isdigit():
        return True

    # Judge s is float number
    items = s.split('.')
    if len(items) == 2 and items[0].isdigit() and items[1].isdigit():
        return True

    # Judge s is the combination of numbers and letters
    pattern = re.compile('\w+', re.A)
    result = pattern.match(s)
    if result:
        return True
    else:
        return False


# Read the data file to cut the original to words
class DataProcess(object):
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__class_data_num = {'1': 0, '2': 0, '3': 0}
        self.__category_one_words = []
        self.__category_two_words = []
        self.__category_three_words = []
        self.__total_data_num = 0

    def read_file_to_words(self):
        with open(self.__file_path, 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                line = f.readline()
                if line:
                    self.__total_data_num += 1
                    line = line.split(' ')
                    if int(line[0]) == 1:
                        self.__class_data_num['1'] += 1
                        items = ' '.join(jieba.cut(line[1]))
                        items = items.split(' ')
                        self.__category_one_words.append(list(set(items)))
                    if int(line[0]) == 2:
                        self.__class_data_num['2'] += 1
                        items = ' '.join(jieba.cut(line[1]))
                        items = items.split(' ')
                        self.__category_two_words.append(list(set(items)))
                    if int(line[0]) == 3:
                        self.__class_data_num['3'] += 1
                        items = ' '.join(jieba.cut(line[1]))
                        items = items.split(' ')
                        self.__category_three_words.append(list(set(items)))
                else:
                    break

    def process_category(self):
        category_one_words = []
        category_two_words = []
        category_three_words = []
        # and not word.isdigit() and not word.isalpha() and not word.isalnum()
        for item1 in self.__category_one_words:
            words = []
            for word in item1:
                if word not in STOP_WORDS and not judge_number_or_letter(word):
                    words.append(word)
            category_one_words.append(words)

        for item2 in self.__category_two_words:
            words = []
            for word in item2:
                if word not in STOP_WORDS and not judge_number_or_letter(word):
                    words.append(word)
            category_two_words.append(words)

        for item3 in self.__category_three_words:
            words = []
            for word in item3:
                if word not in STOP_WORDS and not judge_number_or_letter(word):
                    words.append(word)
            category_three_words.append(words)

        self.__category_one_words = category_one_words
        self.__category_two_words = category_two_words
        self.__category_three_words = category_three_words

    @property
    def class_data_num(self):
        return self.__class_data_num

    @property
    def category_one_words(self):
        return self.__category_one_words

    @property
    def category_two_words(self):
        return self.__category_two_words

    @property
    def category_three_words(self):
        return self.__category_three_words

    @property
    def total_data_num(self):
        return self.__total_data_num

