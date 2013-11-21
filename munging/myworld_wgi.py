import pandas as pd
import requests
import re
from subprocess import call

# utility functions
def null_oor_values(col):
    if re.match('priority[1-6]', col):
        key = 'choices'
    # cols: country, education, gender, priorities, 
    mw[col] = mw[col].fillna(0)
    code = [float(f) for f in mw_codes_json[col].keys()]
    bad_values = [val for val in list(mw[col].unique()) if float(val) not in code]
    mw[col] = mw[col].replace(to_replace=bad_values)

def decode(val, key):
    try:
        return mw_codes_json[key][str(val)]
    except:
        pass

def to_lower(s):
    try:
        return str(s).lower()
    except:
        pass

def to_int_str(s):
    try:
        return str(int(float(s)))
    except:
        pass

def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]      

print "##### LET'S DO THIS #####"
# fetch the MyWorld codes
mw_codes_json = requests.get('http://54.227.246.164/dataset/MYWorld_fields.json').json()

# fetch the MyWorld data
call(['wget', 'http://54.227.246.164/dataset/data/MYWorld_votes_all.csv.tar.bz2', '-P', '../data'])
call(['bzip2','-d','../data/MYWorld_votes_all.csv.tar.bz2'])
call(['tar', '-xvf', '../data/MYWorld_votes_all.csv.tar', '--directory=../data'])
mw = pd.read_csv('../data/MYWorld_votes_all.csv')

# fetch the wgi data
call(['mkdir', '../data/wgi'])
call(['wget','https://www.dropbox.com/s/w2po59d3pvjijv1/control_of_corruption.csv','-P','../data/wgi'])
call(['wget','https://www.dropbox.com/s/zbkyv5dbnzi62fk/government_effectiveness.csv','-P','../data/wgi'])
call(['wget','https://www.dropbox.com/s/md01cxycspdkdu6/political_stability_no_violence.csv','-P','../data/wgi'])
call(['wget','https://www.dropbox.com/s/hgh1cklc1wh0ps2/regulatory_quality.csv','-P','../data/wgi'])
call(['wget','https://www.dropbox.com/s/8gdcp57s2vyihvu/rule_of_law.csv','-P','../data/wgi'])
call(['wget','https://www.dropbox.com/s/z9gybkg0jedw28h/voice_accountability.csv','-P','../data/wgi'])

# tuple list of countries in mw not in wgi
# use the 'diff' function below to test this
tuples = [
    ("american samoa","samoa"),
    ("micronesia, fed. sts.", "micronesia (federated states of)"),
    ("bahamas, the", "bahamas"),
    ("moldova","republic of moldova"),
    ("slovak republic", "slovakia"),
    ("bolivia","bolivia (plurinational state of)"),
    ("gambia, the","gambia"),
    ("egypt, arab rep.", "egypt"),
    ("iran, islamic rep.","iran (islamic republic of)"),
    ("korea, dem. rep.","democratic people's republic of korea"),
    ("korea, rep.","republic of korea",),
    ("lao pdr","lao people's democratic republic"),
    ("macedonia, fyr","the former yugoslav republic of macedonia"),
    ("yemen, rep.", "yemen"),
    ("vietnam", "viet nam"),
    ("congo, dem. rep.","democratic republic of the congo",),
    ("congo, rep.", "congo"),
    ("united kingdom","united kingdom of great britain and northern ireland"),
    ("united states","united states of america"),
    ("venezuela, rb","venezuela (bolivarian republic of)"),
    ("west bank and gaza", "palestine (state of)"),
    ("tanzania", "united republic of tanzania"),
    ("kyrgyz republic","kyrgyzstan"),
    ("st. lucia", "saint lucia"),
    ("st. vincent and the grenadines", "saint vincent and the grenadines"),
    ("st. kitts and nevis", "saint kitts and nevis")
]

dfs = {}
target_cols = ['Country/Territory', '2012_Estimate']
wgi_csvs = [
    'control_of_corruption', 
    'political_stability_no_violence',
    'rule_of_law', 'government_effectiveness', 
    'regulatory_quality', 'voice_accountability'
 ]

# process the wgi data 
for csv in wgi_csvs:
    # read in the data set
    path = '../data/wgi/%s' % str(csv + '.csv')
    dfs[csv] = pd.read_csv(path)
    # replace spaces in column names with udnerscores
    dfs[csv].columns = [col.replace(' ', '_') for col in list(dfs[csv].columns)]
    # replace the df with the target cols df
    dfs[csv] = dfs[csv].ix[:,target_cols]
    # add the name to the column names
    dfs[csv].columns = ['country'] + [csv +'_'+ col for col in target_cols[1:]]
    # make the country names lower case
    dfs[csv]['country'] = dfs[csv]['country'].apply(to_lower)
    # replace the bad countries with the good countries
    for tup in tuples:
        dfs[csv]['country'] = dfs[csv]['country'].replace(tup[0],tup[1])
    # ineleganty fix the unruly countries    
    dfs[csv].ix[dfs[csv]['country'].str.contains('voire'), 'country'] = "cote d'ivoire"
    dfs[csv].ix[dfs[csv]['country'].str.contains('ncipe'), 'country'] = 'sao tome and principe'
    dfs[csv].ix[dfs[csv]['country'].str.contains('of the congo'), 'country'] = 'democratic republic of the congo'
    dfs[csv].ix[dfs[csv]['country'].str.contains('union'), 'country'] = 'reunion'

# null out out of range mw values
mw['country'] = mw['country'].apply(to_int_str)
null_oor_values('country')
null_oor_values('education')
null_oor_values('gender')

# decode mw country names
mw['country'] = mw['country'].apply(decode, key='country')

# lowerize mw country names
mw['country'] = mw['country'].apply(to_lower)

# pre-merge sanity check: mw countries not in wgi dfs
diff(list(mw['country'].unique()),dfs['rule_of_law']['country'])
# just for kicks, wgi countries not in mw (uncomment to run)
# diff(dfs['rule_of_law']['country'],list(mw['country'].unique()))

merge = [dfs[key] for key in dfs.keys()]
while len(merge) > 1:
    merge[0] = pd.merge(merge[0], merge[1], on='country')
    del merge[1]

mw_wgi = pd.merge(mw, merge[0], on='country')    

mw_wgi.to_csv('../data/myworld_wgi_clean.csv', encode='utf-8')

def null_oor_values(col):
    if re.match('priority[1-6]', col):
        key = 'choices'
    # cols: country, education, gender, priorities, 
    mw[col] = mw[col].fillna(0)
    code = [float(f) for f in mw_codes_json[col].keys()]
    bad_values = [val for val in list(mw[col].unique()) if float(val) not in code]
    mw[col] = mw[col].replace(to_replace=bad_values)

def decode(val, key):
    try:
        return mw_codes_json[key][str(val)]
    except:
        pass

def to_lower(s):
    try:
        return str(s).lower()
    except:
        pass

def to_int_str(s):
    try:
        return str(int(float(s)))
    except:
        pass

def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]                        

# def decode(val, key):
#     """
#         Takes a column value and column heading
#         and returns non-coded value text         
#     """
#     try: 
#         val = int(val)
#     except:
#         pass
#     if re.match('priority[1-6]', key):
#         return mw_codes_json['choices'][str(val)]
#     elif val != 'None':
#         try:
#             return mw_codes_json[key][str(val)]
#         except:
#             pass
#     else:
#         pass    
