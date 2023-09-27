import streamlit as st
from model import model
import operator

sentence = st.text_input("Sentence")

index = st.selectbox(
    'Show me top...',
    (1, 2, 3, 5, 10))


genre = st.radio(
    "Sort based on...",
    ["Jaro Distance (Recommended)", "Levenshtein Distance"])

on = st.toggle('Show scores')

try:

	forms = model(sentence)
	print(*forms, sep="\n")
	print("**"*40)





	if genre == 'Jaro Distance (Recommended)':
		forms = sorted(forms, key=operator.itemgetter(2), reverse=True)
	else:
		forms = sorted(forms, key=operator.itemgetter(1))


	
	if on:
		for i in range(index):
			st.write("[{}](%s)".format(forms[i][0]) % forms[i][3], forms[i][1], forms[i][2])
	else:
		for i in range(index):
			st.write("[{}](%s)".format(forms[i][0]) % forms[i][3])
except:
	pass
