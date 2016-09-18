from bs4 import BeautifulSoup
import requests

url = "https://www.packtpub.com"
agent = 'Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.0'

# Your Account
email = ""
password = ""

form_build_id = ""
form_id = ""

# Get form for login
index_page = BeautifulSoup(requests.get(url, headers={'User-Agent':agent}).text, "html.parser")
form_login = index_page.find("form", {"id": "packt-user-login-form"})

for input in form_login.find_all("input"):
	if input.get('type') == 'hidden':
		if input.get('name') == "form_build_id":
			form_build_id = input.get("value")
		else:
			form_id = input.get("value")

# Login data
data = {'email': email, 'password' : password, 'op' : 'Login', 'form_build_id' : form_build_id, 'form_id' : form_id }

# Create session and send data for login
session = requests.Session()
session.post(url, data=data,headers={'User-Agent':agent})

# Get free learning page and url of free ebook
url_free_learning = url + "/packt/offers/free-learning"
free_learning = BeautifulSoup(session.get(url_free_learning,headers={'User-Agent':agent}).text, "html.parser")

div_claim_book = free_learning.find("div", {"class": "float-left free-ebook"})
url_claim_book = url + div_claim_book.find("a").get('href')

free_ebook_today = free_learning.find("div", {"class": "dotd-title"}).find('h2').text


# Claim free ebook
get_free_book = BeautifulSoup(session.get(url_claim_book,headers={'User-Agent':agent}).text, "html.parser")

print("\n.::: CLAIM PACKTPUB's FREE EBOOK :::.");

print("\nFree eBook today: %s" %free_ebook_today.strip());
print("URL to claim free eBook: %s" %url_claim_book)

# LIST of your ebook
print("\nLists of your eBooks")
print("-------------------")

i = 1
list_claimed_book = get_free_book.find("div", {"id": "product-account-list"})

for book in list_claimed_book.find_all("div", {"class": "product-line unseen"}):
	print("%i. %s" %(i,book.get('title')))
	i += 1

