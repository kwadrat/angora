#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse


def recognize_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--state',
                        default=None,
                        help='Initial state file name')
    parser.add_argument('--run_tests',
                        action='store_true', default=False,
                        help='Run tests')
    parser.add_argument('--show_order',
                        action='store_true', default=False,
                        help='Show items in descending order')
    parser.add_argument('--guess_steps',
                        action='store_true', default=False,
                        help='Perform iterative solving')
    parser.add_argument('--step_by_step',
                        action='store_true', default=False,
                        help='Detailed dump of each step')
    parser.add_argument('--final_colors',
                        action='store_true', default=False,
                        help='Final red/green check on rows and columns')
    opt_bag = parser.parse_args()
    return parser, opt_bag
