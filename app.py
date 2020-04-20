from v1 import app
from v1.donor.routes import donorapi
from v1.donation.routes import donationapi
from v1.volunteer.routes import volunteerapi
from v1.items.routes import itemapi
from v1.collection.routes import collectionapi
from v1.centre.routes import centreapi

app.register_blueprint(donorapi, url_prefix='/api/v1/donor')
app.register_blueprint(donationapi, url_prefix='/api/v1/donation')
app.register_blueprint(volunteerapi, url_prefix='/api/v1/volunteer')
app.register_blueprint(itemapi, url_prefix='/api/v1/items')
app.register_blueprint(collectionapi, url_prefix='/api/v1/collection')
app.register_blueprint(centreapi, url_prefix='/api/v1/centre')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

