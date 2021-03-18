from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd
import re
import io

print('heehee')

baseURL = 'https://www.fincaraiz.com.co'

#url = "https://www.fincaraiz.com.co/apartamento-casa/venta/cali/?ad=30|1||||1||8,9|||82|8200006||||||||||||||||1|||1||griddate%20desc||||-1||"
#page = requests.get(url)
#soup = BeautifulSoup(page.content, 'html.parser')

#eq = soup.find_all('a')

links=[]

with io.open("scrapingfr2.csv","w", encoding="utf8") as f1:
	f1.write("url; Ubicacion; Tipo de vivienda; Estado; Anios del inmueble; Habitaciones; Banios; Parqueaderos; Area Privada; Area Construida; Estrato; Piso\n")

for i in range(0, 300):
	i=i+1
	url="https://www.fincaraiz.com.co/apartamento-casa/venta/cali/?ad=30"
	url=url+"|"+str(i)+"|"+"|||1||8,9|||82|8200006||||||||||||||||1|||1||griddate%20desc||||-1||"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	eq = soup.find_all('a')
	for e in eq:
		try:
			if '.aspx' in e.get('href') and 'https' not in e.get('href') and ('casa' in e.get('href') or 'apartamento' in e.get('href')):
				links.append(baseURL+e.get('href'))
		except:
			print('bad link')

print(len(links))

for link in links:
	try:		
		privateArea='0'
		constArea='0'
		floor='0'
		antiqueness='NaN'

		site = requests.get(link)
		soup2 = BeautifulSoup(site.content, 'html.parser')

		#Precio de la vivienda obtenido de la informacion de la pagina web
		price=soup2.find('div', class_='price').getText()
		price = re.sub(r"\s+"," ", price)

		#Cantidad de habitaciones obtenida de la informacion de la pagina web
		rooms=soup2.find('span', class_='advertRooms').getText()
		rooms=(re.sub(" Habitaciones: ","", rooms)).strip()

		#Cantidad de baños obtenido de la informacion de la pagina web
		baths=soup2.find('span', class_='advertBaths').getText()
		baths=(re.sub("Baños: ","", baths)).strip()

		#Cantidad de parqueaderos obtenido de la informacion de la pagina web
		parkingLots=soup2.find('span', class_='advertGarages').getText()
		if 'Sin especificar' in parkingLots:
			parkingLots='NaN'
		else:
			parkingLots=(re.sub("Parqueaderos: ","", parkingLots)).strip()
		state=soup2.find('div', class_='badge').getText()

		info = soup2.find('ul', class_='boxcube').getText()
		info = re.sub(r"\s+"," ", info)

		placeType=''
		if 'apartamento' in link:
			placeType='apartamento'
			if 'Piso No: ' in info:
				floor=info.split('Piso No: ')[1]
				floor=floor.split('º ')[0]
		else:
			placeType='casa'
			if 'Piso No: ' in info:
				floor=info.split('Piso No: ')[1]
				floor=floor.split('º ')[0]
			else:
				floor='1'

		estrato=info.split(' Estrato: ')[1]
		if 'Estado' in estrato:
			estrato=estrato.split(' Estado: ')[0]
		elif 'Antigüedad' in estrato:
			estrato=estrato.split(' Antigüedad: ')[0]
		elif ' Piso ' in estrato:
			estrato=estrato.split(' ')[0]
		else:
			estrato=estrato.split(' Sector: ')[0]

		neighborhood=info.split(' Sector: ')[1]
		if 'Ver Mapa' in neighborhood:
			neighborhood='NaN'

		if 'Antigüedad' in info:
			antiqueness=info.split(' Antigüedad: ')[1]
			if 'Más de ' in antiqueness:
				antiqueness=antiqueness.split('Más de ')[0]
			elif 'Menos de ' in antiqueness:
				antiqueness=antiqueness.split('Menos de ')[0]
			else:
				antiqueness=antiqueness.split(' ')[0]

		if 'Área privada' in info:
			privateArea=info.split('Área privada: ')[1]
			privateArea=privateArea.split(' m²')[0]

			constArea=info.split('Área Const.: ')[1]
			constArea=constArea.split(' m² ')[0]
		elif 'Área Const' in info:
			constArea=info.split('Área Const.: ')[1]
			constArea=constArea.split(' m² ')[0]
		else:
			pass

		neighborhood = re.sub(r"\s+"," ", neighborhood)
		antiqueness = re.sub(r"\s+"," ", antiqueness)
		floor = re.sub(r"\s+"," ", floor)
		rooms = re.sub(r"\s+"," ", rooms)
		baths = re.sub(r"\s+"," ", baths)
		parkingLots = re.sub(r"\s+"," ", parkingLots)
		privateArea = re.sub(r"\s+"," ", privateArea)
		constArea = re.sub(r"\s+"," ", constArea)
		estrato = re.sub(r"\s+"," ", estrato)
		price = re.sub(r"\s+"," ", price)
		data=link+";"+neighborhood+";"+placeType+";"+state+";"+antiqueness+";"+rooms+";"+baths+";"+parkingLots+";"+privateArea+";"+constArea+";"+estrato+";"+floor+"\n"
		#print(data)
		with io.open("C:/users/c/Desktop/scrapingfr2.csv", "a", encoding="utf8") as f1:
			f1.write(data)
			f1.close()
	except:
		print('hee hee. WRONG!')


print("Finish, Se acabó, Se fini xd")
