import bs4, requests, urllib.request, re, os

#os.chdir(r'c:\Users\Adam\Desktop\pythonprogs\XKCDComics')   #change this to your current directory if needed

#this first chunk finds the comic number based on the html code from the page
url = 'http://xkcd.com/'
res = requests.get(url)     #open initial xkcd webpage
res.raise_for_status()      #raise exception if page doesnt work          

imageSoup = bs4.BeautifulSoup(res.text, 'html.parser')  #parse html from page

num = imageSoup.select('#middleContainer')              #select the number of the comic from html code
num = num[0].text.strip()                               #strip the string of extra html stuff
regex = re.compile(r'com/(.*?)/')                       #create regex object to extract comic number
num = regex.findall(num)                                #find comic number and have it in a list


#the comic number is then used to loop through the pages and extract the image and title and then save it to a folder.
for i in range(int(num[0]),0,-1):

    url = 'http://xkcd.com/' + str(i)
    res = requests.get(url)          #open initial xkcd webpage
    res.raise_for_status()

    imageSoup = bs4.BeautifulSoup(res.text, 'html.parser')      #parse html from page

    try:
        imageElem = imageSoup.find(id="comic")                      #get image element from html
        imageFullURL = imageElem.find('img')['src']             #find URL of image
        imageURL = imageFullURL.lstrip('//')                    #delete the first 2 "//" characters

        titleElem = imageSoup.select('#ctitle')                 #finds comic title element
        title = titleElem[0].text.strip()                       #strips title element to just be title

    except:
        print('Not able to find image source')                  #Sometimes this problem happens when there's no image on the page

    if os.path.isfile(title + '.png') == False:                 #if the image does not exist in folder, download it

        try:
            urllib.request.urlretrieve('http://www.' + imageURL, title + '.png')
            print('Comic ' + str(i) + ' downloaded')

        except:
            print('Failed to download this one, not an image?')     #Sometimes the file isn't an image and urllib fails to download it
            continue
    else:
        print('You already have this image (' + title + ')')                        


print('Finished.' + ' All images were downloaded to: ' + os.getcwd())




