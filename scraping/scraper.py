from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
from time import sleep


def getHotelURLs(url, driver): 
    #gets urls of all hotels from query page
    driver.get(url)
    sleep(10)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(10)

    lst = driver.find_elements(By.CSS_SELECTOR, "[data-selenium=hotel-item]")
    
    hotelURLs = []
    
    for i in range(len(lst)):
        hotelURLs.append(lst[i].find_element(By.TAG_NAME, "a").get_attribute('href'))
    if len(hotelURLs) < 20:
        return False
    return hotelURLs

def getReviewsURL(url, driver):
    #gets reviews url from hotel page

    driver.get(url)
    sleep(3)
    ele = False
    try:
        ele = driver.find_element(By.CSS_SELECTOR, '[data-selenium=review-basedon]')
    except:
        pass
    
    if ele:
        try:
            return ele.find_element(By.TAG_NAME, "a").get_attribute('href')
        except:
            pass
    
    return False
    
    

def getReviews(url, driver):
    # gets reviews from hotel review page

    driver.get(url)
    sleep(5)
    hotel_name = driver.find_element(By.CSS_SELECTOR, '[data-selenium=hotel-header-name]').text
    hotel_address = driver.find_element(By.CSS_SELECTOR, '[data-selenium=hotel-address-map]').text
    
    overall_rating = False
    try:
        overall_rating = driver.find_element(By.CSS_SELECTOR, "[data-selenium=hotel-header-review-score]").text
        
    except:
        print("Exception:", 1)
    

    if not overall_rating:
        try:
            overall_rating = driver.find_element(By.CLASS_NAME, "Review__ReviewFormattedScore").text
        except:
            print("Exception:", 2)

    if not overall_rating:
        try:
            overall_rating = driver.find_element(By.CLASS_NAME,"Typographystyled__TypographyStyled-sc-j18mtu-0 hTkvyT kite-js-Typography").text
            
        except:
            print("Exception:", 3)
    if not overall_rating:
        try:
            overall_rating = driver.find_element(By.CLASS_NAME,"Typographystyled__TypographyStyled-sc-j18mtu-0 gouaKT kite-js-Typography").text
            
        except:
            print("Exception:", 4)

    if not overall_rating:
        try:
            overall_rating = driver.find_element(By.CSS_SELECTOR, "[data-selenium=hotel-header-review-score]").text
            

        except:
            print("Exception:", 5)
            pass
    

    

    if not overall_rating:
        overall_rating = driver.find_element(By.CLASS_NAME, "ReviewScore-Number ReviewScore-Number--line-height").text
        return False

    more_reviews = False
    for i in range(5):
        try:
            more_reviews = driver.find_element(By.CLASS_NAME, "Review-paginator-button")
        except:
            break
        if more_reviews:
            more_reviews.click()
            sleep(1.5)

    reviewsHelper = driver.find_elements(By.CLASS_NAME, 'Review-comment')
    if len(reviewsHelper) < 100:
        return False

    reviews = []
    

    for i in range(100):
        title = reviewsHelper[i].find_element(By.CLASS_NAME, 'Review-comment-bodyTitle').text
        comment = reviewsHelper[i].find_element(By.CLASS_NAME, 'Review-comment-bodyText').text
        rating = reviewsHelper[i].find_element(By.CLASS_NAME, 'Review-comment-leftScore').text
        reviews.append({
            "review_rating" : rating,
            "review_title" : title,
            "review_comment" : comment 
        })

    hotel = {
            "name" : hotel_name[:-8],
            "address" : hotel_address,
            "overall_rating" : overall_rating,
            "reviews" : reviews
        }


    return hotel

def scraper(queryURL, driver, num):
    lst = []

    hotelsURLS = getHotelURLs(queryURL, driver)
    print("hotel URLS obtained")
    count = 1
    for url1 in hotelsURLS:
        url2 = getReviewsURL(url1, driver)
        if url2:
            hotel = getReviews(url2, driver)
            if hotel:
                print("Hotel", str(count) + ": ", hotel["name"])
                count = count + 1
            
                lst.append(hotel)
            if count > num:
                break

    return lst



driver = webdriver.Chrome()



queryURL = "https://www.agoda.com/en-gb/search?guid=437e2aab-f1b2-4205-9586-e25f25b1dd7c&asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb96xbS%2Fj7byzDtCkgiDh0EedUkG%2FV1NrARrX6tM8tSQyZ7a22%2FNhbJ8OtIkXdj9lU94paTD5VHq5sFdVCiCn7snlJaIi4WmSCtVdmG6XEBvpIFhk8OpaH%2FXi%2Bfv51OpuBXQYl3V1iy9nb%2B0qxM0R6Qmg%3D%3D&city=9395&tick=637864131401&locale=en-gb&ckuid=53e03153-91e5-4d02-93ad-f998e8098013&prid=0&currency=INR&correlationId=23e4cf20-a082-4c70-93a6-7f6348e58271&pageTypeId=1&realLanguageId=16&languageId=1&origin=IN&cid=-1&userId=53e03153-91e5-4d02-93ad-f998e8098013&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=27&currencyCode=INR&htmlLanguage=en-gb&cultureInfoName=en-gb&machineName=sg-acmweb-6005&trafficGroupId=4&sessionId=ebrd5tsp1mtmux5wtn1lby2e&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkIn=2022-05-03&checkOut=2022-05-04&rooms=1&adults=2&children=0&priceCur=INR&los=1&textToSearch=Bangkok&productType=-1&travellerType=1&familyMode=off"


lst = scraper(queryURL, driver, 20)
dic = { "hotels": lst }
json_object = json.dumps(dic, indent = 4)
  
# Writing to sample.json
with open("bangkok1_hotels.json", "w") as outfile:
    outfile.write(json_object)


driver.close()
driver.quit()

