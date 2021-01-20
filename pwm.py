
class Pwm():

	def __init__(self, number, path, features):
		self.id = number
		self.path = path + 'pwm' + number
		self.features = features
		self.duty = self.get_feature('')
		self.enable = self.get_feature('_enable')

	def get_feature(self, feature):
		return self.features['pwm' + self.id + feature]

	def set_feature(self, feature, value=0):
		pass

	def __str__(self):
		return 'pwm{}'.format(self.id)