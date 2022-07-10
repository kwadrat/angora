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
        seq = seq.replace(CODE_UNKNOWN, CODE_EMPTY)
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


def easy_guess(one_ls, line_size):
    delta = line_size - (sum(one_ls) + len(one_ls) - 1)
    pos_left = 0
    out_ls = []
    for one_size in one_ls:
        possible_width = one_size - delta
        if possible_width > 0:
            first_marked = pos_left + delta
            first_stopped = pos_left + one_size
            one_tpl = (first_marked, first_stopped)
            out_ls.append(one_tpl)
        pos_left += one_size  # Przeskocz za czarny ciąg
        pos_left += 1  # Przeskocz kratkę odstępu między czarnymi
    return out_ls


def near_border(first_by_border, cell_ls):
    out_ls = []
    black_detected = 0
    for nr in range(first_by_border):
        if black_detected and cell_ls[nr] != CODE_BLACK:
            out_ls.append(nr)
        if cell_ls[nr] == CODE_BLACK:
            black_detected = 1
    return out_ls


def gen_cl_hd(length):
    return ''.join(map(lambda a: str(a % 10), range(length)))


class WorkArea:
    def prepare_empty_data(self):
        '''
        WorkArea:
        '''
        self.int_table = []
        for row_nr in range(self.row_cnt):
            line_ls = []
            for col_nr in range(self.col_cnt):
                line_ls.append(CODE_UNKNOWN)
            self.int_table.append(line_ls)

    def assume_no_modification(self):
        '''
        WorkArea:
        '''
        self.is_modified = 0

    def __init__(self, rows, cols, verbose=0):
        '''
        WorkArea:
        '''
        self.rows = rows
        self.cols = cols
        self.row_cnt = len(self.rows)
        self.col_cnt = len(self.cols)
        self.verbose = verbose
        self.prepare_empty_data()
        self.assume_no_modification()

    def set_black(self, row_nr, col_nr):
        '''
        WorkArea:
        '''
        self.int_table[row_nr][col_nr] = CODE_BLACK
        self.is_modified += 1

    def slim_text(self, enable_axis=1):
        '''
        WorkArea:
        '''
        out_ls = []
        if enable_axis:
            col_header = gen_cl_hd(self.col_cnt)
            out_ls.append(col_header)
        for nr, row_data in enumerate(self.int_table):
            if enable_axis:
                trailing_txt = ' ' + str(nr)
            else:
                trailing_txt = ''
            unified_line = ''.join(row_data) + trailing_txt
            out_ls.append(unified_line)
        out_txt = '\n'.join(out_ls)
        return out_txt

    def read_from_file(self, file_name):
        '''
        WorkArea:
        '''
        fd = open(file_name)
        full_txt = fd.read()
        fd.close()
        all_lines = full_txt.splitlines()
        for row_nr in range(self.row_cnt):
            row_txt = all_lines[row_nr]
            for col_nr in range(self.col_cnt):
                self.int_table[row_nr][col_nr] = row_txt[col_nr]

    def save_to_file(self, file_name):
        '''
        WorkArea:
        '''
        full_txt = self.slim_text() + '\n'
        fd = open(file_name, 'w')
        fd.write(full_txt)
        fd.close()

    def small_margins_hint(self):
        '''
        WorkArea:
        Początkowo można zaczernić te kratki, które na pewno są
        zaczernione, bo jest na tyle dużo punktów w linii, że wystąpi
        zaczerniona część wspólna.
        '''
        for row_nr in range(self.row_cnt):
            easy_ls = easy_guess(self.rows[row_nr], self.col_cnt)
            for easy_start, easy_end in easy_ls:
                for col_nr in range(easy_start, easy_end):
                    self.set_black(row_nr, col_nr)
        for col_nr in range(self.col_cnt):
            easy_ls = easy_guess(self.cols[col_nr], self.row_cnt)
            for easy_start, easy_end in easy_ls:
                for row_nr in range(easy_start, easy_end):
                    self.set_black(row_nr, col_nr)

    def fill_from_each_border(self):
        '''
        WorkArea:
        '''
        for row_nr in range(self.row_cnt):
            len_ls = self.rows[row_nr]
            line_ls = self.int_table[row_nr]
            if 1:
                one_length = len_ls[0]
                one_text = ''.join(line_ls[:one_length])
                point_ls = near_border(one_length, one_text)
                if point_ls:
                    tmp_format = 'row_nr, one_length, one_text, point_ls'
                    print('EvalA: %s %s' % (tmp_format, eval(tmp_format)))
                for offset in point_ls:
                    col_nr = offset
                    self.set_black(row_nr, col_nr)
            if 1:
                one_length = len_ls[-1]
                one_text = ''.join(reversed(line_ls[-one_length:]))
                point_ls = near_border(one_length, one_text)
                if point_ls:
                    tmp_format = 'row_nr, one_length, one_text, point_ls'
                    print('EvalB: %s %s' % (tmp_format, eval(tmp_format)))
                for offset in point_ls:
                    col_nr = self.col_cnt - 1 - offset
                    self.set_black(row_nr, col_nr)
        for col_nr in range(self.col_cnt):
            len_ls = self.cols[col_nr]
            line_ls = list(map(lambda lbd_line: lbd_line[col_nr], self.int_table))
            if 1:
                one_length = len_ls[0]
                one_text = ''.join(line_ls[:one_length])
                point_ls = near_border(one_length, one_text)
                if point_ls:
                    tmp_format = 'col_nr, one_length, one_text, point_ls'
                    print('EvalC: %s %s' % (tmp_format, eval(tmp_format)))
                for offset in point_ls:
                    row_nr = offset
                    self.set_black(row_nr, col_nr)
            if 1:
                one_length = len_ls[-1]
                one_text = ''.join(reversed(line_ls[-one_length:]))
                point_ls = near_border(one_length, one_text)
                if point_ls:
                    tmp_format = 'col_nr, one_length, one_text, point_ls'
                    print('EvalD: %s %s' % (tmp_format, eval(tmp_format)))
                for offset in point_ls:
                    row_nr = self.row_cnt - 1 - offset
                    self.set_black(row_nr, col_nr)


