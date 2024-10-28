#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import dx_options
import ts_code
import fx_area
import wk_area
import eg_bag
import rn_info

import sys


def line_to_numbers(one_line):
    return list(map(int, one_line.split()))


def text_to_numbers(one_txt):
    all_lines = one_txt.splitlines()
    return list(map(line_to_numbers, all_lines))


rows = text_to_numbers(fx_area.rows)
cols = text_to_numbers(fx_area.cols)


def zip_check(row_shadow, rows, desc):
    row_stat = map(lambda a, b: eg_bag.is_inside(a, b), row_shadow, rows)
    eq_stat = map(lambda a, b: a == b, row_shadow, rows)
    for nr, (a, b, c, d) in enumerate(zip(row_shadow, rows, row_stat, eq_stat)):
        order_number = rn_info.green_message(str(nr + 1), d)
        print('%s %s %s %s' % (order_number, rn_info.red_message(c, not c), a, b))
    total_state = all(row_stat)
    total_eq = all(eq_stat)
    print('%s %s' % (rn_info.green_message(desc + ' total:', total_eq), rn_info.red_message(total_state, not total_state)))


def main(state_file, step_by_step, final_colors):
    r_sum = sum(map(sum, rows))
    c_sum = sum(map(sum, cols))
    assert r_sum == c_sum, '%d %d' % (r_sum, c_sum)
    work_a_area = wk_area.WorkArea(rows, cols)
    if step_by_step:
        work_a_area.ask_for_every_step()
    if state_file:
        work_a_area.read_from_file(state_file)
    work_a_area.small_margins_hint()
    prev_count = -1
    while 1:
        prev_count = work_a_area.modify_count
        work_a_area.fill_a_from_each_border()
        if work_a_area.modify_count > prev_count:
            work_a_area.display_state('a')
        else:
            break


def rc_dump(label, data_ls):
    a = list(map(lambda x: (sum(x[1]) + len(x[1]) - 1, x[0] + 1, x[1]), enumerate(data_ls)))
    a.sort(reverse=1)
    print(label)
    for one_tpl in a:
        print(one_tpl)


def rc_order():
    rc_dump('Rows', rows)
    rc_dump('Cols', cols)


if __name__ == '__main__':
    parser, opt_bag = dx_options.recognize_options()
    option_done = 0
    error_occured = 1
    if opt_bag.run_tests:
        error_occured = ts_code.perform_tests()
        option_done = 1
    if opt_bag.show_order:
        rc_order()
        error_occured = 0
        option_done = 1
    if opt_bag.guess_steps:
        main(opt_bag.state, opt_bag.step_by_step, opt_bag.final_colors)
        error_occured = 0
        option_done = 1
    if not option_done:
        parser.print_help()
    sys.exit(error_occured)
