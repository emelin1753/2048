import unittest
from logics import *

# тестируем игру 2048
class Test_2048(unittest.TestCase):

	#________________________________________________________
	def test_get_number_from_index_1_2(self):
		self.assertEqual(get_number_from_index(1, 2, 4), 7)


	def test_get_number_from_index_3_3(self):
		self.assertEqual(get_number_from_index(3, 3, 4), 16)

	
	#________________________________________________________
	def test_get_index_from_number_7(self):
		self.assertEqual(get_index_from_number(7, 4), (1, 2))


	def test_get_index_from_number_16(self):
		self.assertEqual(get_index_from_number(16, 4), (3, 3))


	def test_get_index_from_number_1(self):
		self.assertEqual(get_index_from_number(1, 4), (0, 0))


	#________________________________________________________
	def test_get_empty_list_all_0(self):
		mas_test = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		list_res = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
		self.assertEqual(get_empty_list(mas_test, 4), list_res)


	def test_get_empty_list_all_1(self):
		mas_test = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
		self.assertEqual(get_empty_list(mas_test, 4), [])


	def test_get_empty_list_notall_0(self):
		mas_test = [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		list_res = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
		self.assertEqual(get_empty_list(mas_test, 4), list_res)


	#________________________________________________________
	def test_is_zero_in_mas_all_1(self):
		mas_test = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
		self.assertEqual(is_zero_in_mas(mas_test), False)


	def test_is_zero_in_mas_one_0(self):
		mas_test = [[1, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
		self.assertEqual(is_zero_in_mas(mas_test), True)


	def test_is_zero_in_mas_all_0(self):
		mas_test = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		self.assertEqual(is_zero_in_mas(mas_test), True)


	#________________________________________________________
	def test_move_left_first(self):
		mas_test = [[2, 2, 0, 0], [0, 4, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		mas_res = [[4, 0, 0, 0], [8, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		self.assertEqual(move_left(mas_test, 4), (mas_res, 12))


	def test_move_left_second(self):
		mas_test = [[2, 4, 4, 2], [4, 0, 0, 2], [0, 0, 0, 0], [8, 8, 4, 4]]
		mas_res = [[2, 8, 2, 0], [4, 2, 0, 0], [0, 0, 0, 0], [16, 8, 0, 0]]
		self.assertEqual(move_left(mas_test, 4), (mas_res, 32))


	#________________________________________________________
	def test_move_up(self):
		mas_test = [
					[2, 4, 0, 2], 
					[2, 0, 2, 0], 
					[4, 0, 2, 4], 
					[4, 4, 0, 0]
					]
		mas_res = [
					[4, 8, 4, 2], 
					[8, 0, 0, 4], 
					[0, 0, 0, 0], 
					[0, 0, 0, 0]]
		self.assertEqual(move_up(mas_test, 4), (mas_res, 24))


	#________________________________________________________
	def test_move_down(self):
		mas_test = [
					[2, 4, 0, 2], 
					[2, 0, 2, 0], 
					[4, 0, 2, 4], 
					[4, 4, 0, 0]
					]
		mas_res = [
					[0, 0, 0, 0], 
					[0, 0, 0, 0], 
					[4, 0, 0, 2], 
					[8, 8, 4, 4]]
		self.assertEqual(move_down(mas_test, 4), (mas_res, 24))


	#________________________________________________________
	def test_can_move_true(self):
		mas_test = [
					[2, 4, 0, 2], 
					[2, 0, 2, 0], 
					[4, 0, 2, 4], 
					[4, 4, 0, 0]
					]
		self.assertEqual(can_move(mas_test, 4), True)

	#________________________________________________________
	def test_can_move_false(self):
		mas_test = [
					[2, 4, 8, 2], 
					[8, 2, 4, 8], 
					[4, 8, 2, 4], 
					[2, 4, 8, 2]
					]
		self.assertEqual(can_move(mas_test, 4), False)

#________________________________________________________
if __name__ == '__main__':
	unittest.main()
