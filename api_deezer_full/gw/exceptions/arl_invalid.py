class Arl_Invalid(Exception):
	def __init__(
		self,
		arl: str,
	) -> None:

		self.arl = arl
		self.message = f'Sorry the \'{self.arl[:10]}...\' looks incorrect'

		super().__init__(self.message)