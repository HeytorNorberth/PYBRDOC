

import re

class ValidadorPI(object):
	"""
	Realiza a validação de cadeias de caracteres (strings) que representam
	o número da Inscrição Estadual do Estado do Piaui, conforme regras
	encontradas em http://www.sintegra.gov.br/Cad_Estados/cad_PI.html.
	"""

	def __hashDigit(self, insc):
		pesos = range(9, 1, -1)

		val = sum(int(digito) * peso for digito, peso in zip(insc, pesos)) % 11

		return 0 if val < 2 else 11 - val

	@staticmethod
	def validar(numero):
		if numero == None: return False

		p = re.compile('[^0-9]')
		x = p.sub('', numero)

		if len(x) != 9 or len(set(x)) == 1: return False

		v = ValidadorPI()

		return v.__hashDigit(x) == int(x[8])