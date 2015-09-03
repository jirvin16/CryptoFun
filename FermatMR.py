import random
import math

def isPrime(n): #determines if n is prime by checking all possible divisors
        for i in range(2,int(math.sqrt(n))+1):
                if(n % i == 0):
                        return "{0} is composite".format(n)
        return "{0} is prime".format(n)


def fermat(n,k):
        if(n==2 or n==3):
                return ["{0} is prime".format(n), ""]
        elif(n==4):
                return ["4 is composite", ""]
        while(k>0):
                a = random.randint(2,n-2)
                x = (a**(n-1)) % n
                if((x % n) != 1):
                        return ["{0} is composite".format(n), "with witness {0}".format(a)]
                k = k - 1
        return ["{0} is prime".format(n), ""]

def findLargestPowerOfTwo(n): #returns the exponent of the largest power of 2 which divides n
        count = 0
        while(n % (2**count) == 0):
                count = count + 1
        return count - 1


def mr(n,k):
        if(n==2):
                return ["2 is prime", ""]
        m = (n-1) / (2**k)
        a = random.randint(1,n-1)
        x = a**m % n
        if((x % n) == 1):
                return ["{0} is prime".format(n), ""]
        while(k > 0):
                if((x % n) == -1):
                        return ["{0} is prime".format(n), ""]
                else:
                        x = (x**2) % n
                        k = k - 1        
        return ["{0} is composite".format(n), "with witness {0}".format(a)]

def successProbability(): #compares fermat and mr with isPrime to calculate success probabilities
        fermatCount = 0.0
        mrCount = 0.0
        start = 2
        end = 1000
        for i in range(start,end):
                test = random.randint(1000,10000)
                if(fermat(test,3)[0]==isPrime(test)):
                        fermatCount = fermatCount + 1.0
                if(mr(test,findLargestPowerOfTwo(test-1))[0]==isPrime(test)):
                        mrCount = mrCount + 1.0
        primeStart = start + 0.0
        primeEnd = end + 0.0
        fermatProb = fermatCount/(primeEnd-primeStart)
        mrProb = mrCount/(primeEnd-primeStart)
        return [fermatProb,mrProb]
                

carmichaelList = [561,1105,1729,2465,2821,6601,8911,41041,62745,63973,75361,101101,126217,172081,
                  188461,278545,340561] #list of some carmichael numbers

print "TESTS TO FOLLOW"

print "Carmichael Fermat Test" #fermat test on some carmichael numbers
for i in range(len(carmichaelList)):
        print " ".join(fermat(carmichaelList[i],20))

print "Carmichael MR Test" #mr test on some carmichael numbers
for i in range(len(carmichaelList)):
        print " ".join(mr(carmichaelList[i],findLargestPowerOfTwo(carmichaelList[i]-1)))

print "Carmichael Correctness Test" #tests fermat and mr with carmichael numbers
for i in range(len(carmichaelList)):
	print carmichaelList[i]
        print "fermat: {0}".format((fermat(carmichaelList[i],20)[0]==isPrime(carmichaelList[i])))
        print "mr: {0}".format((mr(carmichaelList[i],findLargestPowerOfTwo(carmichaelList[i]-1))[0]==isPrime(carmichaelList[i])))

print "Success Probabilities" #calculates success probabilities of fermat and mr on random integers
for i in range(10): 
        prob = successProbability()
        print "fermat success: {0}".format(prob[0])
        print "mr success: {0}".format(prob[1])

'''
REPORT:
I found that the FERMAT test has a significantly higher success rate than the MR test
on random integers between 1000 and 10000. This may be due to an incorrect implementation
of the MR algorithm however, or due to the fact that the primes tested were relatively small.
The carmichael numbers were evaluated correctly almost every time by the FERMAT and MR tests as well.
'''
