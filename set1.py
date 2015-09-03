import binascii
import sys
import math

def hex_to_base64(hexa):
	return binascii.b2a_base64(binascii.unhexlify(hexa))

def inc_key(key):
	int_key=int(key,16)
	int_key=int_key+1
	hex_key=hex(int_key)[2:] #get rid of 0x in the beginning of the hex number 
	return hex_key

def xor(x,y):
	return int(x,16)^int(y,16)

def decrypt(data,key):
	ans=""
	for temp in [data[a:a+2] for a in range(0,len(data)-2,2)]:
		ans=ans+chr(xor(temp,key))   
	return ans    

def similarity(textFreq):
	englishFreq = [0.081,0.014,0.027,0.042,0.127,0.022,0.02,0.06,0.069,0.001,0.007,0.04,0.024,0.067,0.075,0.019,0.001,0.059,0.063,0.09,0.027,0.009,0.023,0.001,0.019,0.001]
	dotProduct = 0.0
	textProduct = 0.0
	englishProduct = 0.0
	for i in range(len(textFreq)):
		dotProduct += (englishFreq[i]*textFreq[i])
		textProduct += (textFreq[i]*textFreq[i])
		englishProduct += (englishFreq[i]*englishFreq[i])
	value = math.sqrt(textProduct)*math.sqrt(englishProduct)
	if(value==0):
		return 0
	return dotProduct/value

