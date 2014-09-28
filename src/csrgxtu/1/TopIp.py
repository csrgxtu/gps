from Download import Download
import time

IP_FILE = "./static/ip.txt"
TOP_FILE = "./static/top.txt"

# getIps
# read ips from ip.txt
#
# @param filePath
# @return ipList
def getIps(filePath):
  with open(filePath, "r") as myFile:
    data = myFile.read()
    ipList = data.split("|")
    ipList.sort()
    return ipList

# lst2File
# write a list into file
#
# @param list
# @param filePath
def lst2File(lst, filePath):
  with open(filePath, "w") as myFile:
    for item in lst:
      myFile.write(item + "\n")

# main
# glue
def main():
  ipList = getIps(IP_FILE)
  top = {}
  for ip in ipList:
    print ip
    start = int(round(time.time()))
    obj = Download("http://" + ip)
    if not obj.doRequest():
      end = int(round(time.time()))
      top[ip] = end - start
  tmp = [(v, k) for k, v in top.iteritems()]
  topList = []
  for item in sorted(tmp):
    topList.append(item[1])

  lst2File(topList, TOP_FILE)
    

if __name__ == '__main__':
  main()
