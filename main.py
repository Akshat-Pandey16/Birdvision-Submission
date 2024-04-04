from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

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
    """Root endpoint"""
    return {"message": "Go to /docs to view the APIs documentation."}


@app.get("/products")
def get_products(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of products.

    Parameters:
    - `offset` (int, optional): Number of items to skip from the beginning.
    - `limit` (int, optional): Maximum number of items to retrieve.

    Returns:
    - `products` (list): List of products retrieved.
    """
    try:
        products = db.query(Product).offset(offset).limit(limit).all()
        return {"products": products}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID.

    Parameters:
    - `id` (int): The ID of the product to retrieve.

    Returns:
    - `Product` (dict): Details of the product retrieved.
    """
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if product:
            return {"Product": product}
        else:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


@app.post("/products")
def create_product(product_data: ProductModel, db: Session = Depends(get_db)):
    """
    Create a new product.

    Parameters:
    - `product_data` (ProductModel): Details of the product to be created.
        - `title` (str): Title of the product.
        - `description` (str): Description of the product.
        - `price` (float): Price of the product.
        - `count` (int): Count of the product.

    Returns:
    - `Product Added` (int): ID of the newly created product.
    """
    try:
        product_exists = (
            db.query(Product)
            .filter(
                Product.title == product_data.title,
                Product.description == product_data.description,
                Product.price == product_data.price,
                Product.count == product_data.count,
            )
            .first()
        )
        if product_exists:
            raise HTTPException(
                status_code=400,
                detail="Product with the same title, description, price, and count already exists",
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
        return {"Product Added": product.id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")


@app.put("/products/{id}")
def update_product(id: int, product_data: ProductModel, db: Session = Depends(get_db)):
    """
    Update an existing product.

    Parameters:
    - `id` (int): The ID of the product to be updated.
    - `product_data` (ProductModel): New details of the product.

    Returns:
    - `Product Updated` (int): ID of the updated product.
    """
    try:
        product_exists = db.query(Product).filter(Product.id == id).first()
        if product_exists is None:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")

        product_exists.title = product_data.title
        product_exists.description = product_data.description
        product_exists.price = product_data.price
        product_exists.count = product_data.count
        db.commit()
        return {"Product Updated": id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.

    Parameters:
    - `id` (int): The ID of the product to be deleted.

    Returns:
    - `Product Deleted` (int): ID of the deleted product.
    """
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")
        db.delete(product)
        db.commit()
        return {"Product Deleted": id}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")


@app.delete("/products")
def delete_all_products(db: Session = Depends(get_db)):
    """
    Delete all products.

    Returns:
    - `message` (str): Confirmation message of successful deletion.
    """
    try:
        db.query(Product).delete()
        db.commit()
        return {"message": "All products deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error deleting all products: {str(e)}"
        )
