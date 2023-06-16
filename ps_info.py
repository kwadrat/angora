#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest

import lb_cnst


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
