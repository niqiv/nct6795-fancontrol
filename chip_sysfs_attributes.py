import os
import getpass

def require_sudo(func):
	'''Decorator to require sudo for certain public methods'''
	def wrap(*args, **kwargs):
		if getpass.getuser() != 'root':
			# Handle this error properly elsewhere
			raise PermissionError(
				'You might need to run this program as sudo')
		result = func(*args, **kwargs)
		return result
	return wrap

class PwmAttribute:
	'''
	Chip attribute contains attribute name (local path in dir) and read-write
	permissions as literals 'r' and 'w'
	'''
	def __init__(self, name, rw, controller):
		self.name = name
		self.rw = rw
		self.controller = controller

	def get_value(self): 
		if self.can_read:
			return self.controller._get_value_by_attribute(self)

	def can_read(self): return 'r' in self.rw

	def can_write(self): return 'w' in self.rw

	def __str__(self): return self.name


class PwmController:
	'''
	index: fan header index
	---
	This class represents pwm header on the motherboard. This class includes
	arguments linked with the header like pwmX, pwmX_enable and fanX 
	attributes.
	'''
	def __init__(self, index, chip):
		self.index = index
		self.chip = chip
		self.attributes = []

	def add_attribute(self, *args):
		if len(args) == 3:
			self.attributes.append(PwmAttribute(*args))
		else:
			print('False definition of the argument.', args)

	def _get_attribute_by_name(self, name):
		'''
		Method returns sysfs attribute by attribute name
		'''
		for i in self.attributes:
			if i.name == name: return i
		raise ValueError('Attribute %s was not found' % name)

	def _get_value_by_attribute(self, attribute):
		if isinstance(attribute, PwmAttribute):
			return self.chip.get_value_in_file(attribute.name)

	def get_value_by_name(self, name):
		attr = self._get_attribute_by_name(name)
		return self._get_value_by_attribute(attr)

	def get_name(self):
		return self.get_value_by_name('name')

	@require_sudo
	def set_attribute(self, attr, value):
		if isinstance(attr, PwmAttribute):
			return self.chip.set_value_in_file(attr.name, value)
		else:
			print('give PwmAttribute object')

	def _set_mode(self, mode):
		attr = self._get_attribute_by_name('pwm{}_enable'.format(self.index))
		return self.set_attribute(attr, mode)

	def fan_mode_disabled(self):
		return self._set_mode(0)
	def fan_mode_manual(self):
		return self._set_mode(1)
	def fan_mode_thermal_cruise(self):
		return self._set_mode(2)
	def fan_mode_speed_cuise(self):
		return self._set_mode(3)
	def fan_mode_smart_iv(self):
		return self._set_mode(5)

	def set_speed(self, value, percents=True):
		'''
		pwm: number of the fan
		value: value of the speed
		percents, default=True: True if scale 0-100 is used, if False
			pwm signal 0-255 is used
		---
		returns: new speed in percents or pwm
		'''
		if percents:
			# convert percents to pwm value
			pwm_value = round(value / 100 * 255)
		# clamp between 0 and 255
		pwm_value = max(min(pwm_value, 255), 0)

		# set manual mode for fan header
		self.fan_mode_manual()
		# set pwm signal value for fan header
		pwm = self._get_attribute_by_name('pwm{}'.format(self.index))
		set_value = self.set_attribute(pwm, pwm_value)
		if percents:
			return round(int(set_value) / 255)

	def get_speed(self):
		return int(self.get_value_by_name('fan%i_input' % self.index))

	def get_pwm(self):
		return int(self.get_value_by_name('pwm%i' % self.index))

	def __str__(self):
		return 'pwm{}'.format(self.index)

class AbstractChip:
	'''
	Abstract chip model to support all relevant sysfs arguments 
	for fan controlling described in 
	https://www.kernel.org/doc/Documentation/hwmon/sysfs-interface
	'''
	def __init__(self, sysfs_path=''):
		self.name = ''
		self.SUPPORTED_MODES = []
		self.pwm_controllers = []
		self.sysfs_path = sysfs_path

	def get_value_in_file(self, file_name):
		path = os.path.join(self.sysfs_path, file_name)
		with open(path, 'r') as f:
			for i in f.read().splitlines():
				return i

	@require_sudo
	def set_value_in_file(self, file_name, value):
		path = os.path.join(self.sysfs_path, file_name)
		with open(path, 'w') as f:
			f.write(str(value))
		return self.get_value_in_file(file_name)

	def set_all(self, function, *args):
		for i in self.pwm_controllers:
			function(i, *args)

	def __str__(self):
		return self.name

class NCT6775(AbstractChip):
	def __init__(self, sysfs_path):
		super().__init__(sysfs_path)
		self.name = 'nct6775'
		self.SUPPORTED_MODES = [0, 1, 5]

		for i in range(1, 6+1):
			controller = PwmController(i, self)
			controller.add_attribute('pwm%i' % i, 'rw', controller)
			controller.add_attribute('pwm%i_enable' % i, 'rw', controller)
			controller.add_attribute('pwm%i_mode' % i, 'rw', controller)
			controller.add_attribute('fan%i_input' % i, 'r', controller)

			self.pwm_controllers.append(controller)