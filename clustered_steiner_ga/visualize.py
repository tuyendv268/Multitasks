import pickle as pkl
from matplotlib import pyplot as plt

bfs = pkl.load(open("results.pkl", "rb"))

bfs = bfs.mean(axis=0)
bf = bfs.min()
normed_f = (bfs - bf) / (bfs[0] - bf)

print(f"f: {normed_f.mean()}")

plt.plot(normed_f)
plt.xlabel("generations")
plt.ylabel("f")
plt.show()