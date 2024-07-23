# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:17:16 2023

@author: alxan
"""
import os
import Mini_FAT
import Directory.Directory
import Run.Run

class Virtual_Disk(object):
    
    Disk=None
    
    @classmethod
    def CREATEorOPEN_Disk(self,path):
        try:
            if os.path.exists(path): #the virtual disk exists
                self.Disk=open(path,"r+b") #open it
                Mini_FAT.Mini_FAT.readFAT() #read the FAT array from the disk 
                root = Directory("K:", 0x10, 5, None)
                root.readDirectory()
                Run.current = root
            else:
                self.Disk=open(path,"bx") #the virtual disk does not exist (producing of virtual disk phase)
                for i in range(0, 1024):
                    self.writeCluster(b'0'*1024, i) #write 1MB as zeros to the disk becuase our disk has 1024 cluster and every cluster is 1024 bytes so make our virtual disk of size 1MB and is empty
                Mini_FAT.Mini_FAT.createFAT() # initalize the FAT array
                Mini_FAT.Mini_FAT.writeFAT() #write the FAT array to the disk
                root = Directory("K:", 0x10, 5, None)
                Run.current = root
        except:
            print("An error occuered while openning the Disk!\n")
            
    @classmethod
    def writeCluster(self,cluster,clusterIndex):
        self.Disk.seek(clusterIndex*1024,0) # move the pointer of writing to the beginning of the location of our cluster
        self.Disk.write(cluster) #write our cluster on that location
        self.Disk.flush() #force the write order to be executed on the file now
    
    @classmethod
    def readCluster(self,clusterIndex):
        self.Disk.seek(clusterIndex * 1024, 0)
        bytess=bytes()
        bytess += self.Disk.read(1024)
        return bytess
    
    @classmethod
    def getLogicalFreeSpace(self):
        return Mini_FAT.Mini_FAT.getAvilableClusters()*1024
    
    