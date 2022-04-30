import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv("style-transfer-annotation.tsv", sep = "\t")
df = df[["Removed Comment", "Custom"]]
df = df.dropna()
df_list = df.values.tolist()
print (len(df_list))

X, y = [], []

##for i in range (len(df_list)):
##	X.append(df_list[i][0])
##	y.append(df_list[i][1])
##
##
##X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
##
##print (len(X_train), len(X_test), len(y_train), len(y_test))
##
##def writefile(X,y, filename):
##	with open (filename, "w", encoding = "utf-8") as f:
##		f.write("input_text\ttarget_text\n")
##		for i in range (len(X)):
##			f.write(X[i] + "\t" + y[i] + "\n")
##
##writefile(X_train, y_train, "train.tsv")
##writefile(X_test, y_test, "test.tsv")
