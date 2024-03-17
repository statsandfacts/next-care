from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import hashlib

# Connect to your MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="skincare"
)

# Create a cursor object using the cursor() method
mycursor = mydb.cursor()