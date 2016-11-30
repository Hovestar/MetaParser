#!/usr/bin/python3
from EBNFParser import ParseObjects,EBNFParser,ParseError
"""
So how should this work?
Well I have the tree of the  grammar so I can generate an object for each rule. 
Then I have a few basic forms
Parse Below (return res) ESymb
concat (check res and get next part ESymbs
or (on failure find next res) ERules
EBNF (needs helper function) EPart
remove stuff (needs to shorten string) ETerm
"""
class ParseObj:
	def __init__(self,name,*args):
		self.name = name
		self.args = args
	def __str__(self):
		return self.name + ("" if len(self.args)==0 else ("("+",".join(map(lambda x: '"'+x+'"' if isinstance(x,str) else str(x),self.args))+")"))


class Parser:
	special = ["ALPHA"," NUM","ALPHANUM","WHITESPACE","NEWLINE","TAB","QUOTE","BACKSLASH","ALPHAS","NUMS","ALPHANUMS","WHITESPACES","SPWHITES","TILLNEXTQUOTE"]
	def __init__(self,grammar):
		"String with grammer is passed in in EBNF form to be read. Makes a parser object that can take arbitrary string and return fail or a parse tree"
		tree = EBNFParser().parse(grammar)
		rules = {}
		while isinstance(tree,ParseObjects.Seq):
			rules[tree.e2.e1.val1] = tree.e2.e2
			tree = tree.e1
		rules[tree.e1.val1] = tree.e2
		self.rules = rules
	def parse(self,string):
		tree,string = self.parser(string,self.rules["START"])
		if string.strip()=="":
			return tree[0]
		raise ParseError("Full input not consumed. This is left:\n"+string.strip()+"\n with this tree:\n"+"\n".join(map(str,tree)))
	def topLevel(self,string,name):
		lst,string = self.parser(string,self.rules[name])
		if len(lst) == 1 and not isinstance(lst[0],str):
			return lst,string
		return [ParseObj(name,*lst)],string
	def parser(self,string,tree):
		if isinstance(tree,ParseObjects.Name):
			return self.doName(string,tree)
		if isinstance(tree,ParseObjects.Concat):
			return self.doConcat(string,tree)
		if isinstance(tree,ParseObjects.Union):
			return self.doUnion(string,tree)
		if isinstance(tree,ParseObjects.Extend):
			return self.doExtend(string,tree)
		if isinstance(tree,ParseObjects.Opt):
			return self.doOpt(string,tree)
		if isinstance(tree,ParseObjects.Term):
			return self.doTerm(string,tree)
		raise ParseError("How'd I get here?!")
	def doName(self,string,tree):
		name = tree.val1
		if name in self.special:
			try:
				res = self.doSpecial(name,string)
			except ParseError:
				raise ParseError("???")
			return res
		return self.topLevel(string,name)
	def doConcat(self,string,tree):
		part1,string = self.parser(string,tree.e1)
		part2,string = self.parser(string,tree.e2)
		return part1 + part2,string
	def doUnion(self,string,tree):
		try:
			return self.parser(string,tree.e1)
		except ParseError:
			pass
		return self.parser(string,tree.e2)
	def doExtend(self,string,tree):
		def helper(exp,string):
			if(string == ""):
				return exp,string
			try:
				end,string = self.parser(string,tree.e1)
				return helper(exp+end,string)
			except ParseError:
				return exp,string
		return helper([],string)
	def doOpt(self,string,tree):
		try:
			return self.parser(string,tree.e1)
		except ParseError:
			return [],string
	def doTerm(self,string,tree):
		val = tree.val1
		if len(string)< len(val) or string[:len(val)]!=val:
			try:
				place = string[string.index("\n")]
			except ValueError:
				place = string
			raise ParseError("Expected "+val + " at: "+place )
		return [val],string[len(val):]
	def doSpecial(self, special, string):
		if string == "" and special not in ["SPWHITES","WHITESPACES"]:
			raise ParseError("Buffer is empty. Looking for "+special)
		if special == "ALPHA":
			if string[0].isalpha():
				return [string[0]],string[1:]
			raise ParseError("Expected a letter")
		if special == " NUM":
			if string[0].isdigit():
				return [string[0]],string[1:]
			raise ParseError("Expected a number")
		if special == "ALPHANUM":
			if string[0].isalnum():
				return [string[0]],string[1:]
			raise ParseError("Expected a letter or a number")
		if special == "WHITESPACE":
			if string[0] in "\t\n ":
				return [string[0]],string[1:]
			raise ParseError("Expected whitespace")
		if special == "NEWLINE":
			if string[0] == "\n":
				return [string[0]],string[1:]
			raise ParseError("Expected newline")
		if special == "TAB":
			if string[0] == "\t":
				return [string[0]],string[1:]
			raise ParseError("Expected tab")
		if special == "QUOTE":
			if string[0] == '"':
				return [string[0]],string[1:]
			raise ParseError("Expected a quote")
		if special == "BACKSLASH":
			if string[0] == "\\":
				return [string[0]],string[1:]
			raise ParseError("Expected a backslash")
		if special == "ALPHAS":
			i = 0
			while len(string)>i and string[i].isalpha():
				i+=1
			if(i!=0):
				return [string[:i]],string[i:]
			raise ParseError("Expected at least one letter")
		if special == "NUMS":
			i = 0
			while len(string)>i and string[i].isdigit():
				i+=1
			if(i!=0):
				return [string[:i]],string[i:]
			raise ParseError("Expected at least one digit")
		if special == "ALPHANUMS":
			i = 0
			while len(string)>i and string[i].isalnum():
				i+=1
			if(i!=0):
				return [string[:i]],string[i:]
			raise ParseError("Expected at least one letter or digit")
		if special == "WHITESPACES":
			i = 0
			while len(string)>i and string[i] in "\t \n":
				i+=1
			return [string[:i]],string[i:]
		if special == "SPWHITES":
			i = 0
			while len(string)>i and string[i] in "\t ":
				i+=1
			return [string[:i]],string[i:]
		if special == "TILLNEXTQUOTE":
			ind = string[1:].index('"')+1
			while(string[ind-1]=='\\'):
				ind += string[ind+1:].index('"')+1
			return [string[1:ind]],string[ind:]
		raise ParseError("Oops implementation error. Looking for "+special)

if __name__=="__main__":
	import sys
	if(len(sys.argv)>1):
		grammarFile = sys.argv[1]
	else:
		grammarFile = "Grammars/re.gram"
	if(len(sys.argv)>2):
		sentence = sys.argv[2]
	else:
		sentence = "(a.?)*"
	with open(grammarFile,'r') as f:
		text = f.read()
	parser = Parser(text)
	tmp = parser.parse(sentence)
	print(tmp)
