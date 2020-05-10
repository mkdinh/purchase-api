from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from config import pg_username, pg_password

from flask import Flask, jsonify

# database setup
# connection_str = 'sqlite:///Resources/purchasing_data.sqlite'
connection_str = f'postgresql://{pg_username}:{pg_password}@localhost:5432/purchase_db'
conn = create_engine(connection_str)

inspector = inspect(conn)

columns = inspector.get_columns('purchases')

print(' Purchases Table columns')
print('------------------------------------')
for col in columns:
    print('  ',col['name'], col['type'])

Base = automap_base()
Base.prepare(conn, reflect=True)

Purchases = Base.classes.purchases

app = Flask(__name__)

@app.route('/api/data')
def data():
    session = Session(bind=conn)

    purchases = session.query(Purchases).all()

    data = []

    for purchase in purchases:
        data.append({
            'PurchaseID': purchase.purchaseid,
            'SN': purchase.sn,
            'Gender': purchase.gender,
            'Age': purchase.age,
            'ItemID': purchase.itemid,
            'ItemName': purchase.itemname,
            'Price': purchase.price
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)