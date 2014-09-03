class Activity(object):
	"""docstring for Activity"""
	def __init__(self, number, overall_processing_demand, processing_function_root):
		super(Activity, self).__init__()
		self.number = number
		self.overall_processing_demand = overall_processing_demand
		self.processing_function_root = processing_function_root

class ProcessingDemandPart(object):
 	"""docstring for ProcessingDemandPart"""
 	def __init__(self, activity_number,part_number,symbol):
 		super(ProcessingDemandPart, self).__init__()
 		self.activity_number = activity_number
 		self.part_number = part_number
 		self.symbol = symbol
 	def __repr__(self):
 		return "<ProcessingDemandPart>"
 	def __str__(self):
 		return "ProcDemPart Activity={} Part={} Symbol={}".format(self.activity_number,self.part_number,self.symbol)
