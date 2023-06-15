#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest

CODE_BLACK = 'H'
CODE_UNKNOWN = '.'
CODE_EMPTY = ' '


class TestConstants(unittest.TestCase):
    def test_constants(self):
        '''
        TestConstants:
        '''
        self.assertEqual(CODE_BLACK, 'H')
        self.assertEqual(CODE_UNKNOWN, '.')
        self.assertEqual(CODE_EMPTY, ' ')
