class ConsoleHelper:
	class Globals:
		game = None

	@staticmethod
	def tokeniseString(inputString: str):
		"""
		:param inputString: The sting to tokenise
		:return: Returns the input split with ' ' ignoring quotation marks
		:rtype: list[str]
		"""
		args: list = []
		kwargs = {}

		# tokenise the string
		currentToken: str = ""
		inQuotationMarks: bool = False
		keyValue: bool = False
		key = ""

		for i, it in enumerate(inputString):
			# current character is a space?
			if it == ' ':
				# not in quotation marks?
				if not inQuotationMarks:
					# add this token and reset the current token
					if len(currentToken) > 0:
						if keyValue:
							kwargs[key] = currentToken
							keyValue = False
						else:
							args.append(currentToken)
					currentToken = ""
				else:
					currentToken += it
			elif it == '\"':
				# are we currently in quotation marks?
				inQuotationMarks = False if inQuotationMarks else True
			elif it == '=' and not inQuotationMarks:
				key = currentToken
				currentToken = ""
				keyValue = True
			else:
				currentToken += it

		# if there is data in the current token then add it
		if len(currentToken) > 0:
			if keyValue:
				kwargs[key] = currentToken
			else:
				args.append(currentToken)

		return args, kwargs
