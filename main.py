from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import Product, create_database, get_db
from models import ProductModel

app = FastAPI(
    title="Birdvision Submission",
    description="Product APIs to manage products",
    version="1.0.0",
)

create_database()


@app.get("/")
def index():
    return {"message": "Go to /docs to view the APIs documentation."}


@app.get("/products")
def get_products(ost: int = 0, lmt: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(ost).limit(lmt).all()
    return {"products": products}


@app.get("/products/{id}")
def get_products_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if product:
        return {"Product": product}
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@app.post("/products")
def create_product(product_data: ProductModel, db: Session = Depends(get_db)):
    product_exists = (
        db.query(Product)
        .filter(
            Product.title == product_data.title,
            Product.description == product_data.description,
            Product.price == product_data.price,
            Product.color == product_data.color,
        )
        .first()
    )
    if product_exists:
        raise HTTPException(
            status_code=400,
            detail="Product with the same title, description, price, and color already exists",
        )
    product = Product(
        title=product_data.title,
        description=product_data.description,
        price=product_data.price,
        count=product_data.count,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"Product Added"}


@app.put("/products/{id}")
def update_product(id: int, product: ProductModel, db: Session = Depends(get_db)):
    product_exists = db.query(Product).filter(Product.id == id).first()

    if product_exists is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    product_exists.title = product.title
    product_exists.description = product.description
    product_exists.price = product.price
    product_exists.count = product.count
    db.commit()
    return {f"Product {id} Updated"}


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    try:
        db.query(Product).filter(Product.id == id).delete()
        db.commit()
        return {f"Product {id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")


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
