import csv,re,sys,os
import json

inFile=csv.reader(open('merged_r4_codebook3_cleaned.txt','r'),delimiter='\t')

qRe=re.compile('Question Number:'+'(.*?)'+'Source')
#qRe=re.compile('Question Number:'+'(.*?)'+'Source')
# Get everythng between 'Question Number' and 'Values'

valRe=re.compile('Value Labels: '+'(.*?)'+'Source')
# Get values

answerHash={}

for line in inFile:
    if len(line)>0:
        matches=re.findall(qRe,line[0])
        if matches:
            for m in matches:
                print '\t=====>',m
                qKey=m.partition('Question')[0].strip()
                print qKey
                answerHash[qKey]={}
                values=m.partition('Value Labels: ')[2]
                values=values.split(',')
                print '----------->',values
                for v in values:
                    components=v.partition('=')
                    components=[c.strip() for c in components]
                    answerHash[qKey][components[0]]=components[2]
#                values=re.search(valRe,m) 
#                print values
#                print '\t------------>',values.groups()
            print ' '
#print answerHash
#print answerHash['Q60B']

json.dump(answerHash,open('answerKeys.json','w'))
