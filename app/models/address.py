from app.models import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True, nullable=False)

    def as_dict(self):
        return {"id": self.id, "address": self.address}
