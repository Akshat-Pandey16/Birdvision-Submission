from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db import create_database, Product, get_db
from models import ProductModel
import json


app = FastAPI(
    name="Birdvision Submission",
    description="Product APIs to manage products",
    version="1.0.0",
)

create_database()


@app.get("/")
def index():
    return {"message": "Go to /docs to view the APIs documentation."}


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).offset(0).limit(5).all()
    return {"products": json(products)}


@app.get("/products/{id}")
def get_products_by_id(db: Session = Depends(get_db)):
    return {"Api to get product for an id"}


@app.post("/products")
def create_product():
    return {"Api to create a product"}


@app.put("/products/{id}")
def update_product():
    return {"Api to update product of an id"}


@app.delete("/products/{id}")
def delete_product():
    return {"Api to delete product of an id"}


@app.delete("/products")
def delete_all_products(db: Session = Depends(get_db)):
    try:
        db.query(Product).delete()
        db.commit()
        return {"message": "Database flushed successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error flushing database: {str(e)}"
        )
