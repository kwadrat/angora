#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
python -m unittest angora; red_green_bar.py $? $COLUMNS
'''

import sys
import unittest
import itertools

rows = '''\
3 1 1 2
3 4 1
2 1 6
2 6 4
3 8
3 2 7
1 1 1 7
1 4 7
1 6
5 3 7
5 1 3
6 4 1 3 1
4 1 1 1 1
1 3 1 1 1 1
3 3 3
3 2 2 1 1 2
5 2 1 1
3 1 1 3
3 1 2 1 1
4 2 3 1 1 1
'''

cols = '''\
2 2 4
4 3 3 1
4 4 6
4 4
3 4 4
3 2 1
5 1 1 2
5 1 1
1 1 5 1
4 1 1 1 1 2 1
3 3 3 2
1 1 9
3 1
8 5 2
8 1
15 1
8
10 1
2 6 1 1
1 3 1 1 1 5
'''

CODE_BLACK = 'H'
CODE_UNKNOWN = '.'
CODE_EMPTY = ' '


def line_to_numbers(one_line):
    return list(map(int, one_line.split()))


def text_to_numbers(one_txt):
    all_lines = one_txt.splitlines()
    return list(map(line_to_numbers, all_lines))


rows = text_to_numbers(rows)
cols = text_to_numbers(cols)

ZnakEscape = chr(27)


def color_message(napis, paint, color):
    if paint:
        result = '%(escape)s[%(color)sm%(napis)s%(escape)s[0m' % {
            'escape': ZnakEscape,
            'napis': napis,
            'color': color,
            }
    else:
        result = napis
    return result


def green_message(napis, paint):
    return color_message(napis, paint, '32')


def red_message(napis, paint):
    return color_message(napis, paint, '31')


def decode(seq):
    '''
    Count number of marks (H letter)
    '''
    if seq:
        seq = seq.replace('.', ' ')
        result = list(map(len, seq.split()))
    else:
        result = []
    return result


def inside(small, large):
    '''
    Shorter subsequence can be inside large sequence
    '''
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
    for j in range(col_cnt):
        trn_lines.append([])
    for i in range(row_cnt):
        if i < lines_count:
            tmp_line = all_lines[i]
            tmp_len = len(tmp_line)
            if tmp_len < col_cnt:
                tmp_line = tmp_line + ' ' * (col_cnt - tmp_len)
        else:
            tmp_line = empty_line
        for j in range(col_cnt):
            trn_lines[j].append(tmp_line[j])
    trn_lines = map(lambda x: ''.join(x), trn_lines)
    trn_lines = list(trn_lines)
    return trn_lines


def zip_check(row_shadow, rows, desc):
    row_stat = map(lambda a, b: inside(a, b), row_shadow, rows)
    eq_stat = map(lambda a, b: a == b, row_shadow, rows)
    for nr, (a, b, c, d) in enumerate(zip(row_shadow, rows, row_stat, eq_stat)):
        order_number = green_message(str(nr + 1), d)
        print('%s %s %s %s' % (order_number, red_message(c, not c), a, b))
    total_state = all(row_stat)
    total_eq = all(eq_stat)
    print('%s %s' % (green_message(desc + ' total:', total_eq), red_message(total_state, not total_state)))


def main():
    assert sum(map(sum, rows)) == sum(map(sum, cols))
    full_txt = open('plansza.txt').read()
    all_lines = full_txt.splitlines()
    row_cnt = len(rows)
    col_cnt = len(cols)
    row_shadow = map(decode, all_lines)
    trn_lines = transpose(all_lines, row_cnt, col_cnt)
    col_shadow = map(decode, trn_lines)
    zip_check(row_shadow, rows, 'Rows')
    zip_check(col_shadow, cols, 'Cols')


def rc_dump(label, data_ls):
    a = list(map(lambda x: (sum(x[1]) + len(x[1]) - 1, x[0] + 1, x[1]), enumerate(data_ls)))
    a.sort(reverse=1)
    print(label)
    for one_tpl in a:
        print(one_tpl)


def rc_order():
    rc_dump('Rows', rows)
    rc_dump('Cols', cols)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'order':
        rc_order()
    else:
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
        self.assertEqual(decode('.'), [])

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

    def test_constants(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(CODE_BLACK, 'H')
        self.assertEqual(CODE_UNKNOWN, '.')
        self.assertEqual(CODE_EMPTY, ' ')
