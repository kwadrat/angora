#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
python -m unittest angora; red_green_bar.py $? $COLUMNS
'''

import sys
import unittest
import itertools

rows = '''\
3 1 1 2
3 4 1
2 1 6
2 6 4
3 8
3 2 7
1 1 1 7
1 4 7
1 6
5 3 7
5 1 3
6 4 1 3 1
4 1 1 1 1
1 3 1 1 1 1
3 3 3
3 2 2 1 1 2
5 2 1 1
3 1 1 3
3 1 2 1 1
4 2 3 1 1 1
'''

cols = '''\
2 2 4
4 3 3 1
4 4 6
4 4
3 4 4
3 2 1
5 1 1 2
5 1 1
1 1 5 1
4 1 1 1 1 2 1
3 3 3 2
1 1 9
3 1
8 5 2
8 1
15 1
8
10 1
2 6 1 1
1 3 1 1 1 5
'''

CODE_BLACK = 'H'
CODE_UNKNOWN = '.'
CODE_EMPTY = ' '


def line_to_numbers(one_line):
    return list(map(int, one_line.split()))


def text_to_numbers(one_txt):
    all_lines = one_txt.splitlines()
    return list(map(line_to_numbers, all_lines))


rows = text_to_numbers(rows)
cols = text_to_numbers(cols)

ZnakEscape = chr(27)


verbose_messages = 0
small_enough = 29
enable_stepping = 0
def color_message(napis, paint, color):
    if paint:
        result = '%(escape)s[%(color)sm%(napis)s%(escape)s[0m' % {
            'escape': ZnakEscape,
            'napis': napis,
            'color': color,
            }
    else:
        result = napis
    return result


def green_message(napis, paint):
    return color_message(napis, paint, '32')


def red_message(napis, paint):
    return color_message(napis, paint, '31')


def decode(seq):
    '''
    Count number of marks (H letter)
    '''
    if seq:
        seq = seq.replace(CODE_UNKNOWN, CODE_EMPTY)
        result = list(map(len, seq.split()))
    else:
        result = []
    return result


def inside(small, large):
    '''
    Shorter subsequence can be inside large sequence
    '''
    result = 0
    small_cnt = len(small)
    if small_cnt <= len(large):
        for sub_large in itertools.combinations(large, small_cnt):
            result = all(map(lambda x, y: x <= y, small, sub_large))
            if result:
                break
    return result


def transpose(all_lines, row_cnt, col_cnt):
    lines_count = len(all_lines)
    empty_line = ' ' * col_cnt
    trn_lines = []
    for j in range(col_cnt):
        trn_lines.append([])
    for i in range(row_cnt):
        if i < lines_count:
            tmp_line = all_lines[i]
            tmp_len = len(tmp_line)
            if tmp_len < col_cnt:
                tmp_line = tmp_line + ' ' * (col_cnt - tmp_len)
        else:
            tmp_line = empty_line
        for j in range(col_cnt):
            trn_lines[j].append(tmp_line[j])
    trn_lines = map(lambda x: ''.join(x), trn_lines)
    trn_lines = list(trn_lines)
    return trn_lines


def zip_check(row_shadow, rows, desc):
    row_stat = map(lambda a, b: inside(a, b), row_shadow, rows)
    eq_stat = map(lambda a, b: a == b, row_shadow, rows)
    for nr, (a, b, c, d) in enumerate(zip(row_shadow, rows, row_stat, eq_stat)):
        order_number = green_message(str(nr + 1), d)
        print('%s %s %s %s' % (order_number, red_message(c, not c), a, b))
    total_state = all(row_stat)
    total_eq = all(eq_stat)
    print('%s %s' % (green_message(desc + ' total:', total_eq), red_message(total_state, not total_state)))


def easy_guess(one_ls, line_size):
    delta = line_size - (sum(one_ls) + len(one_ls) - 1)
    pos_left = 0
    out_ls = []
    for one_size in one_ls:
        possible_width = one_size - delta
        if possible_width > 0:
            first_marked = pos_left + delta
            first_stopped = pos_left + one_size
            one_tpl = (first_marked, first_stopped)
            out_ls.append(one_tpl)
        pos_left += one_size  # Przeskocz za czarny ciąg
        pos_left += 1  # Przeskocz kratkę odstępu między czarnymi
    return out_ls


def starting_point(ship_len, cell_ls):
    offset = 0
    look_for_place = 1
    while look_for_place:
        good_place_found = 1
        if offset + ship_len > len(cell_ls):
            offset = None  # Impossible, ship extends beyond legal domain
            look_for_place = 0
            continue
        if offset + ship_len < len(cell_ls) and cell_ls[offset + ship_len] == CODE_BLACK:
            offset += 1
            good_place_found = 0
            continue
        for i in reversed(range(ship_len)):
            if cell_ls[offset + i] == CODE_EMPTY:
                offset += i + 1
                good_place_found = 0
                break
        if good_place_found:
            look_for_place = 0
    return offset


def near_border(first_by_border, cell_ls):
    black_ls = []
    space_ls = []
    black_detected = 0
    offset = starting_point(first_by_border, cell_ls)
    if offset is not None:
        if offset:
            for i in range(offset):
                if cell_ls[i] == CODE_UNKNOWN:
                    space_ls.append(i)
        else:
            if cell_ls[first_by_border] == CODE_BLACK:
                for i in range(first_by_border):
                    if cell_ls[first_by_border + i] == CODE_BLACK and cell_ls[i] == CODE_UNKNOWN:
                        space_ls.append(i)
                    else:
                        break  # No more spaces to insert
        for nr in range(offset, offset + first_by_border):
            if black_detected and cell_ls[nr] != CODE_BLACK:
                black_ls.append(nr)
            if cell_ls[nr] == CODE_BLACK:
                black_detected = 1
    return [black_ls, space_ls]


def from_border(first_by_border, cell_ls):
    black_ls = []
    space_ls = []
    if cell_ls[0] == CODE_BLACK:
        for nr in range(first_by_border):
            if cell_ls[nr] == CODE_UNKNOWN:
                black_ls.append(nr)
        if cell_ls[first_by_border] == CODE_UNKNOWN:
            space_ls.append(first_by_border)
    return [black_ls, space_ls]


def fill_ship_by_border(first_by_border, cell_ls):
    black_ls = []
    # Fill fields of ship that is touching border
    if cell_ls[first_by_border] == CODE_EMPTY:
        if CODE_BLACK in cell_ls[:first_by_border]:
            for nr in range(first_by_border):
                if cell_ls[nr] == CODE_UNKNOWN:
                    black_ls.append(nr)
    return black_ls


def gen_cl_hd(length):
    return ''.join(map(lambda a: str(a % 10), range(1, length + 1)))


class DeBug:
    def this_off_test(self):
        '''
        DeBug:
        '''
        self.this_test = 0

    def __init__(self):
        '''
        DeBug:
        '''
        self.this_off_test()

    def look_at_this_test(self):
        '''
        DeBug:
        '''
        self.this_test = 1

    def i_should_inform(self, my_nr):
        '''
        DeBug:
        '''
        if 0:
            result = self.this_test and (my_nr == 4)
            if result:
                print()
                print('%s' % self.all_state)
        return 0
        return result

    def set_state(self, prm_state):
        '''
        DeBug:
        '''
        self.all_state = prm_state

de_bug = DeBug()

class ItemChisel:
    def set_next(self, next_chisel):
        '''
        ItemChisel:
        '''
        self.next_chisel = next_chisel

    def set_local(self, lcl_number):
        '''
        ItemChisel:
        '''
        if 0:
            if lcl_number is None and self.elem_nr == 5 and de_bug.this_test:
                de_bug.this_off_test()
                import pdb
                pdb.set_trace()
        self.local_nr = lcl_number

    def internal_store(self, ship_len):
        '''
        ItemChisel:
        '''
        self.ship_len = ship_len

    def __repr__(self):
        '''
        ItemChisel:
        '''
        if self.local_nr is None:
            tmp_txt = 'None'
        else:
            tmp_txt = '%d' % self.local_nr
        return 'ItemChisel[%d, %s]' % (self.elem_nr, tmp_txt)

    def __init__(self, ship_len, elem_nr=0):
        '''
        ItemChisel:
        '''
        self.set_local(-2)
        self.elem_nr = elem_nr
        self.internal_store(ship_len)
        self.set_next(None)

    def apply_new_text(self, cell_txt):
        '''
        ItemChisel:
        '''
        self.cell_txt = cell_txt
        self.total_len = len(self.cell_txt)

    def internal_rotate(self):
        '''
        ItemChisel:
        '''
        result = None
        look_for_result = 1
        while look_for_result and self.local_nr is not None and self.local_nr < self.total_len:
            self.local_nr += 1
            if self.local_nr >= 0 and self.local_nr < self.total_len:
                if self.cell_txt[self.local_nr] in (CODE_UNKNOWN, CODE_BLACK):
                    end_point = self.local_nr + self.ship_len
                    part_before = self.cell_txt[self.sub_start:self.local_nr]
                    part_inside = self.cell_txt[self.local_nr:end_point]
                    part_after = self.cell_txt[end_point:]
                    other_txt = part_before + part_after
                    if end_point <= self.total_len:
                        if self.next_chisel is not None or other_txt.count(CODE_BLACK) == 0:
                            if part_inside.count(CODE_EMPTY) == 0:
                                if self.local_nr == 0 or self.cell_txt[self.local_nr - 1] != CODE_BLACK:
                                    if end_point == self.total_len or self.cell_txt[end_point] != CODE_BLACK:
                                        result = self.local_nr
                                        look_for_result = 0
            else:
                self.set_local(None)
        if verbose_messages:
            print('End internal_rotate()', self, result)
        return result

    def get_list_of_positions(self):
        '''
        ItemChisel:
        '''
        result = None
        if self.local_nr is not None:
            if self.next_chisel is None:
                result = [self.local_nr]
            else:
                tail_ls = self.next_chisel.get_list_of_positions()
                if tail_ls is not None:
                    result = [self.local_nr] + tail_ls
        return result

    def count_of_intruders_between_me_and_next(self, curr_pos, position_of_next=None):
        '''
        ItemChisel:
        '''
        start_idx = curr_pos + self.ship_len
        if position_of_next is None:
            after_str = self.cell_txt[start_idx:]
        else:
            after_str = self.cell_txt[start_idx:position_of_next]
        return after_str.count(CODE_BLACK)

    def multi_rotor_pos(self, sub_start, detail_stop=0):
        '''
        ItemChisel:
        '''
        result = None
        if verbose_messages:
            print('Wejscie do multi_rotor_ _pos:', self, sub_start, self.total_len)
        if 0:
            if self.elem_nr == 4:
                import pdb
                pdb.set_trace()
        if detail_stop:
            import pdb
            pdb.set_trace()
        if sub_start < self.total_len:
            self.sub_start = sub_start
            self.set_local(self.sub_start - 1)
            look_for_good_values = 1
            while look_for_good_values:
                curr_pos = self.internal_rotate()
                if curr_pos is not None:
                    if self.next_chisel is not None:
                        next_pos = curr_pos + self.ship_len + 1
                        if next_pos >= self.total_len:
                            look_for_good_values = 0  # Next ship will overflow
                        else:
                            if de_bug.i_should_inform(self.elem_nr):
                                print('next_chisel.multi_rotor_pos A %d' % next_pos)
                                if 1:
                                    import pdb
                                    pdb.set_trace()
                            position_of_next = self.next_chisel.multi_rotor_pos(next_pos)
                            if position_of_next is not None:
                                if self.count_of_intruders_between_me_and_next(curr_pos, position_of_next) == 0:
                                    result = curr_pos  # OK, head and tail are in good places
                                    look_for_good_values = 0  # Return good place upward
                    else:
                        if self.count_of_intruders_between_me_and_next(curr_pos) == 0:
                            result = curr_pos  # OK, head is in good places, there is no tail to ask
                            look_for_good_values = 0  # Return good place upward
                        else:
                            if verbose_messages:
                                print('Else A4', self)
                        if verbose_messages:
                            print('Else A3', self)
                else:
                    look_for_good_values = 0  # No more good places for current ship, end search loop
                    if verbose_messages:
                        print('Else A2', self)
        else:
            if verbose_messages:
                print('Else A1', self)
        return result

    def update_locations(self):
        '''
        ItemChisel:
        '''
        my_status = None
        if self.next_chisel is None:
            my_status = self.internal_rotate()
        else:
            updating_not_finished = 1
            while updating_not_finished:
                if de_bug.i_should_inform(self.elem_nr):
                    print('next_chisel.update_locations')
                position_of_next = self.next_chisel.update_locations()
                if position_of_next is None:
                    curr_pos = self.internal_rotate()
                    if curr_pos is None:
                        updating_not_finished = 0  # Nothing found, send failure upward
                    else:
                        next_pos = curr_pos + self.ship_len + 1
                        if next_pos >= self.total_len:
                            updating_not_finished = 0  # Next ship would overflow, send failure upward
                        else:
                            if de_bug.i_should_inform(self.elem_nr):
                                print('next_chisel.multi_rotor_pos B %d' % next_pos)
                            position_of_next = self.next_chisel.multi_rotor_pos(next_pos)
                            if position_of_next is None:
                                updating_not_finished = 0  # Next ship failed to find place, send failure upward
                            else:
                                if self.count_of_intruders_between_me_and_next(self.local_nr, position_of_next) == 0:
                                    my_status = self.local_nr
                                    updating_not_finished = 0  # Good solution found
                else:
                    if self.local_nr is None:
                        updating_not_finished = 0  # No position here, send failure upward
                    else:
                        if self.count_of_intruders_between_me_and_next(self.local_nr, position_of_next) == 0:
                            my_status = self.local_nr
                            updating_not_finished = 0  # Good solution found
        return my_status

    def next_head_pos(self):
        '''
        ItemChisel:
        '''
        result = self.get_list_of_positions()
        self.update_locations()
        return result


class WoodenBox:
    def __init__(self, len_ls):
        '''
        WoodenBox:
        '''
        self.wood_ls = list(map(lambda x: ItemChisel(x[1], x[0]), enumerate(len_ls)))
        for i in range(len(self.wood_ls) - 1):
            next_in_chain = self.wood_ls[i + 1]
            self.wood_ls[i].set_next(next_in_chain)
        de_bug.set_state(self.wood_ls)

    def text_for_all(self, cell_txt, detail_stop=0):
        '''
        WoodenBox:
        '''
        for one_ship in self.wood_ls:
            one_ship.apply_new_text(cell_txt)
        if detail_stop:
            import pdb
            pdb.set_trace()
        self.wood_ls[0].multi_rotor_pos(0, detail_stop=0)
        if verbose_messages:
            for one_ship in self.wood_ls:
                print(one_ship)

    def next_full_pos(self, detail_stop=0):
        '''
        WoodenBox:
        '''
        if detail_stop:
            import pdb
            pdb.set_trace()
        return self.wood_ls[0].next_head_pos()


class WorkArea:
    def prepare_empty_data(self):
        '''
        WorkArea:
        '''
        self.int_table = []
        for row_nr in range(self.row_cnt):
            line_ls = []
            for col_nr in range(self.col_cnt):
                line_ls.append(CODE_UNKNOWN)
            self.int_table.append(line_ls)

    def assume_no_modification(self):
        '''
        WorkArea:
        '''
        self.modify_count = 0

    def __init__(self, rows, cols, verbose=0):
        '''
        WorkArea:
        '''
        self.rows = rows
        self.cols = cols
        self.row_cnt = len(self.rows)
        self.col_cnt = len(self.cols)
        self.verbose = verbose
        self.prepare_empty_data()
        self.assume_no_modification()

    def single_set(self, row_nr, col_nr, one_symbol):
        '''
        WorkArea:
        '''
        self.int_table[row_nr][col_nr] = one_symbol
        if enable_stepping:
            self.save_to_file('g%04d' % self.modify_count, enable_axis=1)
        self.modify_count += 1

    def set_black(self, row_nr, col_nr):
        '''
        WorkArea:
        '''
        if self.int_table[row_nr][col_nr] != CODE_BLACK:
            self.single_set(row_nr, col_nr, CODE_BLACK)

    def set_space(self, row_nr, col_nr):
        '''
        WorkArea:
        '''
        if self.int_table[row_nr][col_nr] == CODE_UNKNOWN:
            self.single_set(row_nr, col_nr, CODE_EMPTY)
        elif self.int_table[row_nr][col_nr] != CODE_EMPTY:
            raise RuntimeError('Why cleaning this place?')

    def slim_text(self, enable_axis=1):
        '''
        WorkArea:
        '''
        out_ls = []
        if enable_axis:
            col_header = gen_cl_hd(self.col_cnt)
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

    def read_from_file(self, file_name):
        '''
        WorkArea:
        '''
        fd = open(file_name)
        full_txt = fd.read()
        fd.close()
        all_lines = full_txt.splitlines()
        for row_nr in range(self.row_cnt):
            row_txt = all_lines[row_nr]
            for col_nr in range(self.col_cnt):
                self.int_table[row_nr][col_nr] = row_txt[col_nr]

    def save_to_file(self, file_name, enable_axis=0):
        '''
        WorkArea:
        '''
        full_txt = self.slim_text(enable_axis) + '\n'
        fd = open(file_name, 'w')
        fd.write(full_txt)
        fd.close()

    def helper_len(self):
        '''
        WorkArea:
        '''
        if self.is_col:
            item_len = self.col_cnt
        else:
            item_len = self.row_cnt
        return item_len

    def get_sketch(self, item_nr):
        '''
        WorkArea:
        '''
        if self.is_col:
            len_ls = self.cols[item_nr]
        else:
            len_ls = self.rows[item_nr]
        return len_ls

    def get_details(self, item_nr):
        '''
        WorkArea:
        '''
        if self.is_col:
            line_ls = list(map(lambda lbd_line: lbd_line[item_nr], self.int_table))
        else:
            line_ls = self.int_table[item_nr]
        if self.is_end:
            one_text = ''.join(reversed(line_ls))
        else:
            one_text = ''.join(line_ls)
        return one_text

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
        for row_nr in range(self.row_cnt):
            easy_ls = easy_guess(self.rows[row_nr], self.col_cnt)
            for easy_start, easy_end in easy_ls:
                for col_nr in range(easy_start, easy_end):
                    self.set_black(row_nr, col_nr)
        for col_nr in range(self.col_cnt):
            easy_ls = easy_guess(self.cols[col_nr], self.row_cnt)
            for easy_start, easy_end in easy_ls:
                for row_nr in range(easy_start, easy_end):
                    self.set_black(row_nr, col_nr)

    def fill_b_from_each_border(self):
        '''
        WorkArea:
        '''
        frequent_update = 1
        item_len = self.helper_len()
        for item_nr in range(item_len):
            len_ls = self.get_sketch(item_nr)
            one_text = self.get_details(item_nr)
            if self.is_end:
                one_length = len_ls[-1]
            else:
                one_length = len_ls[0]
            black_ls, space_ls = near_border(one_length, one_text)
            for offset in black_ls:
                self.helper_black(item_len, item_nr, offset)
            for offset in space_ls:
                self.helper_space(item_len, item_nr, offset)
            if frequent_update:
                one_text = self.get_details(item_nr)
            black_ls, space_ls = from_border(one_length, one_text)
            for offset in black_ls:
                self.helper_black(item_len, item_nr, offset)
            for offset in space_ls:
                self.helper_space(item_len, item_nr, offset)
            if frequent_update:
                one_text = self.get_details(item_nr)
            black_ls = fill_ship_by_border(one_length, one_text)
            for offset in black_ls:
                self.helper_black(item_len, item_nr, offset)

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

    def fill_what_can_be_deduced(self, item_len, item_nr, len_ls, one_text, poss_ls):
        '''
        WorkArea:
        '''
        for ship_nr, ship_len in enumerate(len_ls):
            one_set = set(map(lambda one_sol: one_sol[ship_nr], poss_ls))
            if len(one_set) == 1:  # In all cases ship is in the same place
                if 1:
                    ship_start = list(one_set)[0]
                    self.place_ship_with_water(item_len, item_nr, ship_start, ship_len)

    def analyze_possibilities(self, item_len, item_nr, len_ls, one_text):
        '''
        WorkArea:
        '''
        poss_ls = []
        wooden_box = WoodenBox(len_ls)
        wooden_box.text_for_all(one_text)
        while 1:
            new_one = wooden_box.next_full_pos()
            if new_one is None:
                break
            else:
                poss_ls.append(new_one)
        solution_cnt = len(poss_ls)
        if solution_cnt < small_enough:
            self.fill_what_can_be_deduced(item_len, item_nr, len_ls, one_text, poss_ls)
                

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
                first_index = one_text.index(CODE_BLACK)
                last_index = one_text.rindex(CODE_BLACK)
                for offset in range(first_index + 1, last_index):
                    if one_text[offset] is CODE_UNKNOWN:
                        self.helper_black(item_len, item_nr, offset)
            if 1:
                self.analyze_possibilities(item_len, item_nr, len_ls, one_text)

    def fill_a_from_each_border(self):
        '''
        WorkArea:
        '''
        for self.is_col in range(2):
            for self.is_end in range(2):
                self.fill_b_from_each_border()
            self.fill_c_for_both()

    def display_state(self, label):
        '''
        WorkArea:
        '''
        print('Place %s %d' % (label, self.modify_count))
        print(self.slim_text())


def main():
    assert sum(map(sum, rows)) == sum(map(sum, cols))
    if 0:
        all_lines = []
        row_cnt = col_cnt = 0
        row_shadow = list(map(decode, all_lines))
        if 1:
            tmp_format = 'row_shadow'
            print('Eval: %s %s' % (tmp_format, eval(tmp_format)))
        trn_lines = transpose(all_lines, row_cnt, col_cnt)
        col_shadow = list(map(decode, trn_lines))
        zip_check(row_shadow, rows, 'Rows')
        zip_check(col_shadow, cols, 'Cols')
    work_a_area = WorkArea(rows, cols)
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
    if len(sys.argv) > 1 and sys.argv[1] == 'order':
        rc_order()
    else:
        main()


class TestAngoraPuzzle(unittest.TestCase):
    def test_angora_puzzle(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(decode(''), [])
        self.assertEqual(decode('H'), [1])
        self.assertEqual(decode('HH'), [2])
        self.assertEqual(decode('H H'), [1, 1])
        self.assertEqual(decode('.'), [])

    def test_one_in_another(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(inside([], []), 1)
        self.assertEqual(inside([1], []), 0)
        self.assertEqual(inside([2], [1]), 0)
        self.assertEqual(inside([1, 2], [2, 1]), 0)
        self.assertEqual(inside([2], [1, 1]), 0)
        self.assertEqual(inside([2], [1, 1]), 0)
        self.assertEqual(inside([2], [2, 1]), 1)
        self.assertEqual(inside([], [2, 1]), 1)

    def test_exchange_rows_cols(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(transpose([], 0, 0), [])
        self.assertEqual(transpose([['a', 'b']], 1, 2), ['a', 'b'])
        self.assertEqual(transpose(['a', 'b'], 2, 1), ['ab'])
        self.assertEqual(transpose(['abc', 'xyz'], 2, 3), ['ax', 'by', 'cz'])
        self.assertEqual(transpose(['ax', 'by', 'cz'], 3, 2), ['abc', 'xyz'])

    def test_constants(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(CODE_BLACK, 'H')
        self.assertEqual(CODE_UNKNOWN, '.')
        self.assertEqual(CODE_EMPTY, ' ')

    def test_moving_both_directions_to_limits(self):
        '''
        TestAngoraPuzzle:
        Funkcja zwraca listę [(początek, koniec), ...] elementów do wypełnienia
        Konwencja wyniku: Python range() lub inaczej C/for
        '''
        self.assertEqual(easy_guess([20], 20), [(0, 20)])
        self.assertEqual(easy_guess([19], 19), [(0, 19)])
        self.assertEqual(easy_guess([18], 19), [(1, 18)])
        self.assertEqual(easy_guess([17], 19), [(2, 17)])
        self.assertEqual(easy_guess([4, 5], 10), [(0, 4), (5, 10)])
        self.assertEqual(easy_guess([2, 5], 10), [(5, 8)])

    def test_by_border_fill_from_first_black(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(near_border(4, 'H......'), [[1, 2, 3], []])
        self.assertEqual(near_border(4, '.......'), [[], []])
        self.assertEqual(near_border(4, '.H.....'), [[2, 3], []])
        self.assertEqual(near_border(5, '.H.....'), [[2, 3, 4], []])
        self.assertEqual(near_border(5, '.H.H...'), [[2, 4], []])
        self.assertEqual(near_border(5, ' H.H...'), [[2, 4, 5], []])
        self.assertEqual(near_border(5, '.. .H.......'), [[5, 6, 7], [0, 1]])
        self.assertEqual(near_border(3, '...H.......'), [[], [0]])
        self.assertEqual(near_border(3, '...HH......'), [[], [0, 1]])
        self.assertEqual(near_border(4, '...HH......'), [[], [0]])
        self.assertEqual(near_border(3, ' ..HH'), [[], [1]])
        self.assertEqual(near_border(2, ' ..HH'), [[], [1, 2]])
        self.assertEqual(starting_point(4, '    HHHH.'), 4)
        #self.assertEqual(near_border(4, '    HHHH.'), [[], [8]]) # qaz - row 4, col 12
        self.assertEqual(starting_point(5, '.. .H.......'), 3)
        self.assertEqual(starting_point(5, '...H.......'), 0)
        self.assertEqual(starting_point(3, ' ..HH'), 2)
        self.assertEqual(starting_point(2, ' ..HH'), 3)
        #self.assertEqual(starting_point(10, '    ....HHHHHH. '), 5)
        self.assertEqual(starting_point(4, ' .H.. '), 1)
        self.assertEqual(starting_point(1, ' .H.. '), 2)
        self.assertEqual(starting_point(2, ' .H.. '), 1)
        self.assertEqual(starting_point(3, ' .H.. '), 1)
        self.assertEqual(starting_point(4, ' ..H. '), 1)
        self.assertEqual(starting_point(2, ' ..H. '), 2)
        self.assertEqual(starting_point(10, '    ....HHHHHH. '), 4)
        self.assertEqual(starting_point(9, ' ..H. '), None)

    def test_ship_touches_border(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(from_border(4, '...HH......'), [[], []])
        self.assertEqual(from_border(4, 'H......'), [[1, 2, 3], [4]])
        self.assertEqual(from_border(5, 'H......'), [[1, 2, 3, 4], [5]])
        self.assertEqual(from_border(5, 'HH.....'), [[2, 3, 4], [5]])
        self.assertEqual(from_border(1, 'H..'), [[], [1]])

    def test_ship_is_finished_but_not_filled(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(fill_ship_by_border(2, '.H .'), [0])
        self.assertEqual(fill_ship_by_border(3, 'H.H .'), [1])
        self.assertEqual(fill_ship_by_border(3, '.H. .'), [0, 2])

    def test_generating_column_heading(self):
        '''
        TestAngoraPuzzle:
        '''
        self.assertEqual(gen_cl_hd(2), '12')
        self.assertEqual(gen_cl_hd(3), '123')

    def test_a(self):
        '''
        TestAngoraPuzzle:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('.')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(1)
        obj.apply_new_text('..')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), [1])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(1)
        obj.apply_new_text('...')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), [1])
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(1)
        obj.apply_new_text('. .')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(1)
        obj.apply_new_text('H')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(1)
        obj.apply_new_text('  H  .')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(1)
        obj.apply_new_text('. H')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(2)
        obj.apply_new_text('.. .')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), None)
        obj = ItemChisel(1)

    def test_b(self):
        '''
        TestAngoraPuzzle:
        '''
        obj = WoodenBox([1, 1])
        obj.text_for_all('. .')
        self.assertEqual(obj.next_full_pos(), [0, 2])
        self.assertEqual(obj.next_full_pos(), None)
        obj.text_for_all(' . . . ')
        self.assertEqual(obj.next_full_pos(), [1, 3])
        self.assertEqual(obj.next_full_pos(), [1, 5])
        self.assertEqual(obj.next_full_pos(), [3, 5])

    def test_c(self):
        '''
        TestAngoraPuzzle:
        '''
        obj = WoodenBox([6, 4, 1, 3, 1])
        obj.text_for_all('.HHHHH..HHHH...HHH..')
        self.assertEqual(obj.next_full_pos(), [0, 8, 13, 15, 19])
        self.assertEqual(obj.next_full_pos(), [1, 8, 13, 15, 19])
        self.assertEqual(obj.next_full_pos(), None)

    def test_d(self):
        '''
        TestAngoraPuzzle:
        '''
        obj = WoodenBox([4, 1, 1, 1, 1])
        obj.text_for_all('...........H.H.H.H..', detail_stop=0)
        self.assertEqual(obj.next_full_pos(detail_stop=0), [0, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [1, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [2, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [3, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [4, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [5, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [6, 11, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(), [8, 13, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(), None)

    def test_e(self):
        '''
        TestAngoraPuzzle:
        '''
        obj = WoodenBox([4, 2, 3, 1, 1, 1])
        obj.text_for_all(' HHHH .......... ...', detail_stop=0)
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 9, 13, 15, 17])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 9, 13, 15, 18])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 9, 13, 15, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 9, 13, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 9, 14, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 9, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 10, 14, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 10, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 6, 11, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 7, 10, 14, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 7, 10, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 7, 11, 15, 17, 19])
        self.assertEqual(obj.next_full_pos(detail_stop=0), [1, 8, 11, 15, 17, 19])
