from app import app, db
from server.models import Customer, Item, Review


class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
     with app.app_context():
        assert 'comment' in Review.__table__.columns

        # Create a Customer and Item first
        customer = Customer(name="John Doe")
        item = Item(name="Laptop", price=1200.0)

        db.session.add_all([customer, item])
        db.session.commit()  # Ensure they exist in DB before using them

        # Now create a valid Review
        review = Review(comment='great!', customer_id=customer.id, item_id=item.id)
        db.session.add(review)
        db.session.commit()

        assert review.id is not None  # Check that review was saved


    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            c = Customer()
            i = Item()
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id
            # check relationships
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
