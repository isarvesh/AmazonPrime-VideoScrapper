from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# CSS Variables
titleClass = "h1"
titleName = "_2IIDsE _3I-nQy"
ratingClass = "span"
ratingName = "Gpyvwj _1pG1w4 _1g4OLh _1tadIP _3YQFvK"
synopsisClass = "div"
synopsisName = "_1W5VSv"


storeFrontURL = "https://www.amazon.com/gp/video/storefront"
vidDownloadURL = "/gp/video/detail/"

videoLinks = []
titles = []
ratings = []
synopsis = []


def scrapeText(lst, classType, className):
    findClass = soup.find_all(classType, class_=className)
    if len(findClass) == 0:
        lst.append(None)
    else:
        for n in findClass:
            if className == ratingName:
                lst.append(float(n.text[-3:]))
            else:
                lst.append(n.text)

# Initialize Browser to be Control by Python


driver = webdriver.Chrome(
    executable_path="C:/Users/sarve/Downloads/chromedriver_win32/chromedriver.exe")
driver.get(storeFrontURL)

elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    if vidDownloadURL in elem.get_attribute("href"):
        videoLinks.append(elem.get_attribute("href"))

videoLinks = list(dict.fromkeys(videoLinks))

for i in range(0, len(videoLinks)):
    driver.get(videoLinks[i])
    content = driver.page_source
    soup = BeautifulSoup(content)

    scrapeText(titles, titleClass, titleName)
    scrapeText(ratings, ratingClass, ratingName)
    scrapeText(synopsis, synopsisClass, synopsisName)

data = {'Titles': titles, 'Rating': ratings, 'Synopsis': synopsis}
df = pd.DataFrame(data)
df.to_csv('PrimeVid.csv', index=False, encoding='utf-8')


def wordcloud(dataframe, filename):

    if len(df) > 1:
        text = ' '.join(dataframe.Synopsis)
        wordcloud = WordCloud().generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        plt.savefig(filename + ".png")


dfBelow6 = df.loc[(df['Rating'] < 6)]
dfBelow6 = df.loc[(df['Rating'] >= 6) & (df['Rating'] < 8)]
dfBelow6 = df.loc[(df['Rating'] >= 8)]

wordcloud(dfBelow6, "below6")
wordcloud(df6to7, "6to7")
wordcloud(dfAbove8, "above8")
