import math
import random
import time

#2=3**x mod 2**31+2**30+7=3221225479

def BabyGiant(y,g,p):
    S=[]
    T=[]
    m = int(math.ceil(math.sqrt(p)))
    for i in range(m + 1):
        S.append( (i,pow(g,i*m,p) ) )
        T.append( (i,(y*pow(g,i, p))%p) )
    start = time.time()
    for i in range(m + 1):
    	start = time.time()
        for j in range(m + 1):
        	if(S[i][1] == T[j][1]):
        		break
        else:
        	continue
        break
    return (i*m-j)

print "BabyGiant(44,3,101) = {}".format(BabyGiant(44,3,101))
print "BabyGiant(15,7,41) = {}".format(BabyGiant(15,7,41))
startTime = time.time()
x = BabyGiant(2,3,3221225479)
print "BabyGiant(2,3,3221225479) = {}".format(x)
print "Answer found in {} seconds".format(time.time()-startTime)
print "It is " + str(bool(2 == pow(3,x,3221225479))) + " that {} = {}^{} mod {}".format(2,3,x,3221225479)

'''print "BabyGiant(44,3,101):"
x = 2**len("1100101")*(10**(-6))/2.0 #roughly the time in seconds to perform all necessary exponentiations                
print "Will take " +  str(x) + " seconds"
firstTime = time.time()
print "Result: " + str(BabyGiant(44,3,101))
firstTime2 = time.time() - firstTime #actual time it took to perform algorithm
print "Actually took {} seconds".format(firstTime2)
print "Time accuracy: {}\n".format(x/firstTime2)

print "BabyGiant(15,7,41):"
y = 2**len("101001")*(10**(-6))/2.0 #roughly the time in seconds to perform all necessary exponentiations
print "Will take " + str(y) + " seconds"
secondTime = time.time()
print "Result: " + str(BabyGiant(15,7,41))
secondTime2 = time.time() - secondTime #actual time it took to perform algorithm
print "Actually took {} seconds".format(secondTime2)
print "Time accuracy: {}\n".format(y/secondTime2)

#print BabyGiant(2,3,3221225479)

print "BabyGiant(2,3,3221225479):"
z = 2**len("11000000000000000000000000000111")*(10**(-5))
print "BabyGiant(2,3,3221225479) will take " +  str(z/(60.0*60.0)) + " hours\n"
'''
'''REPORT:
This program runs the BabyStep GiantStep algorithm to solve the discrete logarithm problem, 
and also calculates the time it takes to run it. Based on these estimates, it determines the 
time it would take to solve the problem with p=3221225479,g=3,y=2. Assuming that each 
exponentiation would take a maximum of 60 seconds, it is estimated to finish in roughly 8000 
years. However, this is a significant underestimate since exponentiations on 22 bits take 
37 seconds and 3221225479 is a 32 bit number.
'''