#!/usr/bin/env python3

import argparse
import requests

def get_currency_rate(currency):
   
    url = 'http://api.nbp.pl/api/exchangerates/rates/a/{}/?format=json'.format(currency.upper())
    
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        exit("ConnectionError")
    except requests.exceptions.Timeout:
        exit("Timeout")

    if response.status_code == 200:
        currency_rate = response.json()['rates'][0]['mid']
        return currency_rate
    else:
        exit("An error occured while fetching currency rates!")

def parse_currency_rate(currency):
   
    if currency.upper() == 'PLN': 
        currency_rate = 1
    else:
        currency_rate = get_currency_rate(currency)

    return currency_rate

def return_result(amount, source_currency, target_currency):
    
    source_value = parse_currency_rate(source_currency)
    target_value = parse_currency_rate(target_currency)

    result = round(args.amount * source_value / target_value,2)
    
    return result 

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("amount", help="how much you want to convert", type=float)
    parser.add_argument("source_currency", help="currency you want to convert from")
    parser.add_argument("target_currency", help="currency you want to convert to")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action = "store_true")

    args = parser.parse_args()

    result = return_result(args.amount, args.source_currency, args.target_currency)

    if args.verbose:
        print('Converted from {} to {}:'.format(args.source_currency, args.target_currency), result)
    else:
        print(result)