def main():
    assert sum(map(sum, rows)) == sum(map(sum, cols))
    if 0:
        all_lines = []
        row_cnt = col_cnt = 0
        row_shadow = list(map(decode, all_lines))
        if 1:
            tmp_format = 'row_shadow'
            print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
        trn_lines = transpose(all_lines, row_cnt, col_cnt)
        col_shadow = list(map(decode, trn_lines))
        zip_check(row_shadow, rows, 'Rows')
        zip_check(col_shadow, cols, 'Cols')
    work_area = WorkArea(rows, cols)
    print('PlaceA %d' % work_area.is_modified)
    work_area.small_margins_hint()
    print('PlaceB %d' % work_area.is_modified)
    work_area.fill_from_each_border()
    print('PlaceC %d' % work_area.is_modified)
    work_area.fill_from_each_border()
    print('PlaceD %d' % work_area.is_modified)
    work_area.fill_from_each_border()
    print('PlaceE %d' % work_area.is_modified)
    if 1:
        out_txt = work_area.slim_text()
        print(out_txt)


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

    def test_moving_both_directions_to_limits(self):
        '''
        TestAngoraPuzzle:
        Funkcja zwraca listę [(początek, koniec), ...] elementów do wypełnienia
        Konwencja wyniku: Python range() lub inaczej C/for
        '''
        self.assertEqual(easy_guess([20], 20), [(0, 20)])
        self.assertEqual(easy_guess([19], 19), [(0, 19)])
        self.assertEqual(easy_guess([18], 19), [(1, 18)])
        self.assertEqual(easy_guess([17], 19), [(2, 17)])
        self.assertEqual(easy_guess([4, 5], 10), [(0, 4), (5, 10)])
        self.assertEqual(easy_guess([2, 5], 10), [(5, 8)])

    def test_by_border_fill_from_first_black(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(near_border(4, 'H......'), [1, 2, 3])
        self.assertEqual(near_border(4, '.......'), [])
        self.assertEqual(near_border(4, '.H.....'), [2, 3])
        self.assertEqual(near_border(5, '.H.....'), [2, 3, 4])
        self.assertEqual(near_border(5, '.H.H...'), [2, 4])

    def test_generating_column_heading(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(gen_cl_hd(2), '01')
        self.assertEqual(gen_cl_hd(3), '012')
