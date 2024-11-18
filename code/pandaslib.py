from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    return float(item.replace('$', '').replace(',', '').replace('(', '-').replace(')', '').replace('￥', ''))

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    return datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S").year

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'usa', 'us', 'united states', 'u.s.', "america"
    ]
    return 'United States' if item.lower() in possibilities else item


if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

