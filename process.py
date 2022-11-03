
def parse():
  '''
  Parsing Data from Word document
  '''
  import sys
  #from time import sleep
  import re
  import docx


  c=0
  afd=None
  doc=docx.Document('data/VAN_DER_LINDE_20161031.docx')
  pars=doc.paragraphs
  footnotes=[]
  tl=[]
  pnum=1
  for par in pars:
    txt=par.text
    if 'HOOF STAMBOOM' in txt:
      #print(txt)
      afd=txt
    elif 'ANDER IMMIGRANTE' in txt:
      #print(txt)
      afd=txt
    elif 'ONGEKOPPELDES' in txt:
      #print(txt)
      afd=txt
    c+=1
    if afd=='HOOF STAMBOOM':
      for s,r in zip(['\t',"‘","“",'’'],[' ',"'",'"',"'"]):
        txt=txt.replace(s,r)
      if len(txt)>0: # if not an empty line
        if re.search('^[0-9]+[ ]*[A-Za-z]*',txt): # if the line starts with a number
          #print(f'txt: {len(txt):03} "{txt[0:100]}"')
          if len(txt)<=3: # probably the page number
            pnum=int(txt)
            #print(f'{c:03}: pagenum: {pnum}')
          elif re.search(r'^[1-9]{1,3}[ ]?[A-Za-z]',txt): # otherwise a footnote
            footnoteVal,footnoteText=re.search(r'^([1-9]{1,3})[ ]?([A-Za-z].*)',txt).groups()
            print(f'{pnum} {footnoteVal}, {footnoteText}')
            dat={}
            dat['page']=pnum
            dat['ref']=footnoteVal
            dat['text']=footnoteText
            footnotes.append(dat)
        else:
          #print(f'{txt[:100]} ')
          tl.append(txt)
          k,v='',''
          if re.search(r'^[\[\(]?[A-Za-z][0-9]+[\]\)]? ',txt):
            k,v=re.search(r'^([\[\(]?[A-Za-z][0-9]+[\]\)]?)(.*)',txt).groups()
            v=v.strip()
            #print(f'{k:^4}: {v}')
          else: 
            k=None
            v+=txt
            #print(f'"{txt}"')
          if k is not None:
            if re.search(' [A-Za-z][0-9]{1,2} ',v): 
              res=re.split('([\[\(]?[A-Za-z][0-9]{1,2}[\]\)]?)', txt.strip())
              res.pop(0)
              for i in range(0,len(res),2):
                #print(f"{pnum} {res[i]}: {res[i+1].strip()}")
                split_parts(pnum, res[i],res[i+1].strip())
              #if c>1320: return footnotes, tl
            else:
              #print(f'{pnum} {k}: {v.strip()}')
              split_parts(pnum, k,v.strip())
              #pass
        #if c>=1800: return footnotes, tl
          
  return footnotes, tl

def split_parts(pnum, index, datstr):
  import re
  global c
  # extract index classifier
  if '[' in index: 
    idx_type='other'
  elif '(' in index: 
    idx_type='adopted'
  else: 
    idx_type='vdl'
  #then trip the index of it's classifier tokens
  for v in ['[',']','(',')']:
    index=index.strip(v)
  # then extract exception gender specifiers
  if '(v)' in datstr[:40].lower():
    gender='female'
    #c+=1; print(f'{c} {index} {datstr}')
  elif '(m)' in datstr[:35].lower():
    gender='male'
    #c+=1; print(f'{c} {index} {datstr}')
  else:
    gender=None
  if '(x)' in datstr[:100].lower(): # (x) - not married
    #c+=1; print(f'{c} {index} {datstr[:100]}')
    married=False
  if '*' in datstr.lower(): # born
    #res=re.split(r'(\*|\+|~| x |#)',datstr)
    #c+=1; print(f'{c} {index} {datstr}')
    pass

if __name__ == '__main__':
  c=0
  print('='*200)
  d=parse()
  