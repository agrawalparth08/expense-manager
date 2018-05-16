import pandas as pd
import regex as re
import matplotlib.pyplot as plt

#getting from excel
df = pd.read_excel("sms-20180101-214545.xls", sheetname="Sheet1")
colsToDrop = ['Slot']
df = df.drop(colsToDrop, axis=1)
all_sms = df.values.tolist()

#dividing into sent and recieved messages
sent = [all_sms[i] for i in range(len(all_sms)) if all_sms[i][3]=='Sent']
recieved =  [all_sms[i] for i in range(len(all_sms)) if all_sms[i][3]=='Inbox']

#dividing by special character header name
hsbc = [recieved[i][4] for i in range(len(recieved)) if 'HSBC: Your credit card' in recieved[i][4]]
yes = [recieved[i][4] for i in range(len(recieved)) if 'spent on your YES' in recieved[i][4]]

data_hsbc = []
for i in range(len(hsbc)):
    words = hsbc[i].split()
    entity = re.search('at(.*)\. ', hsbc[i])
    date = [int(x) for x in words[11].split('/')]
    date.reverse()
    #print(date)
    data = [float(words[9]),date,entity.group(1)]
    data_hsbc.append(data)
    
data_yes = []   
for i in range(len(yes)):
    amt = re.search('INR(.*)\has',yes[i])
    entity = re.search('at(.*)\on',yes[i])
    dater = re.search('../../....',yes[i])
    date =[int(x) for x in dater.group(0).split('/')]
    date.reverse()
    data = [float(amt.group(1).replace(',','')),date,entity.group(1)]
    data_yes.append(data)

data_hsbc.sort(key=lambda x: x[1])
data_yes.sort(key=lambda x: x[1])
total_data = data_hsbc + data_yes

monthly_data = [[] for i in range(12)]

for msg in data_yes:
    for i in range(1,13):
        if msg[1][1] == i:
            monthly_data[i-1].append(msg)
for msg in data_hsbc:
    for i in range(1,13):
        if msg[1][1] == i:
            monthly_data[i-1].append(msg)            
total_spent = [0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(12):
    for j in range(len(monthly_data[i])):
        total_spent[i] += monthly_data[i][j][0]
        

#plotting for monthly

labels_month = 'Jan','Feb','March','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
sizes = [round(total_spent[i]/sum(total_spent),2) for i in range(len(total_spent))]
#sizes = [8,8,8,8,8,8,8,8,8,8,8,12] 
#explode = (0,0.1,0,0,0,0,0,0,0,0,0,0)   
year_spent = "Expenditure for 2017 \n INR " + str(sum(total_spent)) +"\n"
fig1,ax1 = plt.subplots()
fig1 = plt.gcf()
fig1.set_size_inches(12,12)
ax1.set_title(year_spent,fontsize="15")
ax1.pie(sizes,labels=labels_month,autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.savefig('monthly.png',bbox_inches='tight')
plt.show()          

#plotting for spent on which item
merchants = []
for i in range(len(total_data)):
    merchants.append([total_data[i][0],total_data[i][2]])
merchants.sort(key=lambda x: x[1])
   
merchant_names = [merchants[i][1] for i in range(len(merchants))]
group_list = dict()
for c,n in merchants:
    if n not in group_list:
        group_list[n] = 0
    if n in merchant_names:
        group_list[n] +=c

#categorical labels        
movies=['cinepolis','bookmyshow','book','bigtree']
wallet = ['mobi','one97','paytm','freec','payu','phonepe']
food = ['zomato','pizza','mcd','falafal','mocca','mocha']
ecommerce = ['amazon','fipkart','snapdeal','lenskart']
travel=['redbus','yatra','goibibo']
daily = ['grofer']
tech = ['goog','faceb','udemy']
telephone = ['bharti','airtel','spectra',]
competitive_exams = ['ibps','iibf','rpsl','jasper','nielit']
domain_list = {'Movies':0,'Wallet':0,'Food':0,'E-Commerce':0,'Travel':0,'DailyNeeds':0,'Tech':0,'Telephone':0,'Exams':0}

#Populating dictionary
for k,v in group_list.items():
    if any(word in k.lower() for word in movies):
        domain_list['Movies'] += v    
    if any(word in k.lower() for word in wallet):
        domain_list['Wallet'] += v
    if any(word in k.lower() for word in food):
        domain_list['Food'] += v
    if any(word in k.lower() for word in ecommerce):
        domain_list['E-Commerce'] += v
    if any(word in k.lower() for word in travel):
        domain_list['Travel'] += v
    if any(word in k.lower() for word in daily):
        domain_list['DailyNeeds'] += v
    if any(word in k.lower() for word in tech):
        domain_list['Tech'] += v
    if any(word in k.lower() for word in telephone):
        domain_list['Telephone'] += v
    if any(word in k.lower() for word in competitive_exams):
        domain_list['Exams'] += v
 
#plotting categorical
labels_category = [k for k,v in domain_list.items()]
labels_category.append('Other')
cost_category = [v for k,v in domain_list.items()]
cost_category.append(sum(total_spent)-sum(cost_category))

print(sum(cost_category))
sizes_category = [round(cost_category[i]/sum(total_spent),2) for i in range(len(cost_category))]
#sizes = [8,8,8,8,8,8,8,8,8,8,8,12] 
#explode = (0,0.1,0,0,0,0,0,0,0,0,0,0)   
year_spent = "Categorical Expenditure for 2017 \n INR " + str(sum(total_spent)) +"\n"
fig2,ax2 = plt.subplots()
fig2 = plt.gcf()
fig2.set_size_inches(12,12)
ax2.set_title(year_spent,fontsize="15")
ax2.pie(sizes_category,labels=labels_category,autopct='%1.1f%%', startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig2.savefig('category.png',bbox_inches='tight')
plt.show()        



