import argparse
import base64
import datetime

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

def create_database(instance_id, database_id):
    print('create_database called')
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id, ddl_statements=[
        """CREATE TABLE Singers (
            SingerId     INT64 NOT NULL,
            FirstName    STRING(1024),
            LastName     STRING(1024),
            SingerInfo   BYTES(MAX)
        ) PRIMARY KEY (SingerId)""",
        """CREATE TABLE Albums (
            SingerId     INT64 NOT NULL,
            AlbumId      INT64 NOT NULL,
            AlbumTitle   STRING(MAX)
        ) PRIMARY KEY (SingerId, AlbumId),
        INTERLEAVE IN PARENT Singers ON DELETE CASCADE"""
    ])

    operation = database.create()

    print('Waiting for operation to complete...')
    operation.result(120)

    print('Created database {} on instance {}'.format(
        database_id, instance_id))


def insert_data(instance_id, database_id):
    print('insert_data called')

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
    
    