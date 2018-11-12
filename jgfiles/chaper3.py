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
plt.close('all')

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

"""
print("Most Likely Value: {}".format(most_likely_value))
print("Mean of Posterior: {}".format(suite.Mean()))
print("Check out jgfiles/trains.png for a cool visual!")
"""


### an alternative prior
# the uniform 1-1000 prior was a rough guess, not necessarily accurate
# the book recommends a power law prior that assumes more small companies than larger companies

# make a class that inherets from Dice (this is the same as the first train class remember)
class Train2(Dice):
    def __init__(self, hypos, alpha=1.0):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, hypo**(-alpha))
        self.Normalize()
            
hypos = range(1, 1001)
suite2 = Train2(hypos)
suite2.Update(60)

# plot old and new together
# OLD
suite = Train(hypos)
suite.Update(60)
y = [suite[i] for i in hypos]   
fig, ax = plt.subplots()
ax.plot(hypos, y, color='b', label='uniform')

# NEW 
suite2 = Train2(hypos)
suite2.Update(60)
y = [suite2[i] for i in hypos]   
ax.plot(hypos, y, color='r', label='power law')

ax.set_title('The Train Problem\nUniform vs Power Law\nSaw Train N=60')
ax.legend()
fig.savefig('jgfiles/trains_2.png')
plt.close('all')



# as the upper limite of the power increases, the results converge 
ubs = [500, 1000, 2000]
for ub in ubs:
    _hypos = range(1, ub+1)
    _suite = Train2(_hypos)
    
    for ob in [30, 60, 90]:
        _suite.Update(ob)
    
    print("Upper Bound: {}".format(ub))
    print("Posterior Mean: {}".format(_suite.Mean()))
    
    
# reporting Credible Intervals
# Percentile function done by book (could use numpy better...)
def Percentile(pmf, percentage):
    p = percentage / 100.0
    total = 0
    for val, prob in pmf.Items():
        total += prob
        if total >= p:
            return val
    
# to get credible interval for case where saw the three trains: 
hypos = range(1, 1001)
suite2 = Train2(hypos)
for ob in [30, 60, 90]:
    suite2.Update(ob)
interval_95 = Percentile(suite2, 5), Percentile(suite2, 95)
print('95% credible interval: {}'.format(interval_95))