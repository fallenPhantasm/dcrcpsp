class Activity:
    def __init__(self, id, processing_demand, processing_rate_coeff):
        self.id = id
        self.processing_demand = processing_demand
        self.processing_rate_coeff = processing_rate_coeff

	def __repr__(self):
		return "Activity {} demand={} root={}".format(self.id,self.processing_demand,self.processing_rate_coeff)
	def __str__(self):
		return "Activity {} demand={} root={}".format(self.id,self.processing_demand,self.processing_rate_coeff)