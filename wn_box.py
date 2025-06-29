#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest

import im_chisel


class WoodenBox:
    def __init__(self, len_ls):
        '''
        WoodenBox:
        '''
        self.wood_ls = list(map(lambda x: im_chisel.ItemChisel(x[1], x[0]), enumerate(len_ls)))
        for i in range(len(self.wood_ls) - 1):
            next_in_chain = self.wood_ls[i + 1]
            self.wood_ls[i].set_next(next_in_chain)

    def text_for_all(self, cell_txt):
        '''
        WoodenBox:
        '''
        if len(self.wood_ls) > 0:
            for one_ship in self.wood_ls:
                one_ship.apply_new_text(cell_txt)
            self.wood_ls[0].multi_rotor_pos(0)

    def next_full_pos(self):
        '''
        WoodenBox:
        '''
        if self.wood_ls:
            result = self.wood_ls[0].next_head_pos()
        else:
            result = None
        return result


def possible_problem(ground_txt, ship_ls):
    wd_bx = WoodenBox(ship_ls)
    wd_bx.text_for_all(ground_txt)
    error_occured = wd_bx.next_full_pos() is None
    if error_occured:
        tmp_format = 'ground_txt, ship_ls'
        print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
    return error_occured


class TestBoxFunctions(unittest.TestCase):
    def test_b(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([1, 1])
        obj.text_for_all('. .')
        self.assertEqual(obj.next_full_pos(), [0, 2])
        self.assertEqual(obj.next_full_pos(), None)
        obj.text_for_all(' . . . ')
        self.assertEqual(obj.next_full_pos(), [1, 3])
        self.assertEqual(obj.next_full_pos(), [1, 5])
        self.assertEqual(obj.next_full_pos(), [3, 5])

    def test_c(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([6, 4, 1, 3, 1])
        obj.text_for_all('.HHHHH..HHHH...HHH..')
        self.assertEqual(obj.next_full_pos(), [0, 8, 13, 15, 19])
        self.assertEqual(obj.next_full_pos(), [1, 8, 13, 15, 19])
        self.assertEqual(obj.next_full_pos(), None)

    def test_d(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([4, 1, 1, 1, 1])
        obj.text_for_all('...........H.H.H.H..')
        self.assertEqual(obj.next_full_pos(), [0, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [1, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [2, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [3, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [4, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [5, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [6, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [8, 13, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(), None)

    def test_e(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([4, 2, 3, 1, 1, 1])
        obj.text_for_all(' HHHH .......... ...')
        self.assertEqual(obj.next_full_pos(), [1, 6, 9, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [1, 6, 9, 13, 15, 18])
        self.assertEqual(obj.next_full_pos(), [1, 6, 9, 13, 15, 19])
        self.assertEqual(obj.next_full_pos(), [1, 6, 9, 13, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 6, 9, 14, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 6, 9, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 6, 10, 14, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 6, 10, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 6, 11, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 7, 10, 14, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 7, 10, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 7, 11, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(), [1, 8, 11, 15, 17, 19])

    def test_f(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([3, 3, 3, 2])
        obj.text_for_all(' .HH ... HHH HHH  HH')
        self.assertEqual(obj.next_full_pos(), [1, 9, 13, 18])
        self.assertEqual(obj.next_full_pos(), None)

    def test_g(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([4, 1, 1, 1, 1])
        obj.text_for_all(' .HHH..    H H H H  ')
        self.assertEqual(obj.next_full_pos(), [1, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [2, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), None)

    def test_h(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([])
        obj.text_for_all(' ')
        self.assertEqual(obj.next_full_pos(), None)

    def test_i(self):
        '''
        TestBoxFunctions:
        '''
        obj = WoodenBox([2, 2])
        one_line = '....H ..'
        obj.text_for_all(one_line)
        self.assertEqual(obj.next_full_pos(), [0, 3])
        self.assertEqual(obj.next_full_pos(), [3, 6])
        self.assertEqual(obj.next_full_pos(), None)
