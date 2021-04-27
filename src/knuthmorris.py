def createPrefix(pattern):
    prefix = []
    for i in range(len(pattern)):
        firstn = pattern[0:i+1]
        prefix.append(firstn)
    return prefix

def createSubfix(pattern):
    prefix = []
    length = len(pattern)
    for i in range(length):
        firstn = pattern[length-i-1:length]
        prefix.append(firstn)
    return prefix

def takeFirstN(pattern, n):
    return pattern[0:n]

def getGeser(prefix, subfix):
    count = len(prefix)
    geser = count
    for i in range(len(prefix)):
        if(prefix[i]==subfix[i] and i != len(prefix)-1):
            geser = count - (i+1) 
    return geser

def kmpStringMatch(pattern, teks):
    lenteks = len(teks)
    lenpat = len(pattern)
    i = 0 ## indeks untuk teks
    j = 0 ## indeks untuk pattern
    while (i < lenteks):
        if ( lenpat == j ):
            print(pattern, " found in index ", i-j, " until ", j)
            return True
        ## bestcase if == di awal
        if(pattern[i] == teks[j]):
            i+=1
            j+=1
        else:
            print('')
            
pre = createPrefix("ayaha")
sub = createSubfix("ayaha")
print(getGeser(pre,sub))
