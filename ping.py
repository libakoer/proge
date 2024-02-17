import ping, socket
try:
    ping.verbose_ping('www.arturtamm.site', count=3)
    delay = ping.Ping('www.wikipedia.org', timeout=2000).do()
except socket.error:
    print ("Ping Error:", e