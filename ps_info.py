#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest


class PositionVault:
    def __init__(self, row_count, col_count):
        '''
        PositionVault:
        '''
        self.row_cnt = row_count
        self.col_cnt = col_count


class TestPositionDetails(unittest.TestCase):
    def test_position_details(self):
        '''
        TestPositionDetails:
        '''
        obj = PositionVault(row_count=5, col_count=5)
        self.assertEqual(obj.row_cnt, 5)
        self.assertEqual(obj.col_cnt, 5)
