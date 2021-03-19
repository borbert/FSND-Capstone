from app import create_app
from models import Item,User,List,db


def main():
    app = create_app()
    db.create_all()

    db.session.add(
        Item(
            
            prod_description = 'test description',
            category = ['test category'],
            image_link = 'test link',
            favorite = True,
            stores = [1,2],
            barcode = '0358423356'
            # lists = [1,2,3]
        )
    )

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    main()