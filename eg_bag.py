#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import itertools

import lb_cnst


def lengths_of_trains(seq):
    '''
    Determine length of trains
    '''
    if seq:
        seq = seq.replace(lb_cnst.CODE_UNKNOWN, lb_cnst.CODE_EMPTY)
        result = list(map(len, seq.split()))
    else:
        result = []
    return result


def is_inside(small, large):
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


def from_border(first_by_border, cell_ls):
    black_ls = []
    space_ls = []
    if cell_ls[0] == lb_cnst.CODE_BLACK:
        for nr in range(first_by_border):
            if cell_ls[nr] == lb_cnst.CODE_UNKNOWN:
                black_ls.append(nr)
        if cell_ls[first_by_border] == lb_cnst.CODE_UNKNOWN:
            space_ls.append(first_by_border)
    return [black_ls, space_ls]


def transpose(all_lines, row_cnt, col_a_cnt):
    lines_count = len(all_lines)
    empty_line = ' ' * col_a_cnt
    trn_lines = []
    for j in range(col_a_cnt):
        trn_lines.append([])
    for i in range(row_cnt):
        if i < lines_count:
            tmp_line = all_lines[i]
            tmp_len = len(tmp_line)
            if tmp_len < col_a_cnt:
                tmp_line = tmp_line + ' ' * (col_a_cnt - tmp_len)
        else:
            tmp_line = empty_line
        for j in range(col_a_cnt):
            trn_lines[j].append(tmp_line[j])
    trn_lines = map(lambda x: ''.join(x), trn_lines)
    trn_lines = list(trn_lines)
    return trn_lines


def fill_ship_by_border(first_by_border, cell_ls):
    black_ls = []
    # Fill fields of ship that is touching border
    if cell_ls[first_by_border] == lb_cnst.CODE_EMPTY:
        if lb_cnst.CODE_BLACK in cell_ls[:first_by_border]:
            for nr in range(first_by_border):
                if cell_ls[nr] == lb_cnst.CODE_UNKNOWN:
                    black_ls.append(nr)
    return black_ls


def easy_guess(one_ls, line_size):
    pos_left = 0
    out_ls = []
    delta = line_size - (sum(one_ls) + len(one_ls) - 1)
    if delta >= 0:
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
    black_ls = []
    space_ls = []
    black_detected = 0
    offset = starting_point(first_by_border, cell_ls)
    if offset is not None:
        if offset:
            for i in range(offset):
                if cell_ls[i] == lb_cnst.CODE_UNKNOWN:
                    space_ls.append(i)
        else:
            if cell_ls[first_by_border] == lb_cnst.CODE_BLACK:
                for i in range(first_by_border):
                    if cell_ls[first_by_border + i] == lb_cnst.CODE_BLACK and cell_ls[i] == lb_cnst.CODE_UNKNOWN:
                        space_ls.append(i)
                    else:
                        break  # No more spaces to insert
        for nr in range(offset, offset + first_by_border):
            if black_detected and cell_ls[nr] != lb_cnst.CODE_BLACK:
                black_ls.append(nr)
            if cell_ls[nr] == lb_cnst.CODE_BLACK:
                black_detected = 1
    return [black_ls, space_ls]


def starting_point(ship_len, cell_ls):
    offset = 0
    look_for_place = 1
    while look_for_place:
        good_place_found = 1
        if offset + ship_len > len(cell_ls):
            offset = None  # Impossible, ship extends beyond legal domain
            look_for_place = 0
            continue
        if offset + ship_len < len(cell_ls) and cell_ls[offset + ship_len] == lb_cnst.CODE_BLACK:
            offset += 1
            good_place_found = 0
            continue
        for i in reversed(range(ship_len)):
            if cell_ls[offset + i] == lb_cnst.CODE_EMPTY:
                offset += i + 1
                good_place_found = 0
                break
        if good_place_found:
            look_for_place = 0
    return offset


def gen_cl_hd(length):
    return ''.join(map(lambda a: str(a % 10), range(1, length + 1)))


def always_in_shadow(one_set, ship_lngth):
    return list(range(max(one_set), min(one_set) + ship_lngth))


