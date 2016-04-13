from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	geo=getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	client_id="OKU5DPCCSVTEIHLZQBXOLCOLINZF2JCMYPDYJHUXIKAYCKDX"
	client_secret="53I453NZJEBEVSCXUIMYYXGBBDXDFFCUYHYPQVFKA5M5XS43"
	url=('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20160412&ll=%s,%s&query=%s'%(client_id,client_secret,geo[0],geo[1],mealType))
	h=httplib2.Http()
	resultFound=json.loads(h.request(url,'GET')[1])
	if resultFound['response']['venues']:
	#3. Grab the first restaurant
		restaurant=resultFound['response']['venues'][0]
		venue_id=restaurant['id']
		restaurant_name=restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		url=('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20160412'%(venue_id,client_id,client_secret))
		result=json.loads(h.request(url,'GET')[1])
		address=""
		for i in restaurant_address:
			address +=i+" "
		restaurant_address=address
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		if result['response']['photos']['items']:
			firstpicture=result['response']['photos']['items'][0]
			prefix=firstpicture['prefix']
			suffix=firstpicture['suffix']
			imageURL=prefix+"300x300"+suffix
		else:
			imageURL = "https://www.google.com"

		restaurantInfo={'name':restaurant_name,'address':restaurant_address,'image':imageURL}
		return restaurantInfo
	else:
		return "NO Restaurant Found!"
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
