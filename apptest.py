from google.cloud import spanner

def main():
    print('app started')
    instance_id = 'tokyo-spanner'
    database_id = 'testdb'

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT * from Airports WHERE iata_code = 'HND'"
        )

        for row in results:
            print(row)

if __name__ == '__main__':
    main()