import pandas as pd
import matplotlib.pyplot as plt

d = {"[0, 1, 2, 3, 4, 5]\nR1": 145.53,
     "[2, 1, 0, 3, 4, 5]\nR2": 123.15,
     "[0, 1, 2, 5, 4, 3]\nR3": 154.56,
     "[5, 4, 3, 2, 1, 0]\nR4": 111.65,
     "[5, 4, 3, 0, 1, 2]\nR5": 124.56,
     "[3, 4, 5, 2, 1, 0]\nR6": 127.35 }

df = pd.DataFrame.from_dict(d, orient='index').sort_values(by=0, ascending=False)

plt.figure(figsize=(10, 7))
plt.bar(df.index, df[0], color='#fcc46f')
plt.xticks(fontsize=10)
plt.yticks(fontsize=14)
plt.xlabel("Permuted Rule Order", fontsize=16, labelpad=12)
plt.ylabel("Time (seconds)", fontsize=16)
plt.title("Reasoning Time by Rule Order", fontsize=20, pad=14)
plt.show()