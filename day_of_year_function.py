month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def date2list(date):
    datelist = []
    d = " "
    for i in range(len(date)):
            if date[i] == "-":
              datelist.append(d)
              d = " "
            elif i == len(date)-1:
              d += date[i]
              datelist.append(d)
            else:
             d += date[i]
    return datelist

def day_in_year(date, days=month_days):
        
    date_list = date2list(date)
    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])
        
    if leap_year(year):
        month_days[2] = 29

    for i in range(1, len(month_days)):
        month_days[i] += month_days[i-1]
    
    previous_month = month_days[month -1]
    return previous_month + day

date = input("Enter a date in the format of YYYY-MM-DD: ")
d = day_in_year(date, month_days)
print(d)