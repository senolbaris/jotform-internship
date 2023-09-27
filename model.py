import pandas as pd
import numpy as np
import operator
from keybert import KeyBERT
import jellyfish

raw_data = pd.read_csv("templates_data.csv")

#raw_data = raw_data[:100]

raw_data['_description'] = raw_data['_description'].str.replace(r'<[^<>]*>', '', regex=True)
raw_data['_title'] = raw_data['_title'].str.replace('-', ' ', regex=True)
raw_data = raw_data[raw_data["_language"] == "en"]
raw_data = raw_data.reset_index(drop=True)

raw_data = raw_data[["_description", "_title", "_slug"]]

raw_data["_title"] = raw_data["_title"].apply(lambda x: x.lower())
raw_data["_description"] = raw_data["_description"].apply(lambda x: x.lower())


train_data = raw_data
#test_data = raw_data[:10]
LEN = len(train_data["_title"])



sentence = """
any food related order forms to take payment ?
"""
#i need a donation form to use in church



def model(sentence):
	kw_model = KeyBERT()
	kw_3 = kw_model.extract_keywords(sentence, keyphrase_ngram_range=(1, 3), stop_words=None, top_n=3)
	kw_4 = kw_model.extract_keywords(sentence, keyphrase_ngram_range=(1, 4), stop_words=None, top_n=3)
	kw_5 = kw_model.extract_keywords(sentence, keyphrase_ngram_range=(1, 5), stop_words=None, top_n=3)

	#print(kw_3)

	levenshtein_distance = []
	jaro_distance = []
	non_dup = []
	top_5_form = []
	min_ld = 100
	min_jd = 0
	for i in range(LEN):
		max_jf2_kw3 = 0
		max_jf1_kw3 = 0
		for k in range(3):
			jf1_kw3 = jellyfish.levenshtein_distance(kw_3[k][0], raw_data["_title"][i])
			jf2_kw3 = jellyfish.jaro_distance(kw_3[k][0], raw_data["_title"][i])
			if jf2_kw3>max_jf2_kw3:
				max_jf1_kw3 = jf1_kw3
				max_jf2_kw3 = jf2_kw3

		max_jf2_kw4 = 0
		max_jf1_kw4 = 0
		for k in range(3):
			jf1_kw4 = jellyfish.levenshtein_distance(kw_4[k][0], raw_data["_title"][i])
			jf2_kw4 = jellyfish.jaro_distance(kw_4[k][0], raw_data["_title"][i])
			if jf2_kw4>max_jf2_kw4:
				max_jf1_kw4 = jf1_kw4
				max_jf2_kw4 = jf2_kw4

		max_jf2_kw5 = 0
		max_jf1_kw5 = 0
		for k in range(3):
			jf1_kw5 = jellyfish.levenshtein_distance(kw_5[k][0], raw_data["_title"][i])
			jf2_kw5 = jellyfish.jaro_distance(kw_5[k][0], raw_data["_title"][i])
			if jf2_kw5>max_jf2_kw5:
				max_jf1_kw5 = jf1_kw5
				max_jf2_kw5 = jf2_kw5


		if (max_jf2_kw3>=max_jf2_kw4) and (max_jf2_kw3>=max_jf2_kw5):
			jf1 = max_jf1_kw3
			jf2 = max_jf2_kw3
		elif (max_jf2_kw4>=max_jf2_kw3) and (max_jf2_kw4>=max_jf2_kw5):
			jf1 = max_jf1_kw4
			jf2 = max_jf2_kw4
		if (max_jf2_kw5>=max_jf2_kw3) and (max_jf2_kw5>=max_jf2_kw4):
			jf1 = max_jf1_kw5
			jf2 = max_jf2_kw5


		if len(top_5_form)!=10:
			top_5_form.append([raw_data["_title"][i], jf1, jf2, "https://www.jotform.com/form-templates/"+raw_data["_slug"][i]])
			top_5_form = sorted(top_5_form, key=operator.itemgetter(2), reverse=True)
			min_jd = top_5_form[-1][2]
		else:
			if jf2>min_jd:
				top_5_form.pop(-1)
				top_5_form.append([raw_data["_title"][i], jf1, jf2, "https://www.jotform.com/form-templates/"+raw_data["_slug"][i]]) 
				top_5_form = sorted(top_5_form, key=operator.itemgetter(2), reverse=True)
				min_jd = top_5_form[-1][2]


	return top_5_form




#print("Sentence:", sentence)
#print(*model(sentence), sep="\n")



