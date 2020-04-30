import argparse
import base64
import datetime
import csv

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

def create_database(instance_id, database_id):
    print('create_database called')
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id, ddl_statements=[
        """CREATE TABLE Airports (
            ident   STRING(1024),
            type    STRING(1024),
            name    STRING(1024),
            elevation_ft    INT64,
            continent   STRING(1024),
            iso_country STRING(1024),
            iso_region  STRING(1024),
            municipality    STRING(1024),
            gps_code    STRING(1024),
            iata_code   STRING(1024),
            local_code  STRING(1024),
            coordinates STRING(1024)
        ) PRIMARY KEY (ident)"""
    ])

    operation = database.create()

    print('Waiting for operation to complete...')
    operation.result(120)

    print('Created database {} on instance {}'.format(
        database_id, instance_id))


def insert_data(instance_id, database_id):
    print('insert_data called')
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    
    collist = ['ident', 'type', 'name', 'elevation_ft', 'continent', 'iso_country', 'iso_region', 'municipality','gps_code','iata_code','local_code','coordinates']
    typelist = ['string','string', 'string', 'integer','string','string','string','string','string','string','string','string']
    alist = []
    path = 'data/airport-codes.csv'
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            for x in range(0, len(collist)):
                if typelist[x] == 'integer':
                    if row[x] != '':
                        row[x] = int(row[x])
                    else:
                        row[x] = None
            alist.append(row)
    #print(alist)

    rowpos = 0
    batchsize = 1000
    while rowpos < len(alist):
        with database.batch() as batch:
            batch.insert(
                table = 'Airports',
                columns=collist,
                values=alist[rowpos:rowpos+batchsize]
            )  
            print('batch insert done from ' + str(rowpos) + ' to ' + str(rowpos+batchsize) ) 
            rowpos = rowpos + batchsize
            
    print('Done')

def delete_data(instance_id, database_id):
    print('delete_data called')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    #args = parser.parse_args()
    parser.add_argument(
        'instance_id', help='Your Cloud Spanner instance ID.'
    )
    parser.add_argument(
        '--database-id', help='Your Cloud Spanner database ID.', default='example_db'
    )
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('create_database')
    subparsers.add_parser('insert_data')
    subparsers.add_parser('delete_data')

    args = parser.parse_args()
    ''' debug 
    print('instance_id:' + args.instance_id)
    print('database-id:' + args.database_id)
    print('command:' + args.command)
    '''

    if args.command == 'create_database':
        create_database(args.instance_id, args.database_id)
    elif args.command == 'insert_data':
        insert_data(args.instance_id, args.database_id)
    elif args.command == 'delete_data':
        delete_data(args.instance_id, args.database_id)
    
    