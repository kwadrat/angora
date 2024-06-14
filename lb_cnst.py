#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest

CODE_BLACK = 'H'  # Here is a black point
CODE_UNKNOWN = '.'  # It can be a black point, it can be space - not yet decided
CODE_EMPTY = ' '  # Here is a space (no black point)


class TestConstants(unittest.TestCase):
    def test_constants(self):
        '''
        TestConstants:
        '''
        self.assertEqual(CODE_BLACK, 'H')
        self.assertEqual(CODE_UNKNOWN, '.')
        self.assertEqual(CODE_EMPTY, ' ')
