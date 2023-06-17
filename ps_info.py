#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest

import lb_cnst
import eg_bag


class PositionVault:
    def __init__(self, row_count, col_count):
        '''
        PositionVault:
        '''
        self.row_cnt = row_count
        self.col_cnt = col_count

    def prepare_empty_data(self):
        '''
        PositionVault:
        '''
        lcl_tbl = []
        for row_nr in range(self.row_cnt):
            line_ls = []
            for col_nr in range(self.col_cnt):
                line_ls.append(lb_cnst.CODE_UNKNOWN)
            lcl_tbl.append(line_ls)
        return lcl_tbl

    def each_row(self):
        '''
        PositionVault:
        '''
        return range(self.row_cnt)

    def each_col(self):
        '''
        PositionVault:
        '''
        return range(self.col_cnt)

    def col_header(self):
        '''
        PositionVault:
        '''
        return eg_bag.gen_cl_hd(self.col_cnt)

    def side_size(self, is_col):
        '''
        PositionVault:
        '''
        if is_col:
            item_len = self.col_cnt
        else:
            item_len = self.row_cnt
        return item_len

    def guess_in_row(self, inflicted_ls):
        '''
        PositionVault:
        '''
        return eg_bag.easy_guess(inflicted_ls, self.col_cnt)

    def guess_in_col(self, inflicted_ls):
        '''
        PositionVault:
        '''
        return eg_bag.easy_guess(inflicted_ls, self.row_cnt)


class TestPositionDetails(unittest.TestCase):
    def test_position_details(self):
        '''
        TestPositionDetails:
        '''
        obj = PositionVault(row_count=5, col_count=5)
        self.assertEqual(obj.row_cnt, 5)
        self.assertEqual(obj.col_cnt, 5)

    def test_initial_emtiness(self):
        '''
        TestPositionDetails:
        '''
        obj = PositionVault(row_count=2, col_count=2)
        self.assertEqual(obj.prepare_empty_data(), [['.', '.'], ['.', '.']])

    def test_each_of_dimension(self):
        '''
        TestPositionDetails:
        '''
        obj = PositionVault(row_count=3, col_count=2)
        self.assertEqual(list(obj.each_row()), [0, 1, 2])
        self.assertEqual(list(obj.each_col()), [0, 1])
        self.assertEqual(obj.col_header(), '12')
        self.assertEqual(obj.side_size(is_col=1), 2)
        self.assertEqual(obj.side_size(is_col=0), 3)

    def test_something_easy(self):
        '''
        TestPositionDetails:
        '''
        obj = PositionVault(row_count=30, col_count=30)
        self.assertEqual(obj.guess_in_row([8, 3, 1, 1, 3, 3]), [(6, 8)])
        self.assertEqual(obj.guess_in_col([9, 4, 7, 1, 1]), [(4, 9), (19, 22)])
