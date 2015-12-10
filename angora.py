#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

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

assert sum(map(sum, rows)) == sum(map(sum, cols))

all_lines = open('plansza.txt', 'rb').read().splitlines()

def decode(seq):
    if seq:
        result = map(len, seq.split())
    else:
        result = []
    return result

class TestAngoraPuzzle(unittest.TestCase):
    def test_angora_puzzle(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(decode(''), [])
        self.assertEqual(decode('H'), [1])
        self.assertEqual(decode('HH'), [2])
        self.assertEqual(decode('H H'), [1, 1])
