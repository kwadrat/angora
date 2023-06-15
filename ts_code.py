#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest

import im_chisel
import eg_bag
import lb_cnst
import wn_box


fast_test_ls = [
    eg_bag.TestBagFunctions,
    lb_cnst.TestConstants,
    im_chisel.TestChiselTool,
    wn_box.TestBoxFunctions,
    ]


def summary_status(suite):
    text_test_result = unittest.TextTestRunner().run(suite)
    return not not (text_test_result.failures or text_test_result.errors)


def perform_tests():
    suite = unittest.TestSuite()
    for one_test in fast_test_ls:
        suite.addTest(unittest.makeSuite(one_test))
    return summary_status(suite)
