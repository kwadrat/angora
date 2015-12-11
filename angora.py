#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import itertools

rows = [
    [3],
    [1,3],
    [9],
    [5],
    [2],
    [1],
    [2],
    [3],
    [8],
    [9],
    [9],
    [12],
    [14],
    [5],
    [1,1],
    [1,1],
    [5],
    [2,1],
    [1],
    [2],
    ]

cols = [
    [0],
    [0],
    [0],
    [1],
    [1],
    [1],
    [1],
    [3,3],
    [1,2,6],
    [13,1],
    [5,5,1],
    [3,6,1],
    [6,1,1],
    [12],
    [6,1],
    [8],
    [3],
    [2],
    [2],
    [2],
    [1],
    [1],
    [1],
    [0],
    [0],
    ]

def decode(seq):
    if seq:
        result = map(len, seq.split())
    else:
        result = []
    return result

def inside(small, large):
    result = 0
    small_cnt = len(small)
    if small_cnt <= len(large):
        for sub_large in itertools.combinations(large, small_cnt):
            result = all(map(lambda x, y: x <= y, small, sub_large))
            if result:
                break
    return result

def transpose(all_lines, row_cnt, col_cnt):
    lines_count = len(all_lines)
    empty_line = ' ' * col_cnt
    trn_lines = []
    for j in xrange(col_cnt):
        trn_lines.append([])
    for i in xrange(row_cnt):
        if i < lines_count:
            tmp_line = all_lines[i]
            tmp_len = len(tmp_line)
            if tmp_len < col_cnt:
                tmp_line = tmp_line + ' ' * (col_cnt - tmp_len)
        else:
            tmp_line = empty_line
        for j in xrange(col_cnt):
            trn_lines[j].append(tmp_line[j])
    trn_lines = map(lambda x: ''.join(x), trn_lines)
    return trn_lines 

def main():
    assert sum(map(sum, rows)) == sum(map(sum, cols))
    all_lines = open('plansza.txt', 'rb').read().splitlines()
    row_cnt = len(rows)
    col_cnt = len(cols)
    tmp_format = 'row_cnt, col_cnt'; print 'Eval:', tmp_format, eval(tmp_format)
    row_shadow = map(decode, all_lines)
    tmp_format = 'row_shadow'; print 'Eval:', tmp_format, eval(tmp_format)
    trn_lines = transpose(all_lines, row_cnt, col_cnt)
    col_shadow = map(decode, trn_lines)
    tmp_format = 'col_shadow'; print 'Eval:', tmp_format, eval(tmp_format)

if __name__ == '__main__':
    main()

class TestAngoraPuzzle(unittest.TestCase):
    def test_angora_puzzle(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(decode(''), [])
        self.assertEqual(decode('H'), [1])
        self.assertEqual(decode('HH'), [2])
        self.assertEqual(decode('H H'), [1, 1])

    def test_one_in_another(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(inside([], []), 1)
        self.assertEqual(inside([1], []), 0)
        self.assertEqual(inside([2], [1]), 0)
        self.assertEqual(inside([1, 2], [2, 1]), 0)
        self.assertEqual(inside([2], [1, 1]), 0)
        self.assertEqual(inside([2], [1, 1]), 0)
        self.assertEqual(inside([2], [2, 1]), 1)
