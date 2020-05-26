from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv

# function to ensure all key data fields have a value
def validate_field(field):
  if not field:
    field = 'No results'
  return field

def scrapeMultiProfiles():

  googleDork = input('Enter Google dork string: ') # User input

  writer = csv.writer(open('results.csv','w',encoding='utf-8',newline=''))
  # writerow() method to the write to the file object
  writer.writerow(['Name','Job Title','Company','College', 'Email', 'URL'])

  # specifies the path to the chromedriver.exe
  driver = webdriver.Chrome('/Users/Enzo/chromedriver')

  driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

  # locate email form by_id
  username = driver.find_element_by_id('username')
  # send_keys() to simulate key strokes
  username.send_keys('mewtcor@gmail.com')
  password = driver.find_element_by_id('password')
  password.send_keys('Bdaynaminay416')

  # locate submit button by_xpath
  log_in_button = driver.find_element_by_xpath("//button[@type='submit']")
  # .click() to mimic button click
  log_in_button.click()

  # pause
  sleep(0.5)
  driver.get('https:www.google.com') # navigate to google.conm
  sleep(3)
  search_query = driver.find_element_by_name('q')

  # google dork search
  search_query.send_keys(googleDork)
  sleep(0.5)

  search_query.send_keys(Keys.RETURN)
  sleep(3)

  googleURLs = driver.find_elements_by_xpath("//div[@class='r']/a")
  googleURLs = [url.get_attribute('href') for url in googleURLs]
  sleep(0.5)


  # For loop to iterate over each URL in the list
  for googleURL in googleURLs:
    # get the profile URL 
    driver.get(googleURL)

    # add a 5 second pause loading each URL
    sleep(5)

    # assigning the source code for the webpage to variable sel
    sel = Selector(text=driver.page_source)

    sleep(3)
    #xpath to extract the first h1 text 
    name = sel.xpath("//li[@class='inline t-24 t-black t-normal break-words']/text()").extract_first()
    if name:
      name = name.strip()
    # xpath to extract job title
    jobTitle = sel.xpath("//h2[@class='mt1 t-18 t-black t-normal break-words']/text()").extract_first()
    if jobTitle:
      jobTitle = jobTitle.strip()
    #xpath to extract company
    company = sel.xpath("//ul[@class='pv-top-card--experience-list']/li[1]/a/span/text()").extract_first()
    if company:
        company = company.strip()
    # xpath to extract the text from the class containing the college
    college = sel.xpath("//ul[@class='pv-top-card--experience-list']/li[2]/a/span/text()").extract_first()
    if college:
        college = college.strip()

    linkedinUrl = driver.current_url # Linkedin URL

    # scraping contact information
    contactLink = driver.find_element_by_xpath("//span[text()='Contact info']")
    contactLink.click()

    sleep(3)
    sel = Selector(text=driver.page_source)

    # xpath to extract email
    email = sel.xpath("//section[@class='pv-contact-info__contact-type ci-email']//a/text()").extract_first()
    if email:
      email = email.strip()

    # validating if the fields exist on the profile
    name = validate_field(name)
    jobTitle = validate_field(jobTitle)
    company = validate_field(company)
    college = validate_field(college)
    email = validate_field(email)
    linkedinUrl = validate_field(linkedinUrl)

    # # writing the corresponding values to the header
    writer.writerow([name.encode('utf-8'),
                    jobTitle.encode('utf-8'),
                    company.encode('utf-8'),
                    college.encode('utf-8'),
                    email.encode('utf-8'),
                    linkedinUrl.encode('utf-8')])

    # print result to console
    print(f'Name: {name}\n Job Title: {jobTitle}\n Company: {company}\n College: {college}\n email: {email}\n url: {linkedinUrl}')

    print('results saved to csv')
  driver.close() # close chrome driver


scrapeMultiProfiles()