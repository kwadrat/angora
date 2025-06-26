#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import lb_cnst
import eg_bag
import wn_box
import ps_info
import rn_info


def cell_to_numbers(one_line):
    return list(map(len, ''.join(one_line).strip().split()))


def compare_with_colors(one_label, expected_ls, guess_ls):
    difference_occured = 0
    label_flag = 1
    for nr, (a, b) in enumerate(zip(expected_ls, guess_ls), 1):
        if a != b:
            if label_flag:
                print(one_label)
                label_flag = 0
            print(nr)
            print(rn_info.green_message(str(a), 1))
            print(rn_info.red_message(str(b), 1))
            difference_occured = 1
    return difference_occured


class WorkArea:
    def ask_for_every_step(self):
        '''
        WorkArea:
        '''
        self.enable_stepping = 1

    def assume_no_modification(self):
        '''
        WorkArea:
        '''
        self.modify_count = 0

    def __repr__(self):
        '''
        WorkArea:
        '''
        return 'WorkArea(col=%d, end=%d)' % (self.is_col, self.is_end)

    def __init__(self, p_rows, p_cols, verbose=0):
        '''
        WorkArea:
        '''
        self.enable_stepping = 0
        self.a_rows = p_rows
        self.a_cols = p_cols
        self.pos_dtls = ps_info.PositionVault(len(self.a_rows), len(self.a_cols))
        self.verbose = verbose
        self.int_table = self.pos_dtls.prepare_empty_data()
        self.exp_table = None
        self.assume_no_modification()

    def slim_text(self, enable_axis=1):
        '''
        WorkArea:
        '''
        out_ls = []
        if enable_axis:
            col_header = self.pos_dtls.col_header()
            out_ls.append(col_header)
        for nr, row_data in enumerate(self.int_table):
            if enable_axis:
                trailing_txt = ' ' + str(nr + 1)
            else:
                trailing_txt = ''
            unified_line = ''.join(row_data) + trailing_txt
            out_ls.append(unified_line)
        out_txt = '\n'.join(out_ls)
        return out_txt

    def save_to_file(self, file_name, enable_axis=0):
        '''
        WorkArea:
        '''
        full_txt = self.slim_text(enable_axis) + '\n'
        fd = open(file_name, 'w')
        fd.write(full_txt)
        fd.close()

    def get_a_details(self, item_nr, is_a_col, is_a_end=0):
        '''
        WorkArea:
        '''
        if is_a_col:
            line_ls = list(map(lambda lbd_line: lbd_line[item_nr], self.int_table))
        else:
            line_ls = self.int_table[item_nr]
        if is_a_end:
            line_ls = reversed(line_ls)
        return ''.join(line_ls)

    def display_state(self, label):
        '''
        WorkArea:
        '''
        print('Place %s %d' % (label, self.modify_count))
        print(self.slim_text())

    def temporary_condition(self, row_nr, col_nr):
        '''
        WorkArea:
        '''
        row_txt = self.get_a_details(row_nr, is_a_col=0)
        if wn_box.possible_problem(row_txt, self.a_rows[row_nr]):
            raise RuntimeError('row = %d (offset %d)' % (row_nr, col_nr))
        else:
            col_txt = self.get_a_details(col_nr, is_a_col=1)
            if wn_box.possible_problem(col_txt, self.a_cols[col_nr]):
                raise RuntimeError('column = %d (offset %d)' % (col_nr, row_nr))

    def single_set(self, row_nr, col_nr, one_symbol):
        '''
        WorkArea:
        '''
        if self.exp_table is not None:
            if self.exp_table[row_nr][col_nr] != one_symbol:
                self.display_state('b')
                print('row_nr %d col_nr %d one_symbol %s' % (row_nr + 1, col_nr + 1, repr(one_symbol)))
                raise RuntimeError('Discrepancy detected')
        self.int_table[row_nr][col_nr] = one_symbol
        if self.enable_stepping:
            self.save_to_file('g%03d' % self.modify_count, enable_axis=1)
        self.temporary_condition(row_nr, col_nr)
        self.modify_count += 1

    def set_black(self, row_nr, col_nr):
        '''
        WorkArea:
        '''
        if self.int_table[row_nr][col_nr] != lb_cnst.CODE_BLACK:
            self.single_set(row_nr, col_nr, lb_cnst.CODE_BLACK)

    def set_space(self, row_nr, col_nr):
        '''
        WorkArea:
        '''
        current_value = self.int_table[row_nr][col_nr]
        if current_value == lb_cnst.CODE_UNKNOWN:
            self.single_set(row_nr, col_nr, lb_cnst.CODE_EMPTY)
        elif current_value != lb_cnst.CODE_EMPTY:
            one_msg = "Why cleaning this place [%d, %d, '%s']?" % (row_nr, col_nr, current_value)
            raise RuntimeError(one_msg)

    def table_from_file(self, prm_table, file_name):
        '''
        WorkArea:
        '''
        fd = open(file_name)
        full_txt = fd.read()
        fd.close()
        all_lines = full_txt.splitlines()
        for row_nr in self.pos_dtls.each_row():
            row_txt = all_lines[row_nr]
            for col_nr in self.pos_dtls.each_col():
                prm_table[row_nr][col_nr] = row_txt[col_nr]

    def read_from_file(self, state_file, expected_solution):
        '''
        WorkArea:
        '''
        if state_file:
            self.table_from_file(self.int_table, state_file)
        if expected_solution:
            self.exp_table = self.pos_dtls.prepare_empty_data()
            self.table_from_file(self.exp_table, expected_solution)

    def helper_len(self):
        '''
        WorkArea:
        '''
        return self.pos_dtls.side_size(self.is_col)

    def helper_line_len(self):
        '''
        WorkArea:
        '''
        return self.pos_dtls.side_size(not self.is_col)

    def get_sketch(self, item_nr):
        '''
        WorkArea:
        Show numbers for row or column.
        This list can be empty - all places are spaces.
        '''
        if self.is_col:
            len_ls = self.a_cols[item_nr]
        else:
            len_ls = self.a_rows[item_nr]
        return len_ls

    def get_details(self, item_nr):
        '''
        WorkArea:
        '''
        return self.get_a_details(item_nr, self.is_col, self.is_end)

    def helper_position(self, item_len, item_nr, offset):
        '''
        WorkArea:
        '''
        if self.is_end:
            item_pos = item_len - 1 - offset
        else:
            item_pos = offset
        if self.is_col:
            row_nr = item_pos
            col_nr = item_nr
        else:
            row_nr = item_nr
            col_nr = item_pos
        return row_nr, col_nr

    def helper_black(self, item_len, item_nr, offset):
        '''
        WorkArea:
        '''
        row_nr, col_nr = self.helper_position(item_len, item_nr, offset)
        self.set_black(row_nr, col_nr)

    def helper_space(self, item_len, item_nr, offset):
        '''
        WorkArea:
        '''
        row_nr, col_nr = self.helper_position(item_len, item_nr, offset)
        self.set_space(row_nr, col_nr)

    def small_margins_hint(self):
        '''
        WorkArea:
        Początkowo można zaczernić te kratki, które na pewno są
        zaczernione, bo jest na tyle dużo punktów w linii, że wystąpi
        zaczerniona część wspólna.
        '''
        for row_nr in self.pos_dtls.each_row():
            easy_ls = self.pos_dtls.guess_in_row(self.a_rows[row_nr])
            for easy_start, easy_end in easy_ls:
                for col_nr in range(easy_start, easy_end):
                    self.set_black(row_nr, col_nr)
        for col_nr in self.pos_dtls.each_col():
            easy_ls = self.pos_dtls.guess_in_col(self.a_cols[col_nr])
            for easy_start, easy_end in easy_ls:
                for row_nr in range(easy_start, easy_end):
                    self.set_black(row_nr, col_nr)

    def fill_b_from_each_border(self):
        '''
        WorkArea:
        '''
        frequent_update = 1
        item_cnt = self.helper_len()
        line_len = self.helper_line_len()
        for item_nr in range(item_cnt):
            len_ls = self.get_sketch(item_nr)
            if len_ls:
                # For one (or more) numbers for this line
                one_text = self.get_details(item_nr)
                if self.is_end:
                    one_length = len_ls[-1]
                else:
                    one_length = len_ls[0]
                black_ls, space_ls = eg_bag.near_border(one_length, one_text)
                for offset in black_ls:
                    self.helper_black(line_len, item_nr, offset)
                for offset in space_ls:
                    self.helper_space(line_len, item_nr, offset)
                if frequent_update:
                    one_text = self.get_details(item_nr)
                black_ls, space_ls = eg_bag.from_border(one_length, one_text)
                for offset in black_ls:
                    self.helper_black(line_len, item_nr, offset)
                for offset in space_ls:
                    self.helper_space(line_len, item_nr, offset)
                if frequent_update:
                    one_text = self.get_details(item_nr)
                black_ls = eg_bag.fill_ship_by_border(one_length, one_text)
                for offset in black_ls:
                    self.helper_black(line_len, item_nr, offset)
            else:
                # There is no numbers in this line - all fields should be empty
                space_ls = eg_bag.all_spaces(line_len)
                for offset in space_ls:
                    self.helper_space(line_len, item_nr, offset)

    def place_ship_with_water(self, item_len, item_nr, ship_start, ship_len):
        '''
        WorkArea:
        '''
        if ship_start > 0:
            self.helper_space(item_len, item_nr, ship_start - 1)
        for offset in range(ship_len):
            self.helper_black(item_len, item_nr, ship_start + offset)
        if ship_start + ship_len < item_len:
            self.helper_space(item_len, item_nr, ship_start + ship_len)

    def space_in_every_case(self, item_len, item_nr, len_ls, one_text, poss_ls):
        '''
        WorkArea:
        '''
        if one_text.count(lb_cnst.CODE_UNKNOWN) > 0:
            always_space_ls = [1] * len(one_text)
            for one_sol in poss_ls:
                for one_len, ship_start in zip(len_ls, one_sol):
                    for i in range(ship_start, ship_start + one_len):
                        always_space_ls[i] = 0
            for offset, one_char in enumerate(one_text):
                if one_char == lb_cnst.CODE_UNKNOWN and always_space_ls[offset]:
                    self.helper_space(item_len, item_nr, offset)

    def fill_what_can_be_deduced(self, item_len, item_nr, len_ls, one_text, poss_ls):
        '''
        WorkArea:
        '''
        for ship_nr, ship_len in enumerate(len_ls):
            one_set = set(map(lambda one_sol: one_sol[ship_nr], poss_ls))
            fully_in_shadow_ls = eg_bag.always_in_shadow(one_set, ship_len)
            for one_item in fully_in_shadow_ls:
                self.helper_black(item_len, item_nr, one_item)

    def analyze_possibilities(self, item_len, item_nr, len_ls, one_text):
        '''
        WorkArea:
        '''
        poss_ls = []
        wooden_box = wn_box.WoodenBox(len_ls)
        wooden_box.text_for_all(one_text)
        while 1:
            new_one = wooden_box.next_full_pos()
            if new_one is None:
                break
            else:
                poss_ls.append(new_one)
        self.fill_what_can_be_deduced(item_len, item_nr, len_ls, one_text, poss_ls)
        self.space_in_every_case(item_len, item_nr, len_ls, one_text, poss_ls)

    def clean_fully_populated(self, item_len, item_nr, len_ls, one_text):
        '''
        WorkArea:
        '''
        if lb_cnst.CODE_UNKNOWN in one_text and sum(len_ls) == one_text.count(lb_cnst.CODE_BLACK):
            for offset, one_char in enumerate(one_text):
                if one_char == lb_cnst.CODE_UNKNOWN:
                    self.helper_space(item_len, item_nr, offset)

    def fill_c_for_both(self):
        '''
        WorkArea:
        '''
        self.is_end = 0
        item_len = self.helper_len()
        for item_nr in range(item_len):
            len_ls = self.get_sketch(item_nr)
            one_text = self.get_details(item_nr)
            if len(len_ls) == 1:
                # Fill gaps
                offset_ls = eg_bag.first_to_last(one_text)
                for offset in offset_ls:
                    if one_text[offset] is lb_cnst.CODE_UNKNOWN:
                        self.helper_black(item_len, item_nr, offset)
            self.analyze_possibilities(item_len, item_nr, len_ls, one_text)
            self.clean_fully_populated(item_len, item_nr, len_ls, one_text)

    def fill_a_from_each_border(self):
        '''
        WorkArea:
        '''
        for self.is_col in range(2):
            for self.is_end in range(2):
                self.fill_b_from_each_border()
            self.fill_c_for_both()

    def enlight_final(self, one_table):
        '''
        WorkArea:
        '''
        error_occured = 0
        tmp_rows = list(map(cell_to_numbers, one_table))
        tmp_error = compare_with_colors('Rows:', self.a_rows, tmp_rows)
        if tmp_error:
            error_occured = tmp_error
        tmp_cols = list(map(cell_to_numbers, list(zip(* one_table))))
        tmp_error = compare_with_colors('Cols:', self.a_cols, tmp_cols)
        if tmp_error:
            error_occured = tmp_error
        return error_occured

    def general_processing(self):
        '''
        WorkArea:
        '''
        error_occured = 0
        prev_count = -1
        while 1:
            prev_count = self.modify_count
            self.fill_a_from_each_border()
            if self.modify_count > prev_count:
                self.display_state('a')
            else:
                break
        if final_colors:
            error_occured = self.enlight_final(self.int_table)
        return error_occured

    def verify_solution(self):
        '''
        WorkArea:
        '''
        return self.enlight_final(self.exp_table)
