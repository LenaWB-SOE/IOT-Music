import datetime
import statistics as st

weekday = datetime.datetime.today().weekday()
print(weekday)

data = [1,2,3,4,5]
average = st.mean(data)
print(average)
hi = 1


if isinstance(hi, int):
    print("Yes")