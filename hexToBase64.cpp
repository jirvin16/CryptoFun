#include <iostream>       // std::cout
#include <string>         // std::string
#include <cmath>
#include <stdlib.h>

using namespace std;

int from_hex_to_decimal(char hex) {//single hex char converter
  if('0'<= hex && hex <='9') return hex - '0';
  else if (hex >= 'A' && hex <= 'Z') {
    return hex - 'A'  + 10;
  }
  else return hex - 'a' + 10;
}

string from_decimal_to_binary(int dec) {
	string binary = "0000";
	int largestTwo = 8, index = 0;
	while(dec > 0) {
		if(dec - largestTwo >= 0) {
			binary[index] = '1';
			index++;
			dec -= largestTwo;
			largestTwo /= 2;
		}
		else {
			largestTwo /= 2;
			index ++;
		}
	}
	return binary;
}

int from_binary_to_decimal(string binary, int x) {
	int i, decimal = 0;
	for(i = 0; i < x; i++) {
		decimal += (binary[i] - '0')*(pow(2,(x-1-i)));
	}
	return decimal;
}

char from_decimal_to_hex(int dec) {
	if(0 <= dec && dec <= 9) return char(dec + '0');
	else return char(dec - 10 + 'a');
}

char from_decimal_to_base64(int dec) {
	if(0 <= dec && dec <= 25) return char(dec + 'A');
	else if(26 <= dec && dec <= 51) return char(dec - 26 + 'a');
	else if(52 <= dec && dec <= 61) return char(dec - 52 + '0');
	else if(dec == 62) return '+';
	else return '/';
}

string from_binary_to_base64(string binary) {
	int i,j,decimal;
	string poop,base64 = "";
	for(i = 0; i < binary.length(); i+=6) {
		poop = "";
		for(j = i; j < i+6; j++) {
			poop += binary[j];
		}
		decimal = from_binary_to_decimal(poop, 6);
		base64 += from_decimal_to_base64(decimal);
	}
	return base64;
}

string from_hex_to_binary(string hex) {
	string binary = "";
	int i;
	for(i = 0; i < hex.length(); i++) {
		binary += from_decimal_to_binary(from_hex_to_decimal(hex[i]));
	}
	return binary;
}

string from_hex_to_base64(string hex) {
	string binary = from_hex_to_binary(hex);
	return from_binary_to_base64(binary);
}

string from_binary_to_hex(string binary) {
	if(binary.length() % 4 != 0) {
		cout << "NOPE\n";
		return "";
	}
	int i,j,decimal;
	string poop,hex = "";
	for(i = 0; i < binary.length(); i+=4) {
		poop = "";
		for(j = i; j < i+4; j++) {
			poop += binary[j];
		}
		decimal = from_binary_to_decimal(poop, 4);
		//cout << "Decimal: " << decimal << "\n";
		hex += from_decimal_to_hex(decimal);
		//cout << "Hex: " << hex << "\n";
	}
	return hex;
}

string XOR(string hex1, string hex2) {
	string binary1 = from_hex_to_binary(hex1);
	string binary2 = from_hex_to_binary(hex2);
	string x = "";
	int i;
	for(i = 0; i < binary1.length(); i++) {
		if(binary1[i] == binary2[i]) x += '0';
		else x += '1'; 
	}
	return from_binary_to_hex(x);
}

float countOccurrences(string plaintext, char c) {
	int i;
	float count = 0.0;
	for(i = 0; i < plaintext.length(); i++) {
		if(plaintext[i] == c) count += 1.0;
	}
	return count;
}

float score(string plaintext) {
	float score = 0.0, total = plaintext.length(), eFreq = countOccurrences(plaintext, 'e')/total,
	tFreq = countOccurrences(plaintext, 't')/total, aFreq = countOccurrences(plaintext, 'a')/total;
	if(eFreq >= 0.1) score += 2.0;
	if(tFreq >= 0.08) score += 1.5;
	if(aFreq >= 0.07) score += 1.0;
	return score;
}

string from_hex_to_plaintext(string hex) {
	return "";
} 



string singleByteXorCipher(string hex) {
	string x, currentBest, plaintext, current;
	int i, j, currentMax = 0, value;
	for(i = 0; i < 16; i++) {
		x = "";
		for(j = 0; j < hex.length(); j++) {
			if(i <= 9) x += char(i + '0');
			else x += char(i - 10 + 'a');
		}
		current = XOR(x,hex);
		//cout << current << "\n";
		plaintext = from_hex_to_plaintext(current);
		value = score(plaintext);
		if(value > currentMax) {
			currentMax = value;
			currentBest = plaintext;
		}
	}
	//cout << currentBest << "\n";
	return currentBest;
}

int main () {

  /*string hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
  cout << from_hex_to_base64(hex) << "\n";
  string hex1 = "1c0111001f010100061a024b53535009181c";
  string hex2 = "686974207468652062756c6c277320657965";
  string x = XOR(hex1,hex2);
  cout << x << "\n";*/
  string hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";
  cout << singleByteXorCipher(hex);
  return 0;
}
