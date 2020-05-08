
# Tor_Stem

Scripts to help investigators/analysts use Tor and Python STEM library to investigate hostile websites

Tor provides a Python binding library called STEM that allows for interaction with a Tor client that allows tools to leverage the anonymity that Tor provides.   

[https://stem.torproject.org/](https://stem.torproject.org/)
Stem is a Python controller library for [Tor](https://www.torproject.org/). With it you can use Tor's [control protocol](https://gitweb.torproject.org/torspec.git/tree/control-spec.txt) to script against the Tor process, or build things such as [Nyx](https://nyx.torproject.org/). Stem's latest version is **1.8** (released December 29th, 2019).

These example scripts provide some use cases that investigators or analysts might find useful when performing actions such as: 

 - `Py2_Tor_Check_URL_From_Country.py`
Connect to a website in a specific Country 
        Simple connect, read headers and download the content 
 - `Py2_Tor_Check_URL_From_Country_SCREENSHOT.py`
 Grab a screenshot of the website from the country (useful for takedowns and evidence) 
 <B>Note: This requires additional libraries and tools Python Selenium and Chromium to create a headless browser. </B> 
 - `Py2_Utility_Show_ExitNodes_BeingUsed.py`
 Show Exit nodes while Tor is in use 
 - `Py2_Utility_Tor_Connection_Status.py`
 Show Tor client status information

 # Requirements 
 **Python Modules:** 
 Stem - `pip install stem` 
 requests - `pip install requests` 
 pycurl - `pip install pycurl` 
 simplejson (or json) - `pip install simplejson` 
 selenium - `pip install selenium` 
 webdriver (part of chromium python) - `pip install chromedriver-install` 
 tld (used to create filename) - `pip install tld` 

**Tools:** 
Chromium (used for the headless browser connection to take screenshots) 

----------
<H3> Setup Tor client </H3>
The Tor client does NOT have to be on the same system as these scripts; the tor client just has to have the following settings in the 'torrc' configuration file. 

    #This is the IP and port for clients to use to connect
    # with the SOCKS5 proxy information 
    SOCKSPort 192.168.1.5:9050
    # Use this setting if the Tor client is on another 
    # machine but in your local network 
    SOCKSPolicy accept 192.168.1.0/24 
    # OPTIONAL Log files (useful for debugging tor issues) 
    Log notice file /var/log/tor/notices.log 
    Log debug file /var/log/tor/debug.log 
    # STEM Controller Library Configurations 
    ControlPort 9051 
    # Enable authentication if other systems can access the host Tor 
    # client is running on 
    # HashedControlPassword SUPERSECRETLONGPASSPHRASE
    # CookieAuthentication 1 
    


<h3> Examples </h3> 

#1 Simple Website grab content 

        python Py2_Tor_Check_URL_From_Country.py ES https://news.google.com
    This is the Country [ES] and this is the URL [https://news.google.com
    ('Domain with Extenstion: ', u'google.com')
    ('Domain for FileName: ', u'google_com')
    Starting Tor:
    May 08 11:47:54.000 [notice] Bootstrapped 0%: Starting
    May 08 11:47:55.000 [notice] Bootstrapped 80%: Connecting to the Tor network
    May 08 11:47:56.000 [notice] Bootstrapped 85%: Finishing handshake with first hop
    May 08 11:47:57.000 [notice] Bootstrapped 90%: Establishing a Tor circuit
    May 08 11:47:58.000 [notice] Bootstrapped 100%: Done
    Checking our endpoint:
    Tor Client Info
    88.218.17.43
    Check Endpoint against Official Tor
    {"IsTor":true,"IP":"88.218.17.43"}
    Checking URL https://news.google.com
    Response Received: 200
    Server Header
    {
    "Strict-Transport-Security": "max-age=31536000",
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": "script-src 'nonce-ouOdEzIUiYJUAOpNTY/yzA' 'unsafe-inline';object-src 'none';base-uri 'self';report-uri /_/DotsSplashUi/cspreport;worker-src 'self'",
    "Content-Encoding": "gzip",
    "Transfer-Encoding": "chunked",
    "Set-Cookie": "GN_PREF=W251bGwsIkNBRVNEQWl6X3RYMUJSQ0Frb193QWciXQo_; Expires=Sat, 07-Nov-2020 03:48:03 GMT; Path=/; Secure",
    "Expires": "Mon, 01 Jan 1990 00:00:00 GMT",
    "Server": "ESF",
    "X-XSS-Protection": "0",
    "x-ua-compatible": "IE=edge",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache, no-store, max-age=0, must-revalidate",
    "Date": "Fri, 08 May 2020 15:48:03 GMT",
    "X-Frame-Options": "SAMEORIGIN",
    "Alt-Svc": "h3-27=\":443\"; ma=2592000,h3-25=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q049=\":443\"; ma=2592000,h3-Q048=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"",
    "Content-Type": "text/html; charset=utf-8"
    }
    Writing to URL Disk 2743196 bytes
    DONE File available at:google_com_Web_Content_file.html

#2 Same with Screenshot (Chromium headless grab) 

    python Py2_Tor_Check_URL_From_Country_SCREENSHOT.py MX http://pclcon.site
    This is the Country [MX] and this is the URL [http://pclcon.site]
    ('Domain with Extenstion: ', u'pclcon.site')
    ('Domain for FileName: ', u'pclcon_site')
    Starting Tor:
    May 08 11:52:11.000 [notice] Bootstrapped 0%: Starting
    May 08 11:52:12.000 [notice] Bootstrapped 80%: Connecting to the Tor network
    May 08 11:52:13.000 [notice] Bootstrapped 85%: Finishing handshake with first hop
    May 08 11:52:14.000 [notice] Bootstrapped 90%: Establishing a Tor circuit
    May 08 11:52:15.000 [notice] Bootstrapped 100%: Done
    Checking our endpoint:
    Tor Client Info
    200.56.44.184
    Check Endpoint against Official Tor
    {"IsTor":true,"IP":"200.56.44.184"}
    Checking URL http://pclcon.site
    Response Received: 200
    Server Header
    {
    "X-Powered-By": "PHP/7.2.30",
    "Transfer-Encoding": "chunked",
    "Keep-Alive": "timeout=5, max=1000",
    "Server": "Apache",
    "Connection": "Keep-Alive",
    "Link": "<http://pclcon.site/wp-json/>; rel=\"https://api.w.org/\", <http://pclcon.site/>; rel=shortlink",
    "Date": "Fri, 08 May 2020 15:52:19 GMT",
    "Content-Type": "text/html; charset=UTF-8"
    }
    Writing to URL Disk 76578 bytes
    DONE File available at:pclcon_site_Web_Content_file.html
    Screen Shot available pclcon_site_screen_shot.png


#3 Utility Tor Status 

    python Py2_Utility_Tor_Connection_Status.py
    Our platform supports connection resolution via: proc, netstat, lsof, ss (picked proc)
    Tor is running with pid 7320
    Connections:
    192.168.1.5:50900 => 5.154.174.241:443


#4 Utility Tor Connections (Useful when running Tor searches to show connections) 
  (check out nyx as well for a realtime terminal to Tor usage )


