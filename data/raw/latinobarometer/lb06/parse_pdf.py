import re,sys,os,csv

inFile=csv.reader(open('Latinobarometro_2006_eng.txt','r'))

qRe=re.compile('(P|Q|S)'+'[0-9]+'+'[A-Z]{0,}')
qRe=re.compile('(P|Q|S)'+'[0-9]+'+'[A-Z]{0,}')
aRe=re.compile('[0-9]{1,2}')

qCounter=0

for line in inFile:
#    print line
    if len(line)==0:
        line=inFile.next()
    if re.match(qRe,line[0]):
        toks=line[0].split('.- ')
        print toks[0].lower()+','+toks[1]
        qCounter+=1
#        for p in inFile.next():
#            print p.encode('utf-8'),
#            print ''
#        sys.exit(1)
    if re.match(aRe,line[0]):
#        print '\t',line[0]
        continue
#print '\t',qCounter
