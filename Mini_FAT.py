# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 14:15:33 2023

@author: alxan
"""
from Converter import Converter
import Virtual_Disk

class Mini_FAT(object):
    
    _FAT=[0]*1024
    
    @classmethod
    def createFAT(self):
        for i in range(0, len(self._FAT)):
            if i == 0 or i == 4:
                self._FAT[i]=-1
            elif i > 0 and i <= 3:
                self._FAT[i]=i+1
            else:
                self._FAT[i]=0
    
    @classmethod
    def writeFAT(self):
        FATBYTES = Converter.IntArrToBytes(self._FAT)
        ls = Converter.splitBytes(FATBYTES)
        for i in range(0, len(ls)):
            Virtual_Disk.Virtual_Disk.writeCluster(ls[i], i+1)
    
    @classmethod 
    def readFAT(self):
        b=bytes()
        for i in range(0, 4):
            b += (Virtual_Disk.Virtual_Disk.readCluster(i+1))
        self._FAT = Converter.BytesArrToInts(b)
        
    @classmethod
    def printFAT(self):
        print("The FAT has the following:\n")
        for i in range(0, 10):
            print("FAT["+str(i)+"] = "+str(self._FAT[i])+"\n")
    
    @classmethod
    def getAvilableCluster(self):
        for i in range(0, len(self._FAT)):
            if self._FAT[i]==0:
                return i
        return -1
    
    @classmethod
    def getAvilableClusters(self):
        s=0
        for i in range(0, len(self._FAT)):
            if self._FAT[i]==0:
                s+=1
        return s
    
    
    @classmethod
    def getClusterStatus(self,clusterIndex):
        if clusterIndex >= 0 and clusterIndex < len(self._FAT):
            return self._FAT[clusterIndex]
        else:
            return -1
    
    
    @classmethod
    def setClusterStatus(self,clusterIndex,clusterStatus):
        if clusterIndex >= 0 and clusterIndex < len(self._FAT):
            self._FAT[clusterIndex] = clusterStatus
    
    
    
    