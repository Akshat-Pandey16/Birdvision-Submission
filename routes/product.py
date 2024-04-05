import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.db import get_db, Product
from models.models import ProductModel

router = APIRouter(tags=["products"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@router.get("/products")
def get_products(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
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
        logger.error(f"Database query failed in get_products: {str(e)}")
        raise HTTPException(status_code=500, detail="Database query failed")


@router.get("/products/{id}")
def get_product_by_id(
    id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
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
        logger.error(f"Database query failed in get_product_by_id: {str(e)}")
        raise HTTPException(status_code=500, detail="Database query failed")


@router.post("/products")
def create_product(
    product_data: ProductModel,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
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
        logger.error(f"Error creating product: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating product")


@router.put("/products/{id}")
def update_product(
    id: int,
    product_data: ProductModel,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Update an existing product.

    Parameters:
    - `id` (int): The ID of the product to be updated.
    - `product_data` (ProductModel): New details of the product.

    Returns:
    - `Product Updated` (int): ID of the updated product.
    """
    try:
        title = product_data.title
        description = product_data.description
        price = product_data.price
        count = product_data.count
        exist = (
            db.query(Product)
            .filter(
                Product.title == title,
                Product.description == description,
                Product.price == price,
                Product.count == count,
            )
            .first()
        )
        if exist:
            raise HTTPException(
                status_code=400,
                detail="Product with the same title, description, price, and count already exists, updation failed",
            )
        product_exists = db.query(Product).filter(Product.id == id).first()
        if product_exists is None:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")

        product_exists.title = title
        product_exists.description = description
        product_exists.price = price
        product_exists.count = count
        db.commit()
        return {"Product Updated": id}
    except SQLAlchemyError as e:
        logger.error(f"Error updating product: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating product")


@router.delete("/products/{id}")
def delete_product(
    id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
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
        logger.error(f"Error deleting product: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting product")


@router.delete("/products")
def delete_all_products(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
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
        logger.error(f"Error deleting all products: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting all products")
