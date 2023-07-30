from app import db


class GeoData(db.Model):
    __tablename__ = "geodata"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<GeoData {self.id}>"
