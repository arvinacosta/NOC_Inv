import json
import sqlite3
import os
import uvicorn

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# import datetime
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Database file path
DB_FILE = os.getenv("DB_FILE", "db/appdata2.db")  # Default to 'db/entries.db' if not specified

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# Initialize the database and create the table with updated columns if it does not exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_number TEXT,
            location TEXT,
            brand TEXT,
            model TEXT,
            macadd TEXT,
            description TEXT,
            itypes TEXT,
            remarks TEXT,
            status TEXT,
            switch TEXT,
            stampTime TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Run the database initialization
@app.on_event("startup")
def on_startup():
    init_db()

# Mount static files
app.mount("/statics", StaticFiles(directory="statics"), name="statics")


# Initialize templates
templates = Jinja2Templates(directory="templates")


# ===================================================================================================
# Pydantic model for item data
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
    #stampTime: datetime  # Ensure timestamp is included as a datetime field
    stampTime: str  # Ensure timestamp is included as a datetime field

# GO TO ROOT and LOAD Main HTML ==================================================================================
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    #return templates.TemplateResponse("main_item2_nov14.html", {"request": request})
    return templates.TemplateResponse("modal4_test.html", {"request": request})
    #return templates.TemplateResponse("modal4_test_noFunc.html", {"request": request})

#main_item2_nov13
#main_item2.html


# SHOW ITEM ALL ==================================================================================================
@app.get("/items", response_class=JSONResponse)
async def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()

    # = WORKING =============================================
    # json_data = json.dumps(items, indent=4)
    # print(json_data)

    # ==============================================
    # Prepare the headers
    headers = ['ID', 'Serial Number', 'Location', 'Brand', 'Model', 'Description', 'itypes', 'MAC Address', 'Remarks', 'Status', 'Switch', 'stampTime']

    # Extract the values for each row (data)
    rows = [[item['id'], item['serial_number'], item['location'], item['brand'], item['model'], item['description'], item['itypes'], item['macadd'], item['remarks'], item['status'], item['switch'], item['stampTime']] for item in items]

    # Print the table
    print(tabulate(rows, headers=headers, tablefmt='pretty'))
    # ==============================================

    return items



# ===================================================================================================
@app.get("/items/pdf", response_class=JSONResponse)
async def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
   
    # Convert rows to a list of dictionaries
    items = [dict(row) for row in rows]
    
    # Create pretty JSON string
    pretty_json = json.dumps(
        {"items": items, "distinct_word": distinct_word, "kb_patch": kb_patch},
        indent=4
    )

    # Return as an HTML response to view pretty JSON
    return HTMLResponse(content=f"<pre>{pretty_json}</pre>", media_itypes="text/html")


# SHOW ITEM Per ID  ============================================================================
@app.get("/items/{item_id}", response_class=JSONResponse)
async def get_item_by_id(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if item:
        return dict(item)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# ===================================================================================================
# Function to check if the serial number already exists in the database
async def check_duplicate_sernum(sernum: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM items WHERE serial_number = ? LIMIT 1", (sernum,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# API endpoint to check for a duplicate serial number
@app.get("/check-duplicate/{sernum}")
async def check_duplicate(sernum: str):
    if await check_duplicate_sernum(sernum):  # Check if the serial number exists
        raise HTTPException(status_code=400, detail="Serial number already exists.")
    return {"message": "Serial number is available."}

# SAVE Endpoint ======================================================================================
@app.post("/item/save", response_model=Item)
async def save_item(item: Item):
 
    conn = get_db_connection()
    cursor = conn.cursor()



    #item.stampTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item.stampTime = datetime.now()
    item.stampTime = item.stampTime.strftime("%Y-%m-%d %H:%M:%S")

     

    cursor.execute(
        "INSERT INTO items (serial_number, location, brand, model, description, itypes, macadd, remarks, status, switch, stampTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (item.serial_number, item.location, item.brand, item.model, item.description, item.itypes, item.macadd, item.remarks, item.status, item.switch, item.stampTime)
    )
    
    conn.commit()
    conn.close()
    return item



# UPDATE  endpoint ======================================================================================
@app.put("/items/{id}", response_model=Item)
async def update_item(id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    #item.stampTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item.stampTime = datetime.now()
    item.stampTime = item.stampTime.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        UPDATE items
        SET serial_number = ?, location = ?, brand = ?, model = ?, description = ?, itypes = ?, macadd = ?, remarks = ?, status = ?, switch = ?, stampTime = ?
        WHERE id = ?
    ''', (item.serial_number, item.location, item.brand, item.model, item.description, item.itypes,
          item.macadd, item.remarks, item.status, item.switch, item.stampTime, id))
    conn.commit()
    conn.close()

    return item


# ===================================================================================================
@app.post("/item/saveXXX", response_model=Item)
async def save_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()

    #item.stampTime = datetime.now() 
    item.stampTime = item.stampTime.strftime("%Y-%m-%d %H:%M:%S")
    print("Received time:", item.stampTime)

    
    if item.id:
        # If ID is provided, update the existing item
        cursor.execute('''
            UPDATE items
            SET serial_number = ?, location = ?, brand = ?, model = ?, description = ?, itypes = ?, macadd = ?, remarks = ?, status = ?, switch = ?, stampTime = ?
            WHERE id = ?
        ''', (item.serial_number, item.location, item.brand, item.model, item.description, item.itypes, item.macadd, item.remarks, item.status, item.switch, item.stampTime, item.id))
    else:
        # If no ID is provided, insert a new item
        cursor.execute(
            "INSERT INTO items (serial_number, location, brand, model, description, itypes, macadd, remarks, status, switch, stampTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (item.serial_number, item.location, item.brand, item.model, item.description, item.itypes, item.macadd, item.remarks, item.status, item.switch, item.stampTime)
        )
    
    conn.commit()
    conn.close()

    return item  # Return the item data after saving or updating



@app.delete("/items/delete/{id}")
async def delete_item(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (id,))
    item = cursor.fetchone()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        conn.execute("BEGIN")
        cursor.execute("DELETE FROM items WHERE id = ?", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete item")
    finally:
        conn.close()

    return {"message": "Item deleted successfully", "id": id}





# ==============================================================





# ==============================================================
if __name__ == "__main__":
    cert_dir = os.path.join(os.path.dirname(__file__), "certs")
    ssl_keyfile = os.path.join(cert_dir, "server_unencrypted.key")
    ssl_certfile = os.path.join(cert_dir, "server.crt")
    uvicorn.run(app, host="0.0.0.0", port=8856, ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile)