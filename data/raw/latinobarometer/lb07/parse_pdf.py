import re,csv,os,sys

inFile=csv.reader(open('Latinobarometro_2007_eng.txt','r'),delimiter='\t')

qRe=re.compile('(Q|S)'+'[0-9]{1,2}'+'[A-Z]{1,}')

qCounter=0

qList=[]

for line in inFile:
#  print line
  if len(line)==0:
    line=inFile.next()
#  print line
  qMatch=re.match(qRe,line[0])
  if qMatch:
    qList.append(qMatch)
    print '====>',line[0],qMatch.group()
    
    # Get first 2 lines of question
    line=inFile.next()
#    if len(line)>0:print line[0]
    line=inFile.next()
#    if len(line)>0:print line[0]

    print ''
    qCounter+=1
print '\t',qCounter
