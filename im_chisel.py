#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest

import lb_cnst


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

    def can_be_black(self):
        '''
        ItemChisel:
        Black was not yet excluded.
        '''
        return self.cell_txt[self.local_nr] in (lb_cnst.CODE_UNKNOWN, lb_cnst.CODE_BLACK)

    def still_searching(self):
        '''
        ItemChisel:
        Position is defined.
        Position is still inside working area, before end of line.
        '''
        return self.local_nr is not None and self.local_nr < self.total_len

    def black_before_first_ship(self):
        '''
        ItemChisel:
        There should be no black fields before first ship.
        '''
        return self.elem_nr == 0 and self.cell_txt[:self.local_nr].count(lb_cnst.CODE_BLACK) > 0

    def internal_rotate(self):
        '''
        ItemChisel:
        '''
        result = None
        look_for_result = 1
        while look_for_result and self.still_searching():
            self.local_nr += 1
            if self.local_nr >= 0 and self.local_nr < self.total_len:
                if self.black_before_first_ship():
                    self.set_local(None)
                    look_for_result = 0  # Some fields are black before first ship - it is wrong!
                elif self.can_be_black():
                    end_point = self.local_nr + self.ship_len
                    if end_point <= self.total_len:
                        part_before = self.cell_txt[self.sub_start:self.local_nr]
                        part_inside = self.cell_txt[self.local_nr:end_point]
                        part_after = self.cell_txt[end_point:]
                        other_txt = part_before + part_after
                        if self.next_chisel is not None or other_txt.count(lb_cnst.CODE_BLACK) == 0:
                            if part_inside.count(lb_cnst.CODE_EMPTY) == 0:
                                if self.local_nr == 0 or self.cell_txt[self.local_nr - 1] != lb_cnst.CODE_BLACK:
                                    if end_point == self.total_len or self.cell_txt[end_point] != lb_cnst.CODE_BLACK:
                                        result = self.local_nr
                                        look_for_result = 0
            else:
                self.set_local(None)
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
        return after_str.count(lb_cnst.CODE_BLACK)

    def multi_rotor_pos(self, sub_start):
        '''
        ItemChisel:
        '''
        result = None
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
                    look_for_good_values = 0  # No more good places for current ship, end search loop
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


class TestChiselTool(unittest.TestCase):
    def test_1_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('.')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), None)

    def test_2_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('..')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), [1])
        self.assertEqual(obj.next_head_pos(), None)

    def test_3_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('...')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), [1])
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)

    def test_4_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('. .')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)

    def test_5_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('H')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), None)

    def test_6_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('  H  .')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)

    def test_7_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(1)
        obj.apply_new_text('. H')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [2])
        self.assertEqual(obj.next_head_pos(), None)

    def test_8_a(self):
        '''
        TestChiselTool:
        '''
        obj = ItemChisel(2)
        obj.apply_new_text('.. .')
        obj.multi_rotor_pos(0)
        self.assertEqual(obj.next_head_pos(), [0])
        self.assertEqual(obj.next_head_pos(), None)
