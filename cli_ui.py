import os
import curses

from chip_sysfs_attributes import PwmController
from nct_io import save_configuration, load_configuration

class Cli_UI():
	def __init__(self, chip):
		self.chip = chip

	def cli_ui(self):
		while True:
			os.system('clear')
			print('Select option:')
			print('1: Set operation mode')
			print('2: Set manual fan speed')
			print('3: Read current speed')
			print('4: Save/Load configuration')
			print('none: exit')
			sel = input(' : ')

			if sel == '1':
				self._set_operation_mode()
			elif sel == '2':
				os.system('clear')
				print('Give speed as percents')
				pct = int(input(' : '))
				if pct:
					self.chip.set_all(PwmController.set_speed, pct)
			elif sel == '3':
				self._show_current_speed()
			elif sel == '4':
				self._saveload()
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
			#print('2: Thermal Cruise')
			#print('3: Fan Speed Cruise')
			#print('4: Smart Fan III') # NCT6775F only
			print('5: Smart Fan IV')
			print('none: Return')
			sel = input(' : ')

			if sel == '0':
				self.chip.set_all(PwmController.fan_mode_disabled)
			elif sel == '1':
				os.system('clear')
				print('Give speed as percents')
				pct = int(input(' : '))
				if pct:
					self.chip.set_all(PwmController.set_speed, pct)
			elif sel == '5':
				self.chip.set_all(PwmController.fan_mode_smart_iv)
				
			elif not sel:
				break

	def _show_current_speed(self):
		scr = curses.initscr()
		curses.halfdelay(10)
		curses.noecho()

		while True:
			scr.clear()
			screen = ''
			for i in self.chip.pwm_controllers:
				fan_pct = i.get_pwm() / 255 * 100
				fan_rpm = i.get_speed()
				screen += ' {} {:>5.0f}% {:>4}rpm\n'.format(
					i, fan_pct, fan_rpm)
			screen += 'Return with q'
			scr.addstr(0, 0, screen)
			if scr.getch() == ord('q'):
				break

		curses.endwin()

	def _saveload(self):
		while True:
			os.system('clear')
			print('Select save or load::')
			print('0: Save')
			print('1: Load')
			print('none: Return')
			sel = input(' : ')

			if sel == '0':
				os.system('clear')
				print('Give full path to file for save')
				path = input(' : ')
				try:
					save_configuration(self.chip, path)
				except PermissionError as e:
					print('Saving failed')
					print(e)
					input('Continue with Enter...')
			
			elif sel == '1':
				os.system('clear')
				print('Give full path to file for load')
				path = input(' : ')
				try:
					load_configuration(self.chip, path)
				except PermissionError as e:
					print('Loading failed')
					print(e)
					input('Continue with Enter...')
			elif not sel:
				break