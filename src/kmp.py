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

def KMPSearch(pattern, teks):
    lenteks = len(teks)
    lenpat = len(pattern)
    i = 0 ## indeks untuk teks
    j = 0 ## indeks untuk pattern
    starti = 0 ## indeks teks yang setelah pergeseran
    while (i < lenteks):
        ## bestcase if == di awal
        if(pattern[j] == teks[i]):
            i+=1
            j+=1
            if ( lenpat == j ):
                # print(pattern, " found in index ", i-j, " until ", i-1)
                return True
        else:
            firstn = takeFirstN(pattern, j)
            if (j==0):
                i += 1
            else :
                pre = createPrefix(firstn)
                sub = createSubfix(firstn)
                geser = getGeser(pre,sub)
                starti += geser
                j = 0
                i = starti
    return False

# def delBeforeKMP(pattern, teks):
#     lenteks = len(teks)
#     lenpat = len(pattern)
#     i = 0 ## indeks untuk teks
#     j = 0 ## indeks untuk pattern
#     starti = 0 ## indeks teks yang setelah pergeseran
#     while (i < lenteks):
#         ## bestcase if == di awal
#         if(pattern[j] == teks[i]):
#             i+=1
#             j+=1
#             if ( lenpat == j ):
#                 print(pattern, " found in index ", i-j, " until ", i-1)
#                 return teks[(i):lenteks]
#         else:
#             firstn = takeFirstN(pattern, j)
#             if (j==0):
#                 i += 1
#             else :
#                 pre = createPrefix(firstn)
#                 sub = createSubfix(firstn)
#                 geser = getGeser(pre,sub)
#                 starti += geser
#                 j = 0
#                 i = starti
#     return teks