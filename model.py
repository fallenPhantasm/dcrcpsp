class Activity:
    def __init__(self, id, processing_demand, processing_rate_coeff, resource_demands, predecessors, successors):
        self.id = id
        self.processing_demand = processing_demand
        self.processing_rate_coeff = processing_rate_coeff
        self.resource_demands = resource_demands
        self.predecessors  = predecessors
        self.successors = successors

	def __repr__(self):
		return "Activity {} demand={} root={}".format(self.id,self.processing_demand,self.processing_rate_coeff)
	def __str__(self):
		return "Activity {} demand={} root={}".format(self.id,self.processing_demand,self.processing_rate_coeff)