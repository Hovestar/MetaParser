#!/usr/bin/python3
class ParseObjects:
	class Seq:
		def __init__(self,e1,e2):
			self.e1 = e1
			self.e2 = e2
		def __str__(self):
			return "Seq("+str(self.e1)+","+str(self.e2)+")"
	class EBNF:
		def __init__(self,e1,e2):
			self.e1 = e1
			self.e2 = e2
		def __str__(self):
			return "EBNF("+str(self.e1)+","+str(self.e2)+")"
	class Union:
		def __init__(self,e1,e2):
			self.e1 = e1
			self.e2 = e2
		def __str__(self):
			return "Union("+str(self.e1)+","+str(self.e2)+")"
	class Concat:
		def __init__(self,e1,e2):
			self.e1 = e1
			self.e2 = e2
		def __str__(self):
			return "Concat("+str(self.e1)+","+str(self.e2)+")"
	class Extend:
		def __init__(self,e1):
			self.e1 = e1
		def __str__(self):
			return "Extend("+str(self.e1)+")"
	class Opt:
		def __init__(self,e1):
			self.e1 = e1
		def __str__(self):
			return "Opt("+str(self.e1)+")"
	class Name:
		def __init__(self,val1):
			self.val1 = val1
		def __str__(self):
			return "Name(\""+str(self.val1)+"\")"
	class Term:
		def __init__(self,value):
			self.val1 = value
		def __str__(self):
			return "Term(\""+self.val1+"\")"


class ParseError(Exception):
	pass

class EBNFParser:
	def __init__(self):
		pass
	def parse(self,string):
		res = self.Seq(string)
		if(res[1].strip()==""):
			return res[0]
		raise ParseError("Didn't consume full input. "+res[1])
	def Seq(self,string):
		res = self.EBNF(string)
		def helper(exp,string):
			if(string == "" or string[0]!="\n"):
				return exp,string
			try:
				res = self.EBNF(string[1:])
				return helper(ParseObjects.Seq(exp,res[0]),res[1])
			except ParseError:
				return exp,string
		return helper(*res)
	def EBNF(self,string):
		name,string = self.Name(string)
		if(not string[:len("::=")] == "::="):
			raise ParseError("Expected a ::= at:\n"+string)
		string = string[len("::="):]
		tree,string = self.Union(string)
		return (ParseObjects.EBNF(name,tree),string)
	def Name(self,string):
		string=string.lstrip(" \t")
		i = 0
		for c in string:
			if not c.isalnum():
				break
			i+=1
		name = string[:i]
		string = string[i:].lstrip(" \t")
		if(i==0):
			raise ParseError("Expected a name")
		return ParseObjects.Name(name),string
	def Union(self,string):
		res = self.Concat(string)
		def helper(exp,string):
			if string=="" or string[0] != "|":
				return (exp,string)
			try:
				tree,string = self.Concat(string[1:])
				return helper(ParseObjects.Union(exp,tree),string)
			except ParseError:
				return exp,string
		return helper(*res)
	def Concat(self,string):
		res = self.Extend(string)
		def helper(exp,string):
			if string == "":
				return exp,string
			try:
				tree,string = self.Extend(string)
				return helper(ParseObjects.Concat(exp,tree),string)
			except ParseError:
				return exp,string
		return helper(*res)
	def Extend(self,string):
		try:
			return self.Opt(string)
		except ParseError:
			pass
		if string[0]!="{":
			raise ParseError("Expected { at: "+string)
		tree,string = self.Union(string[1:])
		if string[0] != "}":
			raise ParseError("Expected } at: "+string)
		return ParseObjects.Extend(tree),string[1:]
	def Opt(self,string):
		tree,string = self.Atom(string)
		if(string[0]=="?"):
			return ParseObjects.Opt(tree),string[1:]
		return tree,string
	def Atom(self,string):
		try:
			return self.Term(string)
		except ParseError:
			pass
		try:
			return self.Name(string)
		except ParseError:
			pass
		string = string.lstrip(" \t")
		if string[0] != "(":
			raise ParseError("Expected (")
		tree,string = self.Union(string[1:])
		if string[0] != ")":
			raise ParseError("Expected )")
		return tree,string[1:].lstrip(" \t")
	def Term(self,string):
		string=string.lstrip(" \t")
		if string[0]!='"':
			raise ParseError('Expected " at: '+string)
		try:
			ind = string[1:].index('"')+1
			while(string[ind-1]=='\\'):
				ind += string[ind+1:].index('"')+1
			return ParseObjects.Term(string[1:ind]),string[ind+1:].lstrip(" \t")
		except ValueError:
			raise ParseError('Expected closing in: '+string)

if __name__=="__main__":
	with open("Grammars/EBNF.gram",'r') as f:
		grammar = f.read()
	parser = EBNFParser()
	print(parser.parse(grammar))
