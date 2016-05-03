import csv
import time
import datetime
import os

contactListName = raw_input("What's the name of the list of merchants you'd like to contact?")
masterListName = raw_input("What's the name of the master list against which you're comparing this list?")
contactThreshold = raw_input("How many days do you want to place between today and the last time those merchants were contacted?")

#create a new file in which to add approved merchants
cleanedListName = contactListName+'.csv' 
filename, file_extension = os.path.splitext(contactListName)
cleanedListName = filename+'_cleaned'+file_extension

#establish the contact threshold in days
contactThresholdDays = datetime.timedelta(days=int(contactThreshold))
today_date = datetime.date.today()

with open(masterListName, 'rU') as csvfile:
    
    csvReaderMaster = csv.reader(csvfile,delimiter=',')
    
    headerMaster = csvReaderMaster.next()
    
    storeIDPositionMaster = headerMaster.index("Store ID")
    dateContactedPositionMaster = headerMaster.index("Date contacted")
    
    csvReaderMasterList=list(csvReaderMaster)
    #csvReaderMasterList = [l for l in csvReaderMaster]
    with open(contactListName,'rU') as csvfile:
        
        csvReaderContact = csv.reader(csvfile,delimiter=',')

        #capturing the header and advancing the reader to the next line
        headerContact = csvReaderContact.next()

        #finding the positions of 'Store ID' and 'Date contacted' in the header
        storeIDPositionContact = headerContact.index("Store ID")
   
        csvReaderContactList = list(csvReaderContact)
        #csvReaderContactList = [l for l in csvReaderContact]       

        with open(cleanedListName, 'w') as csvfile:
            writerCleaned = csv.writer(csvfile)
            writerCleaned.writerow(headerContact)
            
            i=0
            count_matches = 0
            count_cleaned = 0
            for rowContact in csvReaderContactList: 
                #look for store ID's that are similar
                writeFlag=True
                for rowMaster in csvReaderMasterList:
                    if rowMaster[storeIDPositionMaster]==rowContact[storeIDPositionContact]:
                        count_matches+=1
                        #if we have a match, we should compare the dates
                        dateContacted = datetime.datetime.strptime(rowMaster[dateContactedPositionMaster], '%Y-%m-%d').date()
                        #if the difference is greater than the threshold, write the row to the clean file
                        if today_date - dateContacted > contactThresholdDays:
                            #now update the date so we can change it in the master list later
                            csvReaderMasterList[i][dateContactedPositionMaster]=str(today_date); 
                        else:
                            writeFlag = False
                        
                if writeFlag:
                    #write the same line to the cleaned file
                    writerCleaned.writerow(rowContact)
                    count_cleaned+=1              
                i+=1
        print("We found "+str(count_matches)+" merchants who have been contacted previously.")
        print("Of those, " +str(count_cleaned)+" were contacted more than "+contactThreshold+" days ago.")
                
        #update master list
        i=0
        j=0
        with open(masterListName, 'w') as csvfile:
            writerMaster = csv.writer(csvfile)
            writerMaster.writerow(headerMaster)

                
            for rowMaster in csvReaderMasterList:
                writerMaster.writerow((csvReaderMasterList[i][storeIDPositionMaster],csvReaderMasterList[i][dateContactedPositionMaster]))      
                i+=1
                
            #open up the cleaned contact list  
            with open (cleanedListName, 'rU') as csvfile:
                csvReaderCleaned = csv.reader(csvfile,delimiter=',')
                headerCleaned = csvReaderCleaned.next()
                storeIDPositionCleaned = headerCleaned.index("Store ID")
                csvReaderCleanedList = list(csvReaderCleaned)
                
                #write those lines to the master list
                for rowCleaned in csvReaderCleanedList:
                    writerMaster.writerow((csvReaderCleanedList[j][storeIDPositionCleaned],str(today_date)))
                    j+=1
