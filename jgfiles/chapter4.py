from thinkbayes2 import Suite, Beta
import matplotlib.pyplot as plt

class Euro(Suite):
    def Likelihood(self, data, hypo):
        x = hypo
        if data == 'H':
            return x / 100.0
        else:
            return 1 - (x/100.0)

probs = range(0,101)
suite = Euro(probs)

dataset = 'H' * 140 + 'T' * 110
for data in dataset:
    suite.Update(data)

y = [suite[i] for i in probs]

fig, ax = plt.subplots()
ax.plot(probs, y)
fig.savefig('jgfiles/euro.png')
plt.close('all')

# ways to summarize the posterior
euro_max_likelihood = suite.MaximumLikelihood()
euro_mean = suite.Mean()
euro_median = suite.Percentile(50)
euro_cred_interval_90 = suite.CredibleInterval(90)  

# checking with a different prior
def TrianglePrior():
    suite = Euro()
    for x in range(0,51):
        suite.Set(x,x)
    for x in range(51,101):
        suite.Set(x, 100-x)
    suite.Normalize()
y2 = [suite[i] for i in probs]    
    
fig, ax = plt.subplots()
ax.plot(probs, y, color='blue')
ax.plot(probs, y2, color='red')
fig.savefig('jgfiles/euro2.png')
plt.close('all')
# from the fig, can see that the outcome is almost the same, regardless of priors


### ways to optimize code for speed
suite = Euro(probs)

# reduce number of times you call normalize by using UpdateSet
dataset = 'H' * 140 + 'T' * 110
suite.UpdateSet(dataset)

# re-write Likelihood so that it doesn't have to loop for each point of data
class Euro2(Suite):
    def Likelihood(self, data, hypo):
        x = hypo / 100.0
        heads, tails = data
        like = x**heads * (1-x)**tails
        return like
heads, tails = 140, 110
suite = Euro2(probs)
suite.Update((heads,tails))


#### the beta distribution (!!)
# the book has it's own Beta class, not using SciPy's
beta = Beta()
beta.Update((140,110))
beta_mean = beta.Mean()

