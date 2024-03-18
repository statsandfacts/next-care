from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import hashlib

# Connect to your MySQL database
mydb = mysql.connector.connect(
  host="dev-one-health.c78iwse2o1c2.us-east-2.rds.amazonaws.com",
  user="admin",
  password="12345678",
  database="skincare"
)

# Create a cursor object using the cursor() method
mycursor = mydb.cursor()