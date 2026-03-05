#!/usr/bin/env python 
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import re

def html_to_text(html,name,save=False):
    
    class_is_multi= { '*' : 'class'}
    parsed_html = BeautifulSoup(html,'xml', multi_valued_attributes=class_is_multi)
    a=parsed_html.body.find(attrs={"table table-BCRA table-bordered table-hover table-responsive"})
    s=str(a)
    s=re.sub('</td>\n<td style=\"text-align:right\">',"", s)
    s=re.sub('\\t',"", s)
    s=re.sub('\n\n',"\t", s)
    s=re.sub('<(.*)>',"",s)
    s=re.sub('\n\n',"\n", s)
    s=re.sub('\n\n',"\t", s)
    s=re.sub('\t\n',"\n", s)


    if save:
        text_file = open(name+'.txt', "w")
        text_file.write(s[2:-1])
        text_file.close()
    return s
