import httpx
from selectolax.parser import HTMLParser

def getUrls(BasewebsiteUrl):
    headers = {"User-Agent":"iTunes/12.13 (Windows; Microsoft Windows 10 x64; x64) AppleWebKit/7613.2007"}
    

    websiteUrls = [BasewebsiteUrl]
    i = 1
    while(i <= 6):
        websiteUrls.append(BasewebsiteUrl + f"{i}/")
        i += 1

    urls = []

    for websiteUrl in websiteUrls: # gets urls for apartment building pages
        resp = httpx.get(websiteUrl, headers=headers, timeout=10)
        html = HTMLParser(resp.text)

        apartments = html.css("a.property-link")

        for apartment in apartments:
            url = apartment.attributes.get("href")
            if url is not None and url not in urls:
                urls.append(url)

    finalUrls = {}

    for url in urls: # gets urls for apartment room pages
        resp = httpx.get(url, headers=headers, timeout=10)
        html = HTMLParser(resp.text)
        roomTypesCounted = []
        urlsToAdd = []
        tempUrls = []

        roomInfo = html.css("li.unitContainer.js-unitContainerV3")
        for room in roomInfo:
            roomType = room.attributes.get("data-unit") + room.attributes.get("data-beds") + room.attributes.get("data-baths")
            room.strip_tags(["button.btn.btn-sm.btn-secondary.sendMessage.js-sendMessage.actionLinks"])

            if roomType not in roomTypesCounted:
                tempUrls.append(room.attributes.get("data-unitkey") + "-2-unit")
                roomTypesCounted.append(roomType)
        
        for tempUrl in tempUrls:
            urlsToAdd.append(url + "#" + tempUrl)

        finalUrls[url] = urlsToAdd
    return finalUrls
