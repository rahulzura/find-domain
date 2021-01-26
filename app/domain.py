from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# https://godaddy.com/domainsearch/find?checkAvail=1&domainToCheck=hari.com
def find_domain(domain, driver):
    """
    Returns the price of domain if it's available else returns None
    """


    url = f"https://godaddy.com/domainsearch/find?checkAvail=1&domainToCheck={domain}"
    driver.get(url)

    try:
        # this element is only rendered if the domain is available at normal price
        # i.e., when it is neither a primium domain with an owner nor unavailable
        exact_match_domain_p = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element_by_css_selector("p[data-cy='celebrate-exact-match-domain']"))
        
    except Exception as err:
        if isinstance(err, TimeoutException):
            pass
        else:
            print(f"ERROR: {err}")
        return None

    domain_spans = exact_match_domain_p.find_elements_by_css_selector("span")
    label = domain_spans[0].text # this span has the 'example' part of 'example.com'
    tld = domain_spans[1].text # this span has the '.com' part of 'example.com'
    
    if domain == label + tld:
        # If the exact_match_domain_p is rendered, then this is too
        exact_match_pricing_div = driver.find_element_by_css_selector("div[data-cy='celebrate-exact-match-pricing'")
        pricing_spans = exact_match_pricing_div.find_elements_by_css_selector('span')
        price = pricing_spans[1].text # second span has the current pricing for the first year
        
        price = float(price[2:])
        return price

    else:
        # If this runs, it means the assumption that if the exact match p is found
        # the domain is available is wrong
        raise Exception("Exact match but not available?")