class TestBagFunctions(unittest.TestCase):
    def test_angora_puzzle(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(lengths_of_trains(''), [])
        self.assertEqual(lengths_of_trains('H'), [1])
        self.assertEqual(lengths_of_trains('HH'), [2])
        self.assertEqual(lengths_of_trains('H H'), [1, 1])
        self.assertEqual(lengths_of_trains('.'), [])

    def test_one_in_another(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(is_inside([], []), 1)
        self.assertEqual(is_inside([1], []), 0)
        self.assertEqual(is_inside([2], [1]), 0)
        self.assertEqual(is_inside([1, 2], [2, 1]), 0)
        self.assertEqual(is_inside([2], [1, 1]), 0)
        self.assertEqual(is_inside([2], [1, 1]), 0)
        self.assertEqual(is_inside([2], [2, 1]), 1)
        self.assertEqual(is_inside([], [2, 1]), 1)

    def test_exchange_rows_cols(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(transpose([], 0, 0), [])
        self.assertEqual(transpose([['a', 'b']], 1, 2), ['a', 'b'])
        self.assertEqual(transpose(['a', 'b'], 2, 1), ['ab'])
        self.assertEqual(transpose(['abc', 'xyz'], 2, 3), ['ax', 'by', 'cz'])
        self.assertEqual(transpose(['ax', 'by', 'cz'], 3, 2), ['abc', 'xyz'])

    def test_moving_both_directions_to_limits(self):
        '''
        TestBagFunctions:
        Funkcja zwraca listę [(początek, koniec), ...] elementów do wypełnienia
        Konwencja wyniku: Python range() lub inaczej C/for
        '''
        self.assertEqual(easy_guess([17], 15), [])
        self.assertEqual(easy_guess([20], 20), [(0, 20)])
        self.assertEqual(easy_guess([19], 19), [(0, 19)])
        self.assertEqual(easy_guess([18], 19), [(1, 18)])
        self.assertEqual(easy_guess([17], 19), [(2, 17)])
        self.assertEqual(easy_guess([4, 5], 10), [(0, 4), (5, 10)])
        self.assertEqual(easy_guess([2, 5], 10), [(5, 8)])

    def test_by_border_fill_from_first_black(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(near_border(4, 'H......'), [[1, 2, 3], []])
        self.assertEqual(near_border(4, '.......'), [[], []])
        self.assertEqual(near_border(4, '.H.....'), [[2, 3], []])
        self.assertEqual(near_border(5, '.H.....'), [[2, 3, 4], []])
        self.assertEqual(near_border(5, '.H.H...'), [[2, 4], []])
        self.assertEqual(near_border(5, ' H.H...'), [[2, 4, 5], []])
        self.assertEqual(near_border(5, '.. .H.......'), [[5, 6, 7], [0, 1]])
        self.assertEqual(near_border(3, '...H.......'), [[], [0]])
        self.assertEqual(near_border(3, '...HH......'), [[], [0, 1]])
        self.assertEqual(near_border(4, '...HH......'), [[], [0]])
        self.assertEqual(near_border(3, ' ..HH'), [[], [1]])
        self.assertEqual(near_border(2, ' ..HH'), [[], [1, 2]])
        self.assertEqual(starting_point(4, '    HHHH.'), 4)
        self.assertEqual(starting_point(5, '.. .H.......'), 3)
        self.assertEqual(starting_point(5, '...H.......'), 0)
        self.assertEqual(starting_point(3, ' ..HH'), 2)
        self.assertEqual(starting_point(2, ' ..HH'), 3)
        self.assertEqual(starting_point(4, ' .H.. '), 1)
        self.assertEqual(starting_point(1, ' .H.. '), 2)
        self.assertEqual(starting_point(2, ' .H.. '), 1)
        self.assertEqual(starting_point(3, ' .H.. '), 1)
        self.assertEqual(starting_point(4, ' ..H. '), 1)
        self.assertEqual(starting_point(2, ' ..H. '), 2)
        self.assertEqual(starting_point(10, '    ....HHHHHH. '), 4)
        self.assertEqual(starting_point(9, ' ..H. '), None)

    def test_ship_touches_border(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(from_border(4, '...HH......'), [[], []])
        self.assertEqual(from_border(4, 'H......'), [[1, 2, 3], [4]])
        self.assertEqual(from_border(5, 'H......'), [[1, 2, 3, 4], [5]])
        self.assertEqual(from_border(5, 'HH.....'), [[2, 3, 4], [5]])
        self.assertEqual(from_border(1, 'H..'), [[], [1]])

    def test_ship_is_finished_but_not_filled(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(fill_ship_by_border(2, '.H .'), [0])
        self.assertEqual(fill_ship_by_border(3, 'H.H .'), [1])
        self.assertEqual(fill_ship_by_border(3, '.H. .'), [0, 2])

    def test_generating_column_heading(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(gen_cl_hd(2), '12')
        self.assertEqual(gen_cl_hd(3), '123')

    def test_multi_shadowed_places(self):
        '''
        TestBagFunctions:
        '''
        self.assertEqual(always_in_shadow({0, 0}, 7), [0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(always_in_shadow({0, 0}, 6), [0, 1, 2, 3, 4, 5])
        self.assertEqual(always_in_shadow({0, 1}, 6), [1, 2, 3, 4, 5])
        self.assertEqual(always_in_shadow({1, 1}, 6), [1, 2, 3, 4, 5, 6])
        self.assertEqual(always_in_shadow({0, 8}, 6), [])
        self.assertEqual(always_in_shadow({1, 6}, 7), [6, 7])
        self.assertEqual(always_in_shadow({2, 6}, 7), [6, 7, 8])
