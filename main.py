import psycopg2
import faker

connection = psycopg2.connect(
    host="172.28.0.2", database="root", user="root", password="root"
)

cursor = connection.cursor()


def ensure_person_table_exists():
    create_person_table_query = """
      CREATE TABLE IF NOT EXISTS person(
        ID      SERIAL PRIMARY KEY,
        NAME    TEXT NOT NULL,
        ADDRESS TEXT NOT NULL
      );
    """

    cursor.execute(create_person_table_query)
    connection.commit()


def insert_person(name: str, address: str):
    insert_query = f"INSERT INTO person (NAME, ADDRESS) VALUES ('{name}','{address}')"

    cursor.execute(insert_query)
    connection.commit()


ensure_person_table_exists()

fake = faker.Faker()

for person in range(0, 100):
    name, address = fake.name(), fake.address()
    insert_person(name, address)