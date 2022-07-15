import csv
import sqlite3 as s
from datetime import date

cn = s.connect('datalog.db')
c = cn.cursor()

def drop_table():
	with cn:
		c.execute("drop table if exists log")
		c.execute("drop table if exists res")
drop_table()
def create_table():
	with cn:
		c.execute("""
			create table if not exists log(
			datime text,
			email text,
			subject text
		)""")
		c.execute("create table if not exists res(name text, result integer)")
create_table()

def obteniendo_datos():
#abriendo csv y creando tabla con los datos
	with open('Log QCP 2022 - Form Responses 1.csv', 'r', encoding='utf-8') as f:
		data = csv.reader(f)
		#recorriendo los datos leídos
		with cn:
			for d in data:
				#generando cada registro
				c.execute("insert into log values(:d, :e, :s)", {'d':d[0], 'e':d[1], 's':d[3]})
obteniendo_datos()

def leyendo_datos():
	hoy = date.today()
	with cn:
		if input('Mostrar mes completo? (y/n) ') == 'y':
			for mi in miembros:
				c.execute(f"select * from log where email like '{mi}%' and datime like '{hoy.month}%'")
				c.execute("insert into res values(:name, :result)", {'name':mi.upper(), 'result':len(c.fetchall())} )
			c.execute("select * from res order by result desc")
			data = c.fetchall()
			for dat in data:
				print(f"{dat[0]}: {dat[1]}")

		else:
			for mi in miembros:
				c.execute(f"select * from log where email like '{mi}%' and datime like '{hoy.month}/{hoy.day}%'")
				c.execute("insert into res values(:name, :result)", {'name':mi.upper(), 'result':len(c.fetchall())} )
			c.execute("select * from res order by result desc")
			data = c.fetchall()
			for dat in data:
				print(f"{dat[0]}: {dat[1]}")

miembros = ['josias', 'melissa', 'juan', 'jonathan', 'jaider', 'marlon', 'kevin']
leyendo_datos()
		
