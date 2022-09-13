import psycopg2

import app.ScheuleStatus as ScheduleStatus
from datetime import timedelta, datetime
from app.config import config

NEW_JOB_SQL = """INSERT INTO schedules(job_id, task_id, status, trigger_time, retry_count)
             VALUES(%s, %s, %s, %s, %s);"""

INSERT_KEY_VALUES_SQL = """INSERT INTO 
    runner_data (job_id, key, value, created_by, created_at)
    VALUES (%s, %s, %s, %s, %s);"""

params = config()


def create_new_job(job_id, task_id):
    current_time = datetime.now()
    trigger_time = current_time + timedelta(seconds=10)
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute(NEW_JOB_SQL, (job_id, task_id, ScheduleStatus.PENDING, trigger_time.timestamp(), 0))
    cur.close()
    conn.commit()
    conn.close()


def insert_values(values):
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.executemany(INSERT_KEY_VALUES_SQL, values)
    cur.close()
    conn.commit()
    conn.close()
