# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:17:33 2023

@author: alxan
"""
#import Virtual_Disk.Virtual_Disk
import os

class Run(object):
    current = None
    currentPath = ""
    @classmethod
    def main(self):
        os.system("cls")
        print("Welcome to OS_Project_Virtual_DISK_shell ^_^\n\ndeveloped by KHALED ELTURKY\n\n")
        Virtual_Disk.Virtual_Disk.CREATEorOPEN_Disk("VirtualDisk")
        self.currentPath = self.current.dir_name
        while (True):
            self.current.readDirectory()
            incmd = input(self.currentPath+ "\\" + ">>>>>>")
            #Parser.parse(incmd)
            print(incmd)

Run.main()
