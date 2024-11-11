from fastapi import FastAPI, Form
from datetime import datetime
import sqlite3
import os

from pydantic import BaseModel



app = FastAPI()

DB_FILE = os.getenv("DB_FILE", "db/appdata.db")  # Default to 'db/entries.db' if not specified



class Item(BaseModel):
    serial_number: str
    location: str
    brand: str
    model: str
    description: str
    itypes: str
    macadd: str
    remarks: str
    status: str
    switch: str
    timestamp: datetime


# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

@app.post("/item/save")
async def save_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    item.timestamp = datetime.now()  # Set current timestamp here

    print(items)
    cursor.execute(
        "INSERT INTO items (serial_number, location, brand, model, description, itypes, macadd, remarks, status, switch, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (item.serial_number, item.location, item.brand, item.model, item.description, item.itypes, item.macadd, item.remarks, item.status, item.switch, item.timestamp)
    )
    conn.commit()
    conn.close()
    return item



@app.post("/items/savexx")
async def save_item(
    serial_number: str = Form(...),
    location: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    macadd: str = Form(...),
    remarks: str = Form(...),
    status: str = Form(...),
    switch: str = Form(...),
    timestamp: str = Form(...),
):
    # Print the data to the console (for debugging)
    print(f"Item saved: {serial_number}, {location}, {brand}, {timestamp}")
    
    # Save the item to the database or perform any other necessary operations
    return {"message": "Item saved successfully", "timestamp": timestamp}


# uvicorn servertest:app --reload

# curl -X POST http://localhost:8000/items/save -H "Content-Type: application/x-www-form-urlencoded" --data "serial_number=123456&location=Test Location&brand=Test Brand&model=Test Model&description=Test Description&type=Test Type&macadd=00:14:22:01:23:45&remarks=Test Remarks&status=Active&switch=Switch 1&timestamp=2024-11-08T12:34:56"