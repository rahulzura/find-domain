from PyDictionary import PyDictionary
from selenium.webdriver import Chrome

from app.domain import find_domain


def run():
    dictionary = PyDictionary()
    entered_word = input("Enter a word to find an available .com domain with it or a synonym of it: ")
    synomyms = dictionary.synonym(entered_word) # returns a list containing synonyms of the word

    driver = Chrome()

    words = [entered_word]
    words.extend(synomyms)
    for word in words:
        # remove whitespaces from word
        word = ''.join(word.split(' '))
        domain = word + '.com'
        print(f"Checking if {domain} is available")
        price = find_domain(domain, driver)
        if price is not None:
            print(f"{domain} is available and its price is {price} rupees for the first year")
            driver.quit()
            return
        else:
            print(f"{domain} is not available")

    driver.quit()
    print("Neither the word nor the synonyms were availabel as domain names")
    
run()