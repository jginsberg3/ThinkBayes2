# cookie problem exercise (page 18)

from thinkbayes2 import Suite

class newCookie(Suite):
    mixes = {
        'Bowl 1': {'vanilla': 30, 'chocolate': 10},
        'Bowl 2': {'vanilla': 20, 'chocolate': 20}
    }
    
    def remove_cookie(self, hypo, data):
        self.mixes[hypo][data] -= 1
        
    def Likelihood(self, data, hypo):
        self.remove_cookie(hypo, data)
        
        mix = self.mixes[hypo]
        remaining_total_cookies = sum([i for i in mix.values()])
        drawn_cookie = mix[data]
        like = drawn_cookie / remaining_total_cookies
        return like
        

# make new class cookie
hypos = ['Bowl 1', 'Bowl 2']
cookie = newCookie(hypos)

# draw cookie 
# cookie.Update('vanilla')  
# cookie.Update('chocolate')

# check status
cookie.Print()