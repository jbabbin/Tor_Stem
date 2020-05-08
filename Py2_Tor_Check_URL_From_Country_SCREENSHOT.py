################################################################
#
# Title: Geo-Location Website retrieval 
# Author: CTC - Jake Babbin Copper River 
# Date: 6 May 2020  
#
# REQUIREMENTS: 
# 	Tor client with control port available for STEM library 
#	chromium library for headless browser connection 
#   Python Libraries: 
#	selenium 
#	Webdriver 
#	Stem (used for Tor)
#	PycURL
#	simplejson (or json) 
#	requests
#
# USAGE:
#  prompt> python check_url_from_country.py <2_letter_country_name> <URL_to_download> 
#
# TODO: 
#
# BUGS: 
#
# VERSION:
#	2.0 - Added screenshot capture for screenshots (Selenium and chromium) 
#
################################################################
#
#
###### Python Modules 
import io
import pycurl
import sys
import requests
import simplejson
import stem.process
from stem.util import term
from tld import get_tld


################### GLOBAL CONFIG 
SOCKS_PORT = 9050 # orig 7000
sockshost='192.168.1.5' # Tor host (use real IP versus localhost for selenium 


#################### Handle Input 

# Take input from CLI 
if (len(sys.argv)-1 == 0):
        print "NO CLI Arguments, exiting"
        print "Need a value to check"
        print " Example: python this_file.py <short url> "
	print " python this_file.py http://url or https://url" 
        sys.exit(1)
else:
        num_args = len(sys.argv)-1
        if num_args > 3:
                print "ERROR: Too many arguments"
                print "Try again"
                sys.exit(1)

country = sys.argv[1]
check_url = sys.argv[2]

#DEBUG 
print "This is the Country [" + country + "] and this is the URL [" + check_url + "] \n"

# Pull FQDN 
info = get_tld(check_url, as_object=True)
FQDN = info.fld 
FQDN_STR = FQDN.replace('.', '_') 

#DEBUG 
print("Domain with Extenstion: ", info.fld)
print("Domain for FileName: ", FQDN_STR) 

################## Build Tor STEM connection 
# Needs Tor to NOT be running to function
def query(url):
  """
  Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
  """

  output = io.BytesIO()

  query = pycurl.Curl()
  query.setopt(pycurl.URL, url)
  query.setopt(pycurl.PROXY, 'localhost')
  query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
  query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
  query.setopt(pycurl.WRITEFUNCTION, output.write)

  try:
    query.perform()
    return output.getvalue()
  except pycurl.error as exc:
    return "Unable to reach %s (%s)" % (url, exc)

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.GREEN))


print(term.format("Starting Tor:\n", term.Attr.BOLD))

fcountry = "{" + country + "}"

tor_process = stem.process.launch_tor_with_config(
	config = { 
		'SocksPort': str(SOCKS_PORT),
		'StrictNodes': '1',
		'ExitNodes': str(fcountry),
	},
	init_msg_handler = print_bootstrap_lines,
)

print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
print(term.format("Tor Client Info \n", term.Attr.BOLD))
print(term.format(query("https://ifconfig.me/ip"), term.Color.GREEN))
print(term.format("\n Check Endpoint against Official Tor \n", term.Attr.BOLD))
print(term.format(query("https://check.torproject.org/api/ip"), term.Color.GREEN))
# 
print(term.format("\nChecking URL " + check_url, term.Attr.BOLD))
#print(term.format(query(check_url), term.Color.GREEN))
# use requests 
response = requests.get(check_url, stream=True)
response_code = response.status_code
response_code_str = str(response_code)
print(term.format("\n Response Received: " + response_code_str, term.Attr.BOLD))
response_server_header = response.headers
print(term.format("\n Server Header", term.Attr.BOLD))
print(simplejson.dumps(dict(response.headers), indent=4, sort_keys=False))
Size_Response_bytes = len(response.content)
Size_Response_bytes = str(Size_Response_bytes)
print(term.format("\nWriting to URL Disk " + Size_Response_bytes + " bytes", term.Attr.BOLD))

path_str = FQDN_STR + "_Web_Content_file.html"
with open(path_str, 'wb') as f:
	for chunk in response.iter_content(chunk_size=1024): 
		if chunk: # filter out keep-alive new chunks
			#print "WRITING CONTENT TO DISK "
			f.write(chunk)
			f.flush()
#print(term.format("\n DONE File available at:" + path_str, term.Attr.BOLD))

tor_process.kill()  # stops tor

############### Make another conection to take a screenshot 
from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
import time

login = "test"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-setuid-sandbox")

chromeOptions.add_argument("--remote-debugging-port=9222")  # this

chromeOptions.add_argument("--disable-dev-shm-using")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("start-maximized")
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--window-size=1920, 1680")
# add Tor support
#sockshost='192.168.1.5'
socksport='9050'
chromeOptions.add_argument("--proxy-server=socks5://" + sockshost + ":" + socksport)
#
chromeOptions.add_argument(r"user-data-dir=.\cookies\\" + login)
b = webdriver.Chrome(chrome_options=chromeOptions)
# Make new URL
# Save to png
#b.get("http://www.amazon.com")
#b.save_screenshot('screen_shot.png') 

b.get(check_url) 
screenshot_file_name = FQDN_STR + "_screen_shot.png" 
b.save_screenshot(screenshot_file_name) 
#print(term.format("\nScreen Shot available " + screenshot_file_name, term.Attr.BOLD))
b.close()
b.quit()

print(term.format("\n DONE File available at:" + path_str, term.Attr.BOLD))
print(term.format("\nScreen Shot available " + screenshot_file_name, term.Attr.BOLD))

###################### Done ######################

