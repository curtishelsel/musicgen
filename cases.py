import string 
import itertools
keywords = [a+b+c for a,b,c in itertools.product("abcde ", repeat=3)]

print(keywords)
