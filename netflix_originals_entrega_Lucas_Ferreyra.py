######################### Hecho por Lucas Ferreyra para el desafio de Business Bureau. ########################
#pip3 install bs4 
from urllib.request import urlopen as url_request # #is going to grab the page 
from bs4 import BeautifulSoup as soup #to parse the HTML text

my_url = "https://www.netflix.com/ar/browse/genre/839338" #Originales de Netflix ARGENTINA.
# (El unico catalogo de Netflix q me deja ver sin iniciar sesion)

page = url_request(my_url) #descargando la pagina 
page_raw = page.read() #leo y guardo en page_raw todos los datos q descargue en el paso anterior
page.close() #cierro la conexión

page_soup = soup(page_raw, "html.parser") #soup me lo parsea como html, que es lo que quiero
containers = page_soup.findAll("li", {"class":"nm-content-horizontal-row-item"}) #conteiner de las originals de netflix


titles_already_sorted = [] #Agrego esta lista vacia porque voy a appendar los titulos que ya guardé. 
#Observando el catalogo de netflix originals, muchas series y peliculas se repiten y no quiero la repeticion de los datos.

#Lo voy a exportar como csv.
filename = "netflix_originals_arg.csv" 
with open(filename, "w", encoding="utf-8") as f:
	headers = "Type, Title, Duration, Year Released, Genre, Public, Cast, Created by, Description, URL" + "\n"
	f.write(headers)


	for container in containers:
		url_films=container.a["href"]
		#Mismo proceso que antes: voy a descargar la pagina donde esta la información de cada serie/película
		#Desde ahi, busco las variables que necesito.
		page = url_request(url_films)
		page_raw = page.read()
		page.close()
		page_soup = soup(page_raw, "html.parser")
        
		if ((page_soup.find("h1", {"class":"title-title", "data-uia":"title-info-title"})).text not in titles_already_sorted):
			title = (page_soup.find("h1", {"class":"title-title", "data-uia":"title-info-title"})).text
			titles_already_sorted.append(title)
			if ( page_soup.find("span", {"class":"title-info-metadata-item item-year", "data-uia": "item-year" }) == None):
				year = "No hay informacion"
			else:
				year = (page_soup.find("span", {"class":"title-info-metadata-item item-year", "data-uia": "item-year" })).text
			if (page_soup.find("span", {"class":"maturity-number"}) == None):
				pd= "No hay informacion"
			else:
				pd=((page_soup.find("span", {"class":"maturity-number"})).text)
			duration = (page_soup.find("span", {"class":"duration"})).text
			if("temporada" in duration): #Me di cuenta que todas las series tienen la palabra "temporada(s))" (aveces no tiene s cuando es 1 sola temporada)
				type = "Serie"
			else:
				type = "Película"
			if(page_soup.find("a", {"data-uia":"item-genre"}) == None):
				genre = "No hay informacion"
			else:
				genre = (page_soup.find("a", {"data-uia":"item-genre"})).text
			synopsis = (page_soup.find("div", {"class": "title-info-synopsis"})).text
			if(page_soup.find("span", {"class": "title-data-info-item-list", "data-uia":"info-starring"}) == None): #aveces no está la informacion, como este caso.
				cast = "No hay informacion"
			else:
				cast = (page_soup.find("span", {"class": "title-data-info-item-list", "data-uia":"info-starring"})).text
			if (page_soup.find("div", {"class": "title-data-info-item item-creators"}) == None ):
				created = "No hay informacion"
			else:
				created = (page_soup.find("span", {"class": "title-data-info-item-list", "data-uia":"info-creators"})).text
	        
			print(title)
	        
			f.write(type + "," + title.replace(",","|") + "," + duration + "," + year + "," + genre.replace(",","|") + "," + pd + "," + cast.replace(",", "|")+ "," + created.replace(",","|") + "," + synopsis.replace(",","|")+ ","+ url_films + "\n")