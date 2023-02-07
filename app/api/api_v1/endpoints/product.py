from sqlalchemy import and_, desc
from fastapi import APIRouter, Depends, Path, HTTPException

from app.db.database import Database
from app.models.model import Product, User
from app.models.response import BaseRespondModel
from app.models.request import ProductRequest, ProductUpdatedRequest


router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {"description": "Not found"}}
)


database = Database()
engine = database.get_db_connection()


def get_session():
    session = database.get_db_session(engine)
    return session


@router.get("/{product_id}", response_model=BaseRespondModel)
async def read_product(product_id: str=Path(title="The id of the product to get"), session: str = Depends(get_session)):
    response_message = "Product retrieved successfully"
    data = None
    try:
        data = session.query(Product).filter(
            and_(Product.id == product_id, Product.deleted == False)).one()
    except Exception as ex:
        print("Error", ex)
        raise HTTPException(status_code=404, detail="Item not found")
    error = False
    return BaseRespondModel(**{"data": data, "code": 200, "message": response_message, "error": error})


@router.post("/add", response_model=BaseRespondModel)
async def add_product(product: ProductRequest, session: str = Depends(get_session)):
    new_product = Product()
    new_product.name = product.name
    new_product.price = product.price
    new_product.seller_email = product.seller_email
    new_product.is_available = product.is_available
    new_product.created_by = product.created_by
    session.add(new_product)
    session.flush()
    session.refresh(new_product, attribute_names=['id'])
    data = {"product_id": new_product.id}
    session.commit()
    session.close()
    return BaseRespondModel(**{"data": data, "code": 200, "message": "Product add successfully", "error": False})


@router.put("/update", response_model=BaseRespondModel)
async def update_product(product: ProductUpdatedRequest, session: str = Depends(get_session)):
    product_id = product.product_id
    try:
        is_product_updated = session.query(Product).filter(Product.id == product_id).update({
            Product.name: product.name, Product.price: product.price,
            Product.seller_email: product.seller_email,
            Product.is_available: product.is_available,
            Product.updated_by: product.updated_by
        }, synchronize_session=False)
        session.flush()
        session.commit()
        response_message = "Product updated successfully"
        response_code = 200
        error = False
        if is_product_updated == 1:
            data = session.query(Product).filter(
                Product.id == product.product_id).one()
        else:
            response_message = "Product not updated. No product found with this id :" + \
                str(product_id)
            error = True
            data = None
        return BaseRespondModel(**{"data": data, "code": response_code, "message": response_message, "error": error})

    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=401, detail="Product not updated")


@router.delete("/delete", response_model=BaseRespondModel)
async def delete_product(product_id: str, session: str=Depends(get_session)):
    try:
        is_product_updated = session.query(Product).filter(and_(Product.id == product_id, Product.deleted == False)).update({
            Product.deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Product deleted successfully"
        response_code = 200
        error = False
        data = {"product_id": product_id}
        if is_product_updated == 0:
            response_msg = "Product not deleted. No product found with this id :" + \
                str(product_id)
            error = True
            data = None
        return BaseRespondModel(**{"data": data, "code": response_code, "message": response_msg, "error": error})
    except Exception as ex:
        print("Error : ", ex)
        raise HTTPException(status_code=)
        

@router.get("/", response_model=BaseRespondModel)
async def read_all_products(created_by: str, page_size: int, page: int, session: str=Depends(get_session)):
    data = session.query(Product).filter(and_(Product.created_by == created_by, Product.deleted == False)).order_by(
        desc(Product.created_at)).limit(page_size).offset((page-1)*page_size).all()
    return BaseRespondModel(**{"data": data, "code": 200, "message": "Products retrieved successfully.", "error": False})
