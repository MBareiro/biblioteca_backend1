from app import db, ma, app

class ProveedorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'telefono', 'direccion')

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

with app.app_context():
    db.create_all()
