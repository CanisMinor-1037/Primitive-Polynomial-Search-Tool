##Background
*This project aims to:
1. search for primitive polynomials on given finity field 'GF(p^m)'
2. judge whether a polynomial is primitive or not
*The project is based on Flask and Galois.
*Many Thanks to the Authers!

##Install

*Before you first use this application, please type the following commands to initialize it:
1. 'chmod +x run.sh'
2. './run.sh'

##Usage
*Please type the following commands to start this program: 
1. '. venv/bin/activate'
2. 'python app.py'
*Then click on the link 'http://localhost:5050/'.
*The website provides five services:
1.Find All: Find All Primitive Polynomials on GF(p^m)
2.Find One: Find A Primitive Polynomial on GF(p^m)
3.Num-Term: Find Num-Term Primitive Polynomials On GF(p^m)
4.Conway:   Find A Conway Polynomial On GF(p)
5.Judge:    Judge Whether A Polynomial Is Primitive On GF(p^m)
*Please select a item of the navbar by clicking on it.
*Then set values for arguments on the selected page:
1.GF: 'characteristic^degree', such as '2','2^7','3^11'.
    characteristic must be a prime and degree must be a positive number
2.Degree: the degree of the polynomials to be shown, which must be a positive number
3.Limit: the number of polynomials to be shown, which must be a positive number or '-1'(All) 
4.Method: five options: 'order', 'reverse', 'random', 'min, and 'max'
5.Submit: submit the arguments you have input
6.Number Of Term: the number of term of the polynomials to be shown, which must be a positive number
7.Characteristic: the characteristic of the prime field, which must be a prime
8.Expression: the expression of polynomial, such as 'x', 'x^5+x^7+x^19+8x^9'
*Please type 'Ctrl-C' to quit

##Maintainer
CanisMinor-1037
