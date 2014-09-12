class Activity(object):
	"""docstring for Activity"""
	def __init__(self, number, overall_processing_demand, processing_function_root):
		super(Activity, self).__init__()
		self.number = number
		self.overall_processing_demand = overall_processing_demand
		self.processing_function_root = processing_function_root