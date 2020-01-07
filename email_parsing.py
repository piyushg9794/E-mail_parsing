#importing required libraries

import os
import pathlib
import re
import pandas as pd


#defining function for pattern searching in downloaded e-mail's backup

def getEmailCounts(path1=path_of_folder, field='To', pattern='([<].*@[^>]*)'):
    emails_dict=dict()
    
    # Looping through all the downloaded e-mails of extinsion .eml
    
    for path, subdirs, files in os.walk(path1):
        for name in files:
		
            # Skipping the sql lite file, all other files are email files downloaded during backup of e-mails
	
            if(name.endswith('sqlite')):
                continue
                
            # Creating a handle on the file for performing furthur operations
            
            hand=open(pathlib.PurePath(path, name))
            index=0
            
            for line in hand:
                index+=1
                email=''
		
                # Applying the condition to find pattern
		
                if line.startswith(field+":"):
                    email=re.findall(pattern,line)[0][1:]
                    print(email)
                    emails_dict[email]=emails_dict.get(email,0)+1
                    
    #sorting processed e-mails

    emails_dict=dict(sorted(emails_dict.items(), key=lambda x:x[1],reverse=True))



#calling function1

getEmailCounts(path_of_folder, 'To', '([ <].*@[^>\n ]*)')

#function to get the maximum time slot, the maximum recepient, the maximum sender and best friend

def getStats(path1=path_of_folder, emailidPersonal=your_email):
    data = pd.DataFrame(columns=['fromEmails', 'toEmails', 'dates','hrs','emails'])
    
    # Looping through..
    
    for path, subdirs, files in os.walk(path1):
        index=0
        for name in files:
            
            # Skipping the sql lite file, all other files are email files
            
            if(name.endswith('sqlite')):
                continue
                
            hand=open(pathlib.PurePath(path, name))
            FromEmail=''
            ToEmail=''
            dateExt=''
            pattern1 = '([<].*@[^>\n ]*)' # pattern1 to regex
            pattern2 = '([ ].*@[^>\n ]*)' # pattern2 to regex
            
            #extracting the email ids, the time and the hour slot
            
            for line in hand:
                if line.startswith("To:"):
                    if (len(re.findall('[<]',line)))>0:
                        ToEmail=re.findall(pattern1,line)[0][1:]
                    else:
                        ToEmail=re.findall(pattern2,line)[0][1:]
                elif line.startswith("From:"):
                    if (len(re.findall('[<]',line))):
                        FromEmail=re.findall(pattern1,line)[0][1:]
                    else:
                        FromEmail=re.findall(pattern2,line)[0][1:]
                elif line.startswith("Date:"):
                    dateExt=re.findall("[ ].*[ \n]",line)[0].strip()
                    hourSlot=dateExt.split(" ")[4].split(":")[0]
                    
            # Appending to the data frame(pandas)
            
            index+=1
            data.loc[index] = [FromEmail, ToEmail, dateExt, hourSlot, FromEmail]
            index+=1
            data.loc[index] = [FromEmail, ToEmail, dateExt, hourSlot, ToEmail]
            
    # Sorting to get the maximums on the top
    
    topTimes=data[(data["fromEmails"] != emailidPersonal)].groupby(['hrs']).agg('count')['fromEmails'].sort_values(ascending =False)
    topFrom=data.groupby(['fromEmails']).agg('count')['toEmails'].sort_values(ascending =False)
    topTo=data.groupby(['toEmails']).agg('count')['fromEmails'].sort_values(ascending =False)
    topConvo=data.groupby(['emails']).agg('count')['fromEmails'].sort_values(ascending =False)
    print(topTimes[0:5])
    print(topFrom[0:5])
    print(topTo[0:5])
    print(topConvo[0:5])
    
    print('-----------------------------------------------------')
    
    # Displaying the results
    
    print('Top hour slot at which emails were sent: '+topTimes.index[0])
    
    if len(topFrom)>1 and topFrom.index[0] == (emailidPersonal) :
        print('Top sender of emails: '+topFrom.index[1])
    elif len(topFrom)>0:
        print('Top sender of emails: '+topFrom.index[0])
    else:
        print('No emails were received by the user')
        
        
    if len(topTo)>1 and topTo.index[0] == (emailidPersonal) :
        print('Top recepient of emails: '+topTo.index[1])
    elif len(topTo)>0:
        print('Top recepient of emails: '+topTo.index[0])
    else:
        print('No emails sent')
        
        
    if len(topConvo)>1 and topConvo.index[0] == (emailidPersonal):
        print('Top friend: '+topConvo.index[1])
    elif len(topConvo)>0:
        print('Top friend: '+topConvo.index[0])
    else:
        print('No top friend')
		
		
# Calling the function2

getStats(path_of_folder,emailid)
