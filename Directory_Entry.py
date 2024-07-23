# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 19:14:31 2023

@author: alxan
"""

class Directory_Entry(object):
    dir_name=""
    dir_attr=0x0
    dir_empty=[b'0'*12]
    dir_firstCluster=0
    dir_filesize=0
    
    def __init__(self,name,dir_attr,dir_firstCluster):# the directory entry constructor
        self.dir_attr=dir_attr
        name= self.CleanTheName(name)
        if self.dir_attr == 0x0:
            fileName=name.split('.')
            self.assignFileName(fileName[0], fileName[1])
        elif self.dir_attr == 0x10:
            self.assignDIRName(name)
        self.dir_firstCluster=dir_firstCluster
        self.dir_empty=[b'0'*12]
    
    def CleanTheName(self,s):#remove the following characters from the name of the directory entry or you can print error message to the user to tell him not to include these characters in the name of a file or a directory
            if s != "K:":
                n = ""
                for c in s:
                    if c != (' ') and c != ('?') and c != ('؟') and c != ('>') and c != ('<') and c != ('|') and c != (':') and c != ('*') and c != ('\'') and c != ('\\') and c != ('/'):
                        n += c
                return n
            else:
                return s
    
    def assignFileName(self, name, extension):# assign a file name as name part and then . and then the extension with caring that the length of dir_name is less than 11
        if len(name) <= 7 :
            self.dir_name+=name+'.'
        else:
            self.dir_name+=name[:7]+'.'
        if len(extension) <= 3 :
            self.dir_name += extension
        else:
            self.dir_name += extension[:3]
        self.dir_name=self.dir_name.upper()
    
    def assignDIRName(self, name):# assign a directory name as one part the name only with caring that the length of dir_name is less than 11
        if len(name) <= 11:
            self.dir_name=name
        else:
            self.dir_name=name[:11]
            