def isValidPlaintext(string):
	for i in range(len(string)):
		if(string[i] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!?',\n "):
			return 0
	return 1

def singleByteXORCipher(data):
	keywords=['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 
		  'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 
		  'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 
		  'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 
		  'when', 'make', 'can', 'like', 'time', 'just', 'him', 'know', 'take', 'people', 
		  'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 
		  'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 
		  'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 
		  'any', 'these', 'give', 'day', 'most', 'us']
	key="00"
	for a in range(0,255):
		ans=decrypt(data,key)
		#print ans
		for word in keywords:
			word=" "+word+" "
			if word in ans or word+" " in ans or " "+word in ans or " "+word+" " in ans:
				print "[*]Encrypted data : "+data
				print "[*]Decrypted data : "+ans
				print "[*]key : 0x"+(key)
				return key
		textFreq = []
		for i in range(26):
			textFreq.append((ans.count(chr(ord('a') + i))+ans.count(chr(ord('A') + i))+0.0)/(len(ans)+0.0))    	
		sim = similarity(textFreq)
		if(1 - isValidPlaintext(ans)):
			sim = sim * 0
		if(sim > 0.52):
			#print "[*]Encrypted data : "+data
			#print "[*]Decrypted data : "+ans
			#print "[*]key : 0x"+(key)
			return key
		key=inc_key(key)
	return 0

def repeatingKeyXOR(plaintext, key):
	ans = ""
	plainHex = plaintext.encode("hex")
	keyHex = key.encode("hex")
	i = 0
	for temp in [plainHex[a:a+2] for a in range(0,len(plainHex)-1,2)]:
		ans=ans+hex(xor(temp,keyHex[i%6:i%6+2]))[2:]
		i += 2
	if(len(ans)%2 == 1):
		ans = "0" + ans
	return ans

def computeHammingDistance(plaintext1, plaintext2):
	binary1 = bin(int(binascii.hexlify(plaintext1), 16))[2:]
	binary2 = bin(int(binascii.hexlify(plaintext2), 16))[2:]
	if(len(binary1) <= len(binary2)):
		for i in range(len(binary2) - len(binary1)):
			binary1 = "0" + binary1
	else:
		for i in range(len(binary1) - len(binary2)):
			binary2 = "0" + binary2
	count = 0.0
	for i in range(len(binary1)):
		if(binary1[i] != binary2[i]):
			count += 1.0
	return count

def findKeyBytes(ciphertext, k):
	if(k == 0):
		return 0
	blockCiphers = []
	for j in range(k):
		blockCiphers.append("")
	i = 0
	#print "Ciphertext: " + ciphertext
	while(i < len(ciphertext)):
		end = i+2*k
		if(end > len(ciphertext)):
			end = (2*k-(end - len(ciphertext)))+i
		block = ciphertext[i:end]
		i += 2*k
		for j in range(0, len(block),2):
			blockCiphers[j/2] += block[j:j+2]
	key = [k]
	count = 0
	for j in range(k):
		#print "Block " + str(j) + ": " + blockCiphers[j]
		key.append("")
		if(singleByteXORCipher(blockCiphers[j]) != 0):
			key[j+1] = singleByteXORCipher(blockCiphers[j])
			count += 1
	if(count != 0):
		return key
	return 0


def breakRepeatingKeyXOR(ciphertext):
	plainText = ""
	smallestED = 1000.0
	key1 = 0
	secondSmallestED = 1000.0
	key2 = 0
	for KEYSIZE in range(2,41):
		if(KEYSIZE*16 - 1 > len(ciphertext)):
			break
		first = ciphertext[:KEYSIZE*8]
		second = ciphertext[KEYSIZE*8:KEYSIZE*16]
		editDistance = computeHammingDistance(first,second)/KEYSIZE
		if(editDistance < smallestED):
			smallestED = editDistance
			key1 = KEYSIZE
		elif(editDistance < secondSmallestED):
			secondSmallestED = editDistance
			key2 = KEYSIZE
	i = 0
	keyByte1 = findKeyBytes(ciphertext, key1)
	keyByte2 = findKeyBytes(ciphertext, key2)
	if(keyByte1 != 0 or keyByte2 != 0):
		return [keyByte1,keyByte2]
	return 0

def determineKeyAndDecipher(filename):
	keyList = []
	for data in open(filename):
		element = breakRepeatingKeyXOR(data.decode("base64", "strict").encode("hex","strict"))
		if(element != 0):
			keyList.append(element)
	keyLengthList1 = []
	keyLengthList2 = []
	for x in keyList:
		if(x[0] != 0):
			keyLengthList1.append(x[0][0])
		if(x[1] != 0):
			keyLengthList2.append(x[1][0])
	keyLen1 = most_common(keyLengthList1)
	keyLen2 = most_common(keyLengthList2)
	keyPotentialList1 = [keyLen1]
	for i in range(keyLen1):
		keyPotentialList1.append([])
	keyPotentialList2 = [keyLen2]
	for i in range(keyLen2):
		keyPotentialList2.append([])
	for x in keyList:
		if(x[0] != 0):
			if(x[0][0] == keyLen1):
				for i in range(1,len(x[0])):
					if(x[0][i] != ""):
						keyPotentialList1[i].append(x[0][i])
		if(x[1] != 0):
			if(x[1][0] == keyLen2):
				for i in range(1,len(x[1])):
					if(x[1][i] != ""):
						keyPotentialList2[i].append(x[1][i])
	listKeys = []
	for i in range(1,len(keyPotentialList1)):
		if(keyPotentialList1[i] == []):
			keyPotentialList1[i].append("00")
		for j in range(len(keyPotentialList1[i])):
			i+=1
	print keyPotentialList1
	print keyPotentialList2

def most_common(lst):
    return max(set(lst), key=lst.count)



hexa = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
print hex_to_base64(hexa)

hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"
print hex(xor(hex1,hex2))[2:-1]


data1 = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
singleByteXORCipher(data1)

if(len(sys.argv)==2):
	for data in open(sys.argv[1]):
		if(singleByteXORCipher(data)):
			break;


data2 = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
print repeatingKeyXOR(data2,"ICE")

data3 = "jdiggitydawg@gmail.com"
print repeatingKeyXOR(data3, "SWAG")

print singleByteXORCipher("062a232e6a6a332d333a23272a2f46e6a236e27c203566272")

'''
if(len(sys.argv)==2):
	determineKeyAndDecipher(sys.argv[1])
'''



print breakRepeatingKeyXOR(data1)

