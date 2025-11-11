import httpx, time
from selectolax.parser import HTMLParser
from getUrls import getUrls
from getAmenities import getAmenities, getDetails, getRent, getRoomType, getContent

def getInfo():
    urlDict = {}
    infoDict = {}
    headers = {"User-Agent":"iTunes/12.13 (Windows; Microsoft Windows 10 x64; x64) AppleWebKit/7613.2007"}
    MNZipCodes = ["https://www.apartments.com/apartments/minneapolis-mn-55414/","https://www.apartments.com/apartments/minneapolis-mn-55455/","https://www.apartments.com/apartments/minneapolis-mn-55454/"]

    for ZipCode in MNZipCodes: # build a list of all of the urls to parse through, right now they correspond to the apartments in these zip codes: 55414, 55454, 55455
        urlDict.update(getUrls(ZipCode))
    
    for apartUrl, urls in urlDict.items():
        resp = httpx.get(apartUrl, headers=headers)
        html = HTMLParser(resp.text)
        apartmentInfo = []

        try: # This gets the name of the property
            apartmentName = html.css_first("h1#propertyName.propertyName").text().replace("\n","").replace("  ","")
        except AttributeError:
            apartmentName = "Name not found"
        try: # This gets the address of the property
            aptAddress = (html.css_first("div.propertyAddressContainer").text().strip().replace(","," ").replace("\n", "").replace("  ","").replace("Property Website","").replace("MN","MN ")) # + html.css_first("span.stateZipContainer").text().replace("\n","").replace(" ","").strip())
        except AttributeError:
            aptAddress = "Address not found"

        for url in urls: # gets the info for every room in the property
            start = time.perf_counter()
            html = getContent(url)
            if getAmenities(html) is not None:
                apartmentInfo.append(apartmentName)
                apartmentInfo.append(aptAddress)
                apartmentInfo.append(getRoomType(html))
                apartmentInfo.append(getRent(html))
                apartmentInfo.extend(getDetails(html))
                apartmentInfo.append(url)
                apartmentInfo.extend(getAmenities(html))
                apartmentInfo.append("\n")
                print(f"elapsed time: {(time.perf_counter() - start):.4f} seconds")
            
        infoDict[apartmentName] = apartmentInfo # returns a dictionary where the keys are the name of the property and the values is the info of the property

    return infoDict


def makeFile():
    startTime = time.perf_counter()
    infoDict = getInfo()

    with open("apartmentInfo.csv", "w") as fp:
        fp.write(",")
        for aptinfo in infoDict.values(): # build a csv file with each room in each property having its own line
            for item in aptinfo:
                fp.write(f"{item},")

    endTime = time.perf_counter()
    print(f"Program executed in {(endTime - startTime):.4f} seconds")

makeFile()