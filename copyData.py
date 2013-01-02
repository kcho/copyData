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
import glob

#time to make the destination folder name in /volume1
timeAtRun = time.gmtime()
destinFolderName = str(timeAtRun.tm_year) + '_' + str(timeAtRun.tm_mon) + '_' + str(timeAtRun.tm_mday)
#sourceDirectory = os.path.abspath('/Users/mav88/Dropbox/python/exampleNas/')
sourceDirectory = os.path.abspath('/Volumes/LG_HDD/MRI_data/lab_data')
def main():
    '''
    asks the user for the input
    group + subjectNum + modalities
    '''
    groupList = group()
    allSubjectSources = subject(groupList) #[0]:group [1]:subjectNum [2]:datasource
    sourcesToCopy = modality(allSubjectSources)

#checking whether the modalities in the subject exist
def group():
    '''
    returns groups entered by the user
    '''
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



def subject(groupList):
    '''
    returns the data source address of the
    subject numbers entered by the user
    '''
    allSubjectSources=[]
    if len(groupList) == 1:
        groupList.append('justPass')
    for i in groupList:
        if i =='justPass':
            continue
        subjectNums = raw_input('''
    -------in {0}--------
    type the subject numbers separated by spaces
    eg.04 02 11 40
    :'''.format(i)).split(' ')
    #now chekcing whether it exists in the target
        for subjectNum in subjectNums:
            targetSource = glob.glob(os.path.join(sourceDirectory,i)+'/'+i+subjectNum+'*')
            if targetSource:
                print '{0} is matched to {1}'.format(str(i)+str(subjectNum),targetSource)
                allSubjectSources.append((i,subjectNum,targetSource))
            else:
                print '{0} does not exist in {1}'.format(str(i)+str(subjectNum),i)
    return allSubjectSources


def modality(allSubjectSources):
    '''
    from the glob.glob pattern of the address of
    all type of modalities of the subjects,
    returns the address of user's choice
    which is appended to a list for later backup
    '''
    t1Comp = re.compile(r'\w*(?<!s)t1\w*|\w*tfl\w*',flags=2)
    t2flairComp = re.compile(r'\w*flair\w*',flags=2)
    t2tseComp = re.compile(r'\w*tse\w*',flags=2)
    rest4060Comp = re.compile(r'^.*rest(?:(?!15).)*',flags=2) #includes REST4060 & REST152
    rest152Comp = re.compile(r'^.*rest\S*152\S*',flags=2) #includes REST4060 & REST152
    dtiComp = re.compile(r'^.+dti(?:(?!COLFA|EXP|FA).)*$',flags=2)
    dkiComp = re.compile(r'^.+dki(?:(?!COLFA|EXP|FA).)*$',flags=2)

    sourcesToCopy = []

    modalities = raw_input('''
    type the modalities separated by spaces
    eg.T1 T2TSE T2FLAIR REST4060 REST152 DTI DKI
    :''').split(' ')
    allModalities = ['T1','T2FLAIR','T2TSE','REST4060','REST152','DTI','DKI']
    if [item for item in modalities if item not in allModalities]:
        print 'make sure the modalities you entered are spelled right'
        group,subjNum,datasource = modality(allSubjectSources)
    for groupNumSourcetup in allSubjectSources:
        allImageDirectories = glob.glob(os.path.abspath(''.join(groupNumSourcetup[2]))+'/*/*')
        T1s = filter(t1Comp.search,allImageDirectories)
        T2FLAIRs = filter(t2flairComp.search,allImageDirectories)
        T2TSEs = filter(t2tseComp.search,allImageDirectories)
        REST4060s = filter(rest4060Comp.search,allImageDirectories)
        REST152s = filter(rest152Comp.search,allImageDirectories)
        DTIs = filter(dtiComp.search,allImageDirectories)
        DKIs = filter(dkiComp.search,allImageDirectories)
        modalComps=[T1s,T2FLAIRs,T2TSEs,REST4060s,REST152s,DTIs,DKIs]

        for modality,modalComp in zip(allModalities,modalComps):
            if modality in modalities:
                if modalComp != '':
                    sourcesToCopy.append(modalComp)
                    print modalComp
                else:
                    print '{0} is missing in {1}'.format(modality,groupNumSourcetup[0]+str(groupNumSourcetup[1]))

       return sourcesToCopy

if __name__ == '__main__':
    main()

