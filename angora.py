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

ZnakEscape = chr(27)

def red_message(napis, paint):
    if paint:
        result = '%(escape)s[31m%(napis)s%(escape)s[0m' % { 'escape': ZnakEscape, 'napis': napis }
    else:
        result = napis
    return result

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

def zip_check(row_shadow, rows, desc):
    row_stat = map(lambda a, b: inside(a, b), row_shadow, rows)
    for nr, (a, b, c) in enumerate(zip(row_stat, row_shadow, rows)):
        print nr + 1, red_message(a, not a), b, c
    total_state = all(row_stat)
    print desc, 'total:', red_message(total_state, not total_state)

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
    zip_check(row_shadow, rows, 'Rows')
    zip_check(col_shadow, cols, 'Cols')

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
        self.assertEqual(inside([], [2, 1]), 1)

    def test_exchange_rows_cols(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(transpose([], 0, 0), [])
        self.assertEqual(transpose([['a', 'b']], 1, 2), ['a', 'b'])
        self.assertEqual(transpose(['a', 'b'], 2, 1), ['ab'])
        self.assertEqual(transpose(['abc', 'xyz'], 2, 3), ['ax', 'by', 'cz'])
        self.assertEqual(transpose(['ax', 'by', 'cz'], 3, 2), ['abc', 'xyz'])
