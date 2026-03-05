from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

import psycopg2
from neo4j import GraphDatabase


POSTGRES_CONFIG = {
    "host": "192.168.18.178",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

NEO4J_CONFIG = {
    "uri": "bolt://192.168.18.16:7687",
    "user": "neo4j",
    "password": "Ddi12345!"
}


def sync_persons():

    print("Connecting to PostgreSQL...")

    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, age, city_id
        FROM persons
    """)

    rows = cur.fetchall()

    print(f"Fetched {len(rows)} rows")

    driver = GraphDatabase.driver(
        NEO4J_CONFIG["uri"],
        auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"])
    )

    with driver.session(database="airflowtest") as session:

        for row in rows:

            session.run("""
                MERGE (p:Person {id:$id})
                SET
                    p.name=$name,
                    p.email=$email,
                    p.age=$age,
                    p.city_id=$city_id
            """,
            id=row[0],
            name=row[1],
            email=row[2],
            age=row[3],
            city_id=row[4])

    cur.close()
    conn.close()
    driver.close()

    print("Sync complete")


with DAG(

    dag_id="postgres_to_neo4j_persons",

    start_date=datetime(2024,1,1),

    schedule="@once",

    catchup=False,

    tags=["postgres","neo4j"]

) as dag:

    sync_task = PythonOperator(

        task_id="sync_persons",

        python_callable=sync_persons

    )

    sync_task
