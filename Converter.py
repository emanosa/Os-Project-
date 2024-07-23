# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 14:40:57 2023

@author: alxan
"""
from Directory_Entry import Directory_Entry

class Converter(object):
    
    @classmethod
    def IntArrToBytes(self,array):
        bytess=bytes()
        for i in range(0, len(array)):
            b = array[i].to_bytes(4,'big',signed=True)
            bytess += b
        return bytess
    
    
   # @classmethod
  #  def IntArrToBytes(self,array):
   #     bytess=bytes(array)
    #    return bytess
    
    @classmethod
    def BytesArrToInts(self,bytess):
        ints=list()
        for i in range(0, len(bytess),4):
            ints += ([int.from_bytes(bytess[i:i+4],'big',signed=True)])
        return ints
    
   # @classmethod
   # def BytesArrInts(self,bytess):
    #    ints=list(bytess)
     #   return ints
    
    @classmethod
    def splitBytes(self,Bytes):
        ls=list()
        if len(Bytes) > 0:
            number_of_arrays = int(len(Bytes) / 1024);
            rem = int(len(Bytes) % 1024);
            for i in range(0, number_of_arrays):
                b=Bytes[(i*1024):((i+1)*1024)]
                ls.append(b)
            if rem > 0:
                br=Bytes[number_of_arrays*1024:]
                b=br+(0).to_bytes(1024-rem, 'big',signed=True)
                ls.append(b)
        else:
            v = 0
            b= v.to_bytes(1024,'big',signed=True)
            ls.append(b)
        return ls
    
    @classmethod
    def Directory_EntryToBytes(self,d):
        Bytes=bytes()
        Bytes+=bytes(d.dir_name)
        if len(d.dir_name) < 11:
            for i in range(len(d.dir_name), 11):
                Bytes+=b'\0'
        Bytes+=d.dir_attr.to_bytes(1,'big',signed=True)
        Bytes+=d.dir_empty()
        Bytes+=d.dir_firstCluster.to_bytes(4,'big',signed=True)
        Bytes+=d.dir_filesize.to_bytes(4,'big',signed=True)
        return Bytes
    
    @classmethod
    def BytesToDirectory_Entry(self,B):
        name=self.BytesToString(B[:11])
        attr=int.from_bytes(B[11], 'big',signed=True)
        empty = B[12:24]
        firstCluster=int.from_bytes(B[24:28], 'big',signed=True)
        fileSize=int.from_bytes(B[28:], 'big',signed=True)
        d = Directory_Entry(name, attr, firstCluster)
        d.dir_empty = empty
        d.dir_filesize = fileSize
        return d
        

    @classmethod
    def BytesToString(self,B):
        stri=""
        for i in range(0, len(B)):
            if B[i] != b'\0':
                stri += str(B[i])
            else:
                break
        return stri