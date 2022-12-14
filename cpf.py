
import re

from itertools import chain
from random import randint

from .documentoidentificacao import DocumentoIdentificacao

class CPF(DocumentoIdentificacao):
	"""
	docstring for CPF

	Attributes
	# type : (str)

	"""

	def __init__(self, arg): 
		super().__init__(arg)

	def __str__(self):
		"""
		Methods
		-------

		Formatará uma string de CPF somente com números formatada adequadamente, adicionando visual de formatação padrão
		símbolos de ajuda para exibição.
		Se CPF for Nenhum, retorna uma string vazia; caso contrário, se a string CPF for encurtada para 11 dígitos ou
		contém caracteres sem dígitos, retorna o valor bruto que representa a instância do CPF inválido
		string não formatada
		"""

		if self.rawValue == None: return str()

		x = self.rawValue

		if not x.isdigit() or len(x) != 11 or len(set(x)) == 1:
			return self.rawValue

		return '{}.{}.{}-{}'.format(x[:3], x[3:6], x[6:9], x[9:])

	@property
	def isValid(self):
		"""
		Methods

		Retorna se os dígitos de checksum de verificação do `cpf` fornecido correspondem ou não ao seu número base.
		A entrada deve ser uma string de dígitos de comprimento adequado.
		"""
		return ValidadorCpf.validar(self)



class ValidadorCpf(object):
	"""
	docstring for ValidadorCpf
	
	"""

	def __call__(self, value):
		return ValidadorCpf.validar(value)

	def __validarCpf(self, arg):  
		return self.__validarStr(arg.rawValue)
		"""
		# type : (CPF) -> bool

		"""

	def __validarStr(self, arg): 
		"""
		# type : (CPF) -> bool

		"""

		if arg == None:
			return False

		p = re.compile('[^0-9]')
		x = p.sub('', arg)

		if len(x) != 11 or len(set(x)) == 1: return False

		return all(self.__hashdigit(x, i + 10) == int(v) for i, v in enumerate(x[9:]))


	def __hashdigit(self, cpf, position): 
		"""
		Attributes
		----------
		# type : (str, int) -> int

		Methods
		-------
		Calculará o dígito de soma de verificação `position` fornecido para a entrada `cpf`. A entrada deve conter todos
		elementos anteriores a `position` senão a computação produzirá o resultado errado.

		Returns
		-------
		return(str)
		0 se o valor for menor que 2, se não for, retorna 11 - valor

		"""

		val = sum(int(digit) * weight for digit, weight in zip(cpf, range(position, 1, -1))) % 11

		return 0 if val < 2 else 11 - val

	@staticmethod
	def validar(arg):  
		"""
		Attributes
		# type : (CPF) -> bool or  type: (str) -> bool

		"""
		v = ValidadorCpf()

		if type(arg) == CPF: return v.__validarCpf(arg)

		if type(arg) == str: return v.__validarStr(arg)

		return False


validar_cpf = ValidadorCpf()

   
class GeradorCpf(object):
	"""
	docstring for GeradorCpf
	
	"""

	def __hashDigit(self, cpf, position): 
		"""
		Attributes
		# type : (str, int) -> int

		Methods
		-------
		Calculará o dígito de soma de verificação `position` fornecido para a entrada `cpf`. A entrada deve conter
		todos os elementos anteriores a `position` senão a computação produzirá o resultado errado.

		"""

		val = sum(int(digit) * weight for digit, weight in zip(cpf, range(position, 1, -1))) % 11

		return 0 if val < 2 else 11 - val

	def __checksum(self, basenum): 
		"""
		Calculará os dígitos da soma de verificação para um determinado número de base do CPF. `basenum` precisa ser uma string de dígitos
		de comprimento adequado.
		"""
		digits = str(self.__hashDigit(basenum, 10))
		digits += str(self.__hashDigit(basenum + digits, 11))

		return digits

	@staticmethod
	def gerar(): 
		"""
		Gera um CPF válido aleatório
		"""
		base = str(randint(1, 999999998)).zfill(9)

		while len(set(base)) == 1: base = str(randint(1, 999999998)).zfill(9)

		gerador = GeradorCpf()

		return CPF(base + gerador.__checksum(base))

