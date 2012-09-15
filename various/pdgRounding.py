#!/bin/env python

# This class implements the pdg rounding rules indicated in
# section 5.3 of doi:10.1088/0954-3899/33/1/001

# davide.gerbaudo@cern.ch
# September 2012

def pdgRound(value, error, asInt=False) :
    def threeDigits(value) :
        "extract the three most significant digits and return them as an int"
        return int(("%.2e"%float(error)).split('e')[0].replace('.','').replace('+','').replace('-',''))
    def nSignificantDigits(threeDigits) :
        assert threeDigits<1000,"three digits (%d) cannot be larger than 10^3"%threeDigits
        if threeDigits<101 : return 2 # not sure
        elif threeDigits<356 : return 2
        elif threeDigits<950 : return 1
        else : return 2
    def frexp10(value) :
        valueStr = ("%e"%float(value)).split('e')
        return float(valueStr[0]), int(valueStr[1])
    def nDigitsValue(expVal, expErr, nDigitsErr) :
        "compute the number of digits we want for the value, assuming we keep nDigitsErr for the error"
        return expVal-expErr+nDigitsErr
    def formatValue(value, exponent, nDigits) :
        if exponent<0 : return ('%.'+str(nDigits+(-exponent-1 if (-exponent+1)<nDigits else 0))+'f')%value
        else : return '%.0f'%round(value, nDigits-(exponent+1))
    def formatRoundupValue(value, exponent, nDigits) :
        if exponent<0 : return ('%.'+str(nDigits+(-exponent+1))+'f')%round(value,exponent-1)
        else : return '%.0f'%round(value, nDigits-(exponent+1))
    tD = threeDigits(error)
    nD = nSignificantDigits(tD)
    expVal, expErr = frexp10(value)[1], frexp10(error)[1]
    fVal, fErr = '', ''
    if tD>=950 :
        fVal = formatRoundupValue(value, expVal, nDigitsValue(expVal, expErr, nD))
        fErr = formatRoundupValue(error, expErr, nD)
    else :
        fVal = formatValue(value, expVal, nDigitsValue(expVal, expErr, nD))
        fErr = formatValue(error, expErr, nD)
    return (fVal, fErr)
def test(valueError=(0., 0.)) :
    val, err = valueError
    print val,' +/- ',err,' --> ',
    val, err = pdgRound(val, err)
    print ' ',val,' +/- ',err
if __name__=='__main__' :
    for x in [(0.827, 0.119121212)
              ,(0.827, 0.3676565)
              ,(0.827, 0.952)
              ,(1.2345e7, 67890.1e2)
              ] : test(x)
