# MetaParser
---This is hopelessly out of date. I'll fix it when it's finished---
This is a metaparser. It is really just a language for EBNF, or a least a subset defined in Grammars/EBNF.gram. To run this you run "Parser.py <Grammar> <sentence>" and it generates a tree for the sentence based on the grammar. 

## How it works
The first thing this does is take the grammar and parse it how works. It does this based on the EBNF grammar. Essentially there are 5 + 2 important rules. First the +2 rules. These are ESeq and EBnf. The Sequence just allows more than one rule in a grammar and I get rid of that right away and make it a list of rules rather than a nested tree. Then I take each EBnf, and take it's rules and associate them with the names. Then come the 5 important rules. From my Priciples of programming languages class at CU we needed to implement a parser for  regex and I noticed a few behaviors in the code. They were that the code needed to Parse Below, concatenate two parts, perform an or, use a helper function for repeats, or remove stuff from the string. Conviently based on the grammar these correspond directly with the ESymb, ESymbs, ERules, EPart, and ETerm rules respectively.
The next challenge was getting the parts to behave as a function. I do this by using two functions together, topLevel and parser. All toplevel does is take a name, and it then retrieves the parse tree associated with that name and calls parser on it. Then it takes the resulting list of matching parts and returns an object with the associated name and list of parts. parser then is effectivly a match statement on each of the previously mentioned classes. It matches each part and modifies the resulting list and then passes it up. 
--Edit--
While refactoring I noticed that there would be an issue with "rule1 ::= rule2 | rule2 rule3", because the or would match the first rule2 so it would never try rule3. So I added option "rule1 ::= rule2 (rule3)?" which will always test rule3 and always return success. However it occurs to me that some garbage may form from a "rule1 ::= fail?". Or it's a hacky way of including the empty string, that I intentionally didn't include.  

##Possible Uses
So this project was just for fun for me, but I can see an application in Programming Languages. I hope to build the other side of this that deals with the implementation of a language so that prototyping a language is as easy as designing it. Then it can be written the proper way, but it would be really nice to be able to test drive a language just from a specification. 

##Special Terminals
There are a few special terminals that I put in the make life easier. They are:
1 ALPHA - All alphabetical letters or-ed together.
1 NUM - All digits 0 to 9 or-ed together.
1 ALPHANUM - A letter or digit.
1 WHITESPACE - TAB or space (" ") or NEWLINE
1 NEWLINE - newline ("\n")
1 TAB - tab ("\t")
1 QUOTE - quote ("\"")
1 BACKSLASH - backslash ("\\")
1 ALPHAS - ALPHA {ALPHA} - It just puts this all in one string for ease.
1 NUMS - NUM {NUM} - Similar to ALPHAS
1 ALPHANUMS - ALPHANUM {ALPHANUM} - Similar to ALPHAS
1 WHITESPACES - {WHITESPACE} - Similar to ALPHAS
1 SPWHITES - {TAB | " "} - This only exists for the convience on writing EBNF.gram
1 TILLNEXTQUOTE - Super cheaty escape sequence. Pretty much just for EBNF.gram. This allows for \" in the string too.

Eventually I'll make this better, but for now this works. I think in the long run I'll have to change this to match regex after a certain special char. 

## Warnings
Unfortunately I didn't have a good way to tell the parser to ignore charactors that we as programmers don't care about, so that may come in the future. For now though the parse tree will have some extranous parts to it. 

## Shameless Self Promotion
I'm a junior at CU Boulder and I don't have a summer internship yet. If you think you'd like to interview me (or just ask me a question about this code) you can get me at <firstName>.<lastName>@colorado.edu. Oh and my name is Seth Hovestol. 
