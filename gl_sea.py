#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import fx_area


def line_to_numbers(one_line):
    return list(map(int, one_line.split()))


def text_to_numbers(one_txt):
    all_lines = one_txt.splitlines()
    return list(map(line_to_numbers, all_lines))


g_rows = text_to_numbers(fx_area.rows)
g_cols = text_to_numbers(fx_area.cols)


def rc_dump(label, data_ls):
    a = list(map(lambda x: (sum(x[1]) + len(x[1]) - 1, x[0] + 1, x[1]), enumerate(data_ls)))
    a.sort(reverse=1)
    print(label)
    for one_tpl in a:
        print(one_tpl)


def rc_order():
    rc_dump('Rows', g_rows)
    rc_dump('Cols', g_cols)
