from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv

# function to ensure all key data fields have a value
def validate_field(field):# if field is present pass if field:pass
  if not field:
    field = 'No results'
  return field

def scrapeLinkedinProfile():
  profileName = input('Linkedin Profile name: ')

  options = webdriver.ChromeOptions()
  options.add_argument('headless')
  options.add_argument('--no-sandbox')
  options.add_argument("--disable-extensions")
  #for anti head less mode detection
  options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36") # agent change
  options.add_argument("lang=en") 
  chromedriver = '/Users/Enzo/Downloads/chromedriver'
  driver = webdriver.Chrome(chromedriver,options=options)

  # driver.get method() will navigate to a page given by the URL address
  driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

  # locate email form by_class_name
  username = driver.find_element_by_id('username')

  # send_keys() to simulate key strokes
  username.send_keys('')

  # locate password form by_class_name
  password = driver.find_element_by_id('password')

  # send_keys() to simulate key strokes
  password.send_keys('')

  # locate submit button by_xpath
  log_in_button = driver.find_element_by_xpath("//button[@type='submit']")

  # .click() to mimic button click
  log_in_button.click()

  sleep(3)

  # locate search box by_xpath
  searchField = driver.find_element_by_xpath("//input[@placeholder='Search']")
  kword = searchField.send_keys(f'{profileName}')
  searchField.send_keys(Keys.RETURN)

  sleep(5)
  # locate first instance of the search
  firstRow = driver.find_element_by_xpath("//ul[contains(@class,'search-results__list list-style-none')]/li[1]//h3/parent::a")
  firstRow.click()

  sleep(3)
  sel = Selector(text=driver.page_source)
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

  # Linkedin URL
  linkedinUrl = driver.current_url

  # scraping contact information
  contactLink = driver.find_element_by_xpath("//span[text()='Contact info']")
  contactLink.click()

  sleep(3)
  sel = Selector(text=driver.page_source)

  # xpath to extract email
  email = sel.xpath("//section[@class='pv-contact-info__contact-type ci-email']//a/text()").extract_first()
  if email:
    email = email.strip()
  
  website = sel.xpath("//li[@class='pv-contact-info__ci-container link t-14']//a/text()").extract_first()
  if website:
    website = website.strip()

  # validating if the fields exist on the profile
  name = validate_field(name)
  jobTitle = validate_field(jobTitle)
  company = validate_field(company)
  college = validate_field(college)
  email = validate_field(email)
  website = validate_field(website)
  linkedinUrl = validate_field(linkedinUrl)
  
  # # defining new variable passing two parameters
  writer = csv.writer(open(profileName+'.csv','w',encoding='utf-8',newline=''))

  # # writerow() method to the write to the file object
  writer.writerow(['Name','Job Title','Company','College', 'Email', 'Website', 'URL'])

  # # writing the corresponding values to the header
  writer.writerow([name.encode('utf-8'),
                  jobTitle.encode('utf-8'),
                  company.encode('utf-8'),
                  college.encode('utf-8'),
                  email.encode('utf-8'),
                  website.encode('utf-8'),
                  linkedinUrl.encode('utf-8')])

  print(f'Name: {name} Job Title: {jobTitle}\nCompany: {company}\nCollege: {college}\nemail: {email}\nwebsite: {website}\nurl: {linkedinUrl}')

  #print('results saved to csv')
  driver.close()


scrapeLinkedinProfile()