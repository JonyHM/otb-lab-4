import time
import datetime
import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt

con = cx_Oracle.connect(
  user="system",
  password="fatec",
  dsn="localhost/LOCALDB",
  encoding="UTF-8")

cur = con.cursor()
index = 1

statement = '''SELECT DISTINCT SAL_ID FROM SALARY ORDER BY SAL_ID ASC'''
cur.execute(statement)
info = cur.fetchall()

## HARD
print('HARD')
hardInit = datetime.datetime.now()

for value in info:
  salId = value[0]
  statement = f'''SELECT * FROM SALARY WHERE SAL_ID = {salId}'''
  cur.execute(statement)
  select = cur.fetchone()
  index += 1
  if index == 100000:
    break

hardEnd = datetime.datetime.now()
hardDiff = hardEnd - hardInit

print(hardInit)
print(hardEnd)
print(hardEnd - hardInit)

## SOFT
print('SOFT')
index = 1
softInit = datetime.datetime.now()

statement = f'''SELECT * FROM SALARY WHERE SAL_ID = :bind'''
for value in info:
  salId = value[0]
  bind= {"bind" : salId}
  cur.execute(statement, bind)
  select = cur.fetchone()
  index += 1
  if index == 100000:
    break

softEnd = datetime.datetime.now()
softDiff = softEnd - softInit

print(softInit)
print(softEnd)
print(softEnd - softInit)

cur.close()
con.close()

data = [
  ['Hardcoded', hardDiff.total_seconds()],
  ['Softcoded', softDiff.total_seconds()]
]
  
df = pd.DataFrame(data, columns=['Modo de acesso','Tempo de execução (ms)'])
print (df)

df.plot(x ='Modo de acesso', y='Tempo de execução (ms)', kind = 'bar')
plt.show()