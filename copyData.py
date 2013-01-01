#!/usr/bin/python
#kcho
#Tue 01 Jan 2013 00:21:54
'''
this script
gets following inputs from the user
- group
- subject
- modality
then add those target data in a list
which are copied at the end
in the /volume1/`date`
'''
import os
import re
import time

#time to make the destination folder name in /volume1
timeAtRun = time.gmtime()
destinFolderName = str(timeAtRun.tm_year) + '_' + str(timeAtRun.tm_mon) + '_' + str(timeAtRun.tm_mday)

def main():
    '''
    asks the user for the input
    group + subjectNum + modalities
    '''
    groupList = group()

    subjectNum = subject(groupList)
    modalities = raw_input('''
    type the modalities separated by spaces
    eg.rest t1 dti dk
    :''').split(' ')

#checking whether the modalities in the subject exist
def group():
    groupList = raw_input('''
    list the groups to copy separated by spaces
    eg.CHR NOR GHR
    :''').split(' ')
    allGroups = ['CHR','DNO','EMO','FEP','GHR','NOR','OCM','ONS','OXY','PAIN','SPR','UMO']
    if [item for item in groupList if item not in allGroups]:
        print 'make sure the groups you entered are spelled right'
        group()
    else:
        return groupList



Tue 01 Jan 2013 00:53:00
'''%%%%%start from here
make a code that concatanates the groupname(i) with the number
input then check whether it exist in the data source'''
def subject(groupList):
    for i in groupList:
        subjectNum = raw_input('''
        -------in {0}--------
        type the subject numbers separated by spaces
        eg.04 02 11 40
        :'''.format(i)).split(' ')


#def modality():





if __name__ == '__main__':
    main()

