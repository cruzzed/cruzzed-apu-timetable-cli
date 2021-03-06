import requests
import sys
import time

#this functions returns arguments
#separated by spaces provided by user
#when opened from command line
#or when using the interactive console
def sysargs(sysargv, argsdictionary):
    sysarg = [sys.upper() for sys in sysargv]
    if sysarg[0] == '/?' or sysarg[0] == '/help':
        help()
        exit()
    else:
        print(sysarg)
        argsdict = {}
        for b in range(len(argsdictionary[0])):
            if (argsdictionary[0][b] in sysarg):
                argsdict[str(argsdictionary[1][b])] = sysarg[sysarg.index(argsdictionary[0][b])+1]
    return argsdict

def argsdictionary():
   return list([["/IN","/MOD","/LEC","/DAY","/DATE","/ST","/ET","/LOC","/GRP"],["INTAKE","MODID","NAME","DAY","DATESTAMP","TIME_FROM","TIME_TO","LOCATION","GROUPING"]])

#main function

def main():
    if (len(sys.argv)) < 2:
        try:
            help()
            print("Enter commands without 'timetable.py'.")
            print("Press Ctrl+C to exit.")
            while(True):
                arguments = input(">>>\t")
                arguments = arguments.split(" ")
                print(arguments)
                parsing(sysargs(arguments,argsdictionary()))
        except:
            print("Error, Program exiting...")
            exit()
    else:
        parsing(sysargs(sys.argv[1:], argsdictionary()))
        exit()

#API Parser function
def parsing(argsdict):
    #api URL
    URL = "https://s3-ap-southeast-1.amazonaws.com/open-ws/weektimetable"
    #open URL
    data = requests.get(URL).json()
    print("API retrieved in: %s seconds" % (time.time() - start_time))
    return search(data, argsdict) #continues to search phase which takes API data and system arguments

#Search function based on flags,
#it will only take schedules
#that perfectly matches
#the arguments and value given
def search(schedules, argsdict):
    search_time=time.time()
    listofschedule = []
    count = int(0)
    countt = int(0)
    for scheduledict in schedules:
        flag = int(0)
        for a,b in argsdict.items():
            for x,y in scheduledict.items():
                countt = countt + 1
                if (a == x):
                    if b in y:
                        flag = flag+1
                        if (flag == len(argsdict)):
                            listofschedule.append(scheduledict)
                        break
                    else:
                        break
        count = count + 1
    print("Data filtered in: {0} seconds for total of {1} schedules for all classes available, with each schedules containing {2} data.".format((time.time() - search_time), count, countt))
    return formatter(listofschedule) #continues to format the values phase

#format and print function
def formatter(list):
    form_time = time.time()
    for v in list:
        print('''~~~\t {modid} \t~~~
Intake: {intake}
Lecture Name: {lec}
Module Code: {modid}
Day and Date: {day} {date}
Time Start and Finish: {tf}-{tt}
Location: {loc}
Grouping: {group}'''
        .format(modid = v["MODID"]
            ,intake = v["INTAKE"]
            ,lec = v["NAME"]
            ,day = v["DAY"]
            ,date = v["DATESTAMP"]
            ,tf = v["TIME_FROM"], tt =v["TIME_TO"]
            ,loc= v["LOCATION"]
            ,group = v["GROUPING"])
            )
    print("Data printed in: %s seconds" % (time.time() - form_time))

#help page function
#will be called upon
#no arguments provided or
#arguments such as /? or /help provided
#then exits the application
def help():
    print('''
Asia Pacific University Timetable Command Line Interface v1.0
Usage: .\\timetable.py /arg value /arg value /arg value

        /? or /help: Show help page and exits.
        /in: Used to search a schedule based on the intake.
        /loc:                    ...                location.
        /lec:                    ...                lecturer name.
        /mod:                    ...                module code.
        /day:                    ...                day.
        /date:                   ...                date.
        /start:                  ...                start time.
        /end:                    ...                end time.
        /grp:                    ...                grouping.
Example: timetable.py /in UC2F1908SE /mod dmtd /date 01
Output:  ~~~      CT015-3-2-DMTD-T-2     ~~~
        Intake: UC2F1908SE
        Lecture Name: CENSORED
        Module Code: CT015-3-2-DMTD-T-2
        Day and Date: FRI 01-MAY-20
        Time Start and Finish: 09:30 AM-10:30 AM
        Location: NEW CAMPUS
        Grouping: T2
        ''')

if __name__ == '__main__':
    start_time = time.time()
    main()
