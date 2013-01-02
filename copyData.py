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


bcolours from blender-build scripts
http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = "\033[1m"

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD = ''

def main():
    '''
    asks the user for the input
    group + subjectNum + modalities
    '''
    groupList = group()
    allSubjectSources = subject(groupList)
    #allSubjectSources 'yes|no','group+subjectNum','datasource|x'
    sourcesToCopy,modalitiesEntered = modality(allSubjectSources)
    #sourcesToCopy:[0]folderName with initial [1]modality Entered [2]target image folder
    copyWithLog(modalitiesEntered,sourcesToCopy,allSubjectSources)



#checking whether the modalities in the subject exist
def group():
    '''
    returns groups entered by the user
    '''
    groupList = raw_input('''
    list the groups to copy separated by spaces
    eg.CHR NOR GHR
    :''').upper().split(' ')
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
    :'''.format(i)).upper().split(' ')
    #now chekcing whether it exists in the target
        for subjectNum in subjectNums:
            targetSource = glob.glob(os.path.join(sourceDirectory,i)+'/'+i+subjectNum+'*')
            if targetSource:
                print '{0} is matched to {1}'.format(str(i)+str(subjectNum),targetSource)
                allSubjectSources.append(('yes',str(i)+str(subjectNum),targetSource))
            else:
                print bcolors.FAIL +'{0} does not exist in {1}'.format(str(i)+str(subjectNum),i) + bcolors.ENDC
                allSubjectSources.append(('no',str(i)+str(subjectNum),'x'))

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
    rest4060Comp = re.compile(r'^.*(?:(?!152))rest.*',flags=2) #includes REST4060 & REST152
    rest152Comp = re.compile(r'^.*rest\S*152\S*',flags=2) #includes REST4060 & REST152
    dtiComp = re.compile(r'^.+dti(?:(?!COLFA|EXP|FA).)*$',flags=2)
    dkiComp = re.compile(r'^.+dki(?:(?!COLFA|EXP|FA).)*$',flags=2)

    sourcesToCopy = []
    noImageSource = []

    modalitiesEntered = raw_input('''
    type the modalities separated by spaces
    eg.T1 T2TSE T2FLAIR REST4060 REST152 DTI DKI
    :''').upper().split(' ')
    allModalities = ['T1','T2FLAIR','T2TSE','REST4060','REST152','DTI','DKI']
    if [item for item in modalitiesEntered if item not in allModalities]:
        raise NameError('make sure the modalities you entered are spelled right'
)

    for yngroupNumSourcetup in allSubjectSources:
        if yngroupNumSourcetup[0] == 'yes':
            allImageDirectories = glob.glob(os.path.abspath(''.join(yngroupNumSourcetup[2]))+'/*/*')
            folderNameWithInitial = os.path.basename(''.join(yngroupNumSourcetup[2]))
            T1s = filter(t1Comp.search,allImageDirectories)
            T2FLAIRs = filter(t2flairComp.search,allImageDirectories)
            T2TSEs = filter(t2tseComp.search,allImageDirectories)
            REST4060s = filter(rest4060Comp.search,allImageDirectories)
            REST152s = filter(rest152Comp.search,allImageDirectories)
            DTIs = filter(dtiComp.search,allImageDirectories)
            DKIs = filter(dkiComp.search,allImageDirectories)
            modalComps=[T1s,T2FLAIRs,T2TSEs,REST4060s,REST152s,DTIs,DKIs]

            for modality,modalComp in zip(allModalities,modalComps):
                if modality in modalitiesEntered:
                    if len(modalComp) == 1:
                        sourcesToCopy.append((folderNameWithInitial,modality,modalComp))
                    elif len(modalComp) >= 2:
                        print bcolors.FAIL + '\t{0} has more than one {1}, choose one among'.format(str(yngroupNumSourcetup[0])+str(yngroupNumSourcetup[1]),modality) + bcolors.ENDC
                        for foundfolder,num in zip(modalComp,range(len(modalComp))):
                            print '\t\t{1}:{0}\n'.format(foundfolder,num)
                        choice = raw_input(':')
                        modalComp = modalComp[int(choice)]
                        sourcesToCopy.append((folderNameWithInitial,modality,modalComp))
                    else:
                        print bcolors.FAIL + '\t\t{0} is missing in {1}'.format(modality,yngroupNumSourcetup[0]+str(yngroupNumSourcetup[1])) + bcolors.ENDC

                        sourcesToCopy.append((folderNameWithInitial,modality,'x'))


                        for item in allImageDirectories:
                            print '\t\t |{0}'.format(item)
        else:
            sourcesToCopy.append(('x','x','x'))

    return sourcesToCopy,modalitiesEntered



def copyWithLog(modalitiesEntered,sourcesToCopy,allSubjectSources):
#sourcesToCopy:[0]folderName with initial [1]modality Entered [2]target image source
#allSubjectSources 'yes|no','group+subjectNum','datasource|x'
#SUBJECT Subject_folder_matched Modality[0] Modality[1] etc ...
    logSubject=[]
    logSubjectMatched=[]
    logModality=[]

    for i in allSubjectSources:
            logSubject.append(i)

    for modality in modalitiesEntered:
        print modality
        for i in logSubject:
            for if i == modality:
                print i[0],
                print i[2]



if __name__ == '__main__':
    main()

