# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 21:26:25 2023

@author: alxan
"""
from Directory_Entry import Directory_Entry
from Mini_FAT import Mini_FAT
from Virtual_Disk import Virtual_Disk
import Converter.Converter
import Run.Run

class Directory(Directory_Entry):
    DirOrFiles=list()
    Parent=None
    
    def __init__(self, name, dir_attr, dir_firstCluster,pa):
        Directory_Entry.__init__(self,name, dir_attr, dir_firstCluster)
        self.DirOrFiles=list()
        if pa != None:
            self.Parent=pa
            
    def GetMyDirectory_Entry(self):
        me=Directory_Entry(self.dir_name, self.dir_attr, self.dir_firstCluster)
        me.dir_empty=self.dir_empty
        me.dir_filesize=self.dir_filesize
        return me
    
    def getMySizeOnDisk(self):
        size = 0
        if self.dir_firstCluster != 0:
            cluster = self.dir_firstCluster
            nextc = Mini_FAT.getClusterStatus(cluster)
            if cluster == 5 and nextc == 0:
                return size
            while cluster != -1:
                size+=1
                cluster=nextc
                if cluster != -1:
                    nextc = Mini_FAT.getClusterStatus(cluster)
        return size
    
    def emptyMyClusters(self):
        if self.dir_firstCluster != 0:
            cluster = self.dir_firstCluster
            nextc = Mini_FAT.getClusterStatus(cluster)
            if cluster == 5 and nextc == 0:
                return
            while cluster != -1:
                Mini_FAT.setClusterStatus(cluster, 0)
                cluster=nextc
                if cluster != -1:
                    nextc = Mini_FAT.getClusterStatus(cluster)
    
    def canAddEntry(self,d):
        can = False
        neededSize = (len(self.DirOrFiles) + 1) * 32
        neededClusters = int(neededSize / 1024)
        rem = int(neededSize % 1024)
        if rem > 0:
            neededClusters+=1
        neededClusters += int(d.dir_filesize / 1024)
        rem1= int(d.dir_filesize % 1024)
        if rem1 > 0:
            neededClusters+=1
        if (self.getMySizeOnDisk() + Mini_FAT.Mini_FAT.getAvilableClusters() >= neededClusters):
            can = True
        return can
    
    def readDirectory(self):
        if self.dir_firstCluster != 0:
            self.DirOrFiles=list()
            cluster = self.dir_firstCluster
            nextc = Mini_FAT.getClusterStatus(cluster)
            if cluster == 5 and nextc == 0:
                return
            lsBytes=bytes()
            while cluster!=-1:
                lsBytes += Virtual_Disk.readCluster(cluster)
                cluster=nextc
                if cluster != -1:
                    nextc = Mini_FAT.getClusterStatus(cluster)    
            for i in range(0, len(lsBytes),32):
                if (i+1)*32 < len(lsBytes):
                    b=lsBytes[i*32:(i+1)*32]
                else:
                    b=lsBytes[i*32:]
                if b[0] == b'0':
                    break
                self.DirOrFiles.append(Converter.BytesToDirectory_Entry(b))
    
    def writeDirectory(self):
        o = self.GetMyDirectory_Entry()
        if len(self.DirOrFiles) != 0:
            dirsorfilesBYTES = bytes()
            for i in range(0, len(self.DirOrFiles)):
                dirsorfilesBYTES += Converter.Converter.Directory_EntryToBytes(self.DirOrFiles[i])
            bytesls = Converter.splitBytes(dirsorfilesBYTES)
            clusterFATIndex = -1
            if self.dir_firstCluster != 0:
                    #empty all its clusters
                self.emptyMyClusters()
                clusterFATIndex = Mini_FAT.Mini_FAT.getAvilableCluster()
                self.dir_firstCluster = clusterFATIndex
            else:
                clusterFATIndex = Mini_FAT.Mini_FAT.getAvilableCluster()
                if clusterFATIndex != -1:
                    self.dir_firstCluster = clusterFATIndex
            lastCluster = -1
            for i in range(0,len(bytesls)):
                if (clusterFATIndex != -1):
                    Virtual_Disk.Virtual_Disk.writeCluster(bytesls[i], clusterFATIndex)
                    Mini_FAT.Mini_FAT.setClusterStatus(clusterFATIndex, -1)
                    if (lastCluster != -1):
                        Mini_FAT.Mini_FAT.setClusterStatus(lastCluster, clusterFATIndex)
                    lastCluster = clusterFATIndex
                    clusterFATIndex = Mini_FAT.Mini_FAT.getAvilableCluster()
            if (len(self.DirOrFiles) == 0):
                if (self.dir_firstCluster != 0):
                    self.emptyMyClusters()
                if (self.Parent != None):
                    self.dir_firstCluster = 0
            n = self.GetMyDirectory_Entry()
            if (self.Parent != None):
                self.Parent.updateContent(o,n)
                self.Parent.writeDirectory()
            Mini_FAT.Mini_FAT.writeFAT()
    
    def searchDirectory(self, name):
        self.readDirectory()
        for i in range(0,len(self.DirOrFiles)):
            n = self.DirOrFiles[i].dir_name
            if (n == name):
                return i
        return -1
    
    def deleteDirectory(self):
        self.emptyMyClusters()
        if (self.Parent != None):
            self.Parent.removeEntry(self.GetMyDirectory_Entry())
        if (Run.Run.current == self):
            if (self.Parent != None):
                Run.Run.current = self.Parent
                Run.Run.currentPath = Run.Run.currentPath[:len(Run.Run.currentPath)-len(self.dir_name)-1]
                Run.Run.current.readDirectory()
        Mini_FAT.Mini_FAT.writeFAT()

    def updateContent(self, OLD, NEW):
        self.readDirectory()
        index = self.searchDirectory(OLD.dir_name)
        self.DirOrFiles.pop(index)
        self.DirOrFiles.append(NEW)

    def addEntry(self, d):
        self.DirOrFiles.append(d)
        self.writeDirectory()

    def removeEntry(self, d):
        self.readDirectory()
        index = self.searchDirectory(d.dir_name)
        self.DirOrFiles.pop(index)
        self.writeDirectory()