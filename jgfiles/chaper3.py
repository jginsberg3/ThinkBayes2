from thinkbayes2 import Suite, Pmf
import matplotlib.pyplot as plt

### The Dice Problem

class Dice(Suite):
    def Likelihood(self, data, hypo):
        if hypo < data:
            return 0
        else:
            return 1.0/hypo
            
hypothesis = [4,6,8,12,20]
suite = Dice(hypothesis)

"""
# manually exploring Likelihood function
pmf = Pmf()
pmf.Set(8, 1/8)
pmf.Set(12, 1/12)
pmf.Set(20, 1/20)
"""


### The Locomotive Problem

# start with a simple broad prior 
hypos = range(1,1001)

class Train(Suite):
    def Likelihood(self, data, hypo):
        if hypo < data:
            return 0
        else:
            return 1.0/hypo
# it's the same problem as the dice problem!

# create and updae the suite
suite = Train(hypos)
suite.Update(60)

# plotting the likelihoods  
y = [suite[i] for i in hypos]   
fig, ax = plt.subplots()
ax.plot(hypos, y)
ax.set_title('The Train Problem\nSaw Train N=60')
fig.savefig('jgfiles/trains.png')

# so 60 is the single most likely value  
# but if you want to minimize your error (not try to get the exact value) you should guess the mean of the posterior


def Mean(suite):
    """take in a suite and calculate the mean of the posterior"""
    total = 0
    for hypo, prob in suite.Items():
        total += hypo * prob  
    return total
    
# extract most likely value
sorted_results = sorted(suite.Items(), key=lambda x: x[1], reverse=True) 
most_likely_value = sorted_results[0][0]

print("Most Likely Value: {}".format(most_likely_value))
print("Mean of Posterior: {}".format(suite.Mean()))
print("Check out jgfiles/trains.png for a cool visual!")



