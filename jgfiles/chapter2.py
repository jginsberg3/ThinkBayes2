#  add path below to package autocomplete-python settings in Atom
#  /Users/jesseginsberg/Documents/Programming/thinkbayes/ThinkBayes2/thinkbayes2

from thinkbayes2 import Pmf

# instattiate a Pmf object 
pmf = Pmf()

# assign 6 values to the pmf (the integers 1-6)
# the probability of each will be 1/6
for x in [1,2,3,4,5,6]:
    pmf.Set(x, 1/6)
    
# normalize to ensure all the probabilities add up to 1
# in the example above the already do but you could make examples that didn't
pmf.Normalize()

# then you can check the probablity for any object in the pmf like:
pmf[1]



## the cookie problem
pmf = Pmf()
pmf.Set('Bowl 1', 0.5)
pmf.Set('Bowl 2', 0.5)
# these are the priors

# update the distribution based on new data 
# to do this, multiply each prior by the corresponding likelihood
pmf.Mult('Bowl 1', 0.75)
pmf.Mult('Bowl 2', 0.5)

# after this, the distribution is no longer normalized so do that again
pmf.Normalize()

# then you can check the new probabilities
pmf.Prob('Bowl 1') 






## the bayesian framework
# create a class that inherets from Pmf
class Cookie(Pmf):
    def __init__(self, hypos):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()
        
    def Update(self, data):
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()
        
    mixes = {
        'Bowl 1': {'vanilla': 0.75, 'chocolate': 0.25},
        'Bowl 2': {'vanilla': 0.5, 'chocolate': 0.5}
    }
    
    def Likelihood(self, data, hypo):
        mix = self.mixes[hypo]
        like = mix[data]
        return like

    
hypos = ['Bowl 1', 'Bowl 2']
pmf = Cookie(hypos)

# draw cookies like:
#pmf.Update('chocolate')  
#pmf.Update('vanilla')

# and see how the probabilities change   
#for hypo, prob in pmf.Items():
#    print(hypo,prob) 



### the monty hall problem
class Monty(Pmf):
    def __init__(self, hypos):
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()
        
    # update is the same as cookies
    def Update(self, data):
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()
        
    # likelihood is different though
    # no need to define separate mixes object this time
    def Likelihood(self, data, hypo):
        if hypo == data:
            return 0
        elif hypo == 'A':
            return 0.5
        else:
            return 1
        
    
# you can chose any of the three doors
hypos = 'ABC'
pmf = Monty(hypos)

# update process is the similar:
data = 'B'
pmf.Update(data)




# encapsulating framework
from thinkbayes2 import Suite
        
      
class Monty(Suite):
    def Likelihood(self, data, hypo):
        if hypo == data:
            return 0
        elif hypo =='A':
            return 0.5
        else:
            return 1
            
suite = Monty('ABC')
suite.Update('B')
suite.Print()        
            
### the M&M problem

            
class MnM(Suite):
    mix94 = dict(brown=30,
                yellow=20,
                red=20,
                green=10,
                orange=10,
                tan=10)

    mix96 = dict(blue=24,
                green=20,
                orange=16,
                yellow=14,
                red=13,
                brown=13)
                
                
    hypoA = dict(bag1=mix94, bag2=mix96)
    hypoB = dict(bag1=mix96, bag2=mix94)            
    hypotheses = dict(A=hypoA, B=hypoB)
    
    def Likelihood(self, data, hypo):
        bag, color = data
        mix = self.hypotheses[hypo][bag]
        like = mix[color]
        return like

# create like
suite = MnM('AB') 

# update like 
#suite.Update(('bag1','yellow'))      

# see results like
#suite.Print()


