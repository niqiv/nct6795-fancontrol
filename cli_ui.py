import os

class Cli_UI():
	def __init__(self, fans):
		self.fans = fans

	def cli_ui(self):
		while True:
			os.system('clear')
			print('Select option:')
			print('1: Set operation mode')
			print('2: Set manual fan speed')
			print('none: exit')
			sel = input(' : ')

			if sel == '1':
				self._set_operation_mode()
			elif sel == '2':
				pass
			elif sel:
				pass
			else:
				break

	def _set_operation_mode(self):
		while True:
			os.system('clear')
			print('Set operation mode:')
			print('0: Full Speed')
			print('1: Manual mode')
			print('2: Thermal Cruise')
			print('3: Fan Speed Cruise')
			#print('4: Smart Fan III') # NCT6775F only
			print('5: Smart Fan IV')
			print('none: Return')
			sel = input(' : ')

			if sel == 0:
				break
			elif sel == 1:
				pass
			elif not sel:
				break