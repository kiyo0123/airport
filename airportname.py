import argparse
import requests

def airportname(code):
    url = 'https://airports-r3bmrgmuna-an.a.run.app'
    response = requests.get(url + "/airportname/%s" % code)
    print(response.status_code)
    return response.text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'code', help='IATA 3 letters airport code e.g. HND'
    )
    
    args = parser.parse_args()
    code = args.code

    name = airportname(code)
    print(name)    




