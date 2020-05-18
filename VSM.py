"""
Created on Sun Apr  5 21:41:26 2019

@author: Usama Saeed
"""
import math
def length(dict):
    sum=0
    for i in dict:
        sum+=dict[i]**2
    return math.sqrt(sum)
openStopWords=open("Stopword-List.txt")
readStopWords=openStopWords.read()
stopWords=readStopWords.split('\n')
openStopWords.close()
docVector=[]
vectorSpace=[]
df={}
for i in range(50):
    docId=i+1
    tf={}
    docFlag=False
    wordList=[]
    openFile=open("ShortStories\\"+str(docId)+".txt")
    fileData=openFile.read()
    lines=fileData.split("\n")
    words=fileData.split(" ")
    openFile.close()
    word=""
    for character in fileData:
        if character=="'":
            continue
        elif not character.isalnum():
            if word=="" or stopWords.__contains__(word.lower()):
                word=""
                continue
            else:
                if tf.__contains__(word.lower()):
                    tf[word.lower()]+=1
                else:
                    vectorSpace.append(word.lower())
                    tf[word.lower()]=1
                if df.__contains__(word.lower()) and docFlag==False:
                    df[word.lower()]+=1
                else:
                    docFlag=True
                    df[word.lower()]=1
                word=""
        else:
            word+=character
    docVector.append(tf)
openFile.close()
queryTf={}
vectorSpace=set(vectorSpace)
for i in vectorSpace:
    for j in docVector:
        if j.__contains__(i):
            j[i]=1+math.log10(j[i])
        else:
            j[i]=0
    df[i]=math.log10(len(docVector)/df[i])
    queryTf[i]=0
query=input("\nEnter the Query: ")
temp=len(query)
i=0
while i!=temp:
    if not query[i].isalnum():
        if query[i]=="-" or query[i]==" ":
            query=query.replace(query[i]," ")
        else:
            query=query.replace(query[i],"")
            temp-=1
    i+=1
splitQuery=query.lower().split(" ")
stopWordsInQuery=[]
for i in splitQuery:
    if i in stopWords:
        stopWordsInQuery.append(i)
    else:
        if queryTf.__contains__(i):
            queryTf[i]+=1
        else:
            queryTf[i]=1
for i in stopWordsInQuery:
    splitQuery.remove(i)
qScore={}
for i in splitQuery:
    queryTf[i]=1+math.log10(queryTf[i])
    qScore[i]=queryTf[i]*df[i]
docScore=[]
for i in docVector:
    wtDoc={}
    for j in i:
        wtDoc[j]=i[j]*df[j]
    docScore.append(wtDoc)
total={}
sums=0
alpha=0.00
for i in range(len(docScore)):
    sums=0
    for j in splitQuery:
        sums+=(docScore[i][j]/length(docScore[i]))*(qScore[j]/length(qScore))
    if sums>=float(alpha) and sums>0:
        total[i+1]=sums
total=sorted(total.items(),key=lambda kv:(kv[1], kv[0]),reverse=True)
count=0
print("\n\n\t===SEARCH RESULT===\n")
print("\nRank\tDocument\tScore\n")
for i,j in total:
    count+=1
    print(str(count)+"\t"+str(i)+".txt"+"\t\t"+str(j))