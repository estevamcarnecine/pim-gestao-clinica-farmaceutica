from . import db
from datetime import datetime

# Usuários do sistema (gestores, pesquisadores, operadores)
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default="researcher")  # admin, researcher, operator
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"


# Pacientes que participam de estudos clínicos
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relacionamento: um paciente pode estar em vários estudos
    studies = db.relationship("ClinicalStudy", secondary="patient_studies", back_populates="patients")

    def __repr__(self):
        return f"<Patient {self.id} {self.name}>"


# Estudos clínicos
class ClinicalStudy(db.Model):
    __tablename__ = "clinical_studies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default="planning")  # planning, ongoing, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relacionamento: muitos pacientes podem participar de muitos estudos
    patients = db.relationship("Patient", secondary="patient_studies", back_populates="studies")

    def __repr__(self):
        return f"<ClinicalStudy {self.id} {self.title}>"


# Tabela de associação N:N entre pacientes e estudos
patient_studies = db.Table(
    "patient_studies",
    db.Column("patient_id", db.Integer, db.ForeignKey("patients.id"), primary_key=True),
    db.Column("study_id", db.Integer, db.ForeignKey("clinical_studies.id"), primary_key=True)
)


# Produção farmacêutica (exemplo simples)
class Production(db.Model):
    __tablename__ = "production"

    id = db.Column(db.Integer, primary_key=True)
    batch_number = db.Column(db.String(50), nullable=False, unique=True)  # número do lote
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="in_progress")  # in_progress, completed, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Production {self.id} {self.product_name} Lote:{self.batch_number}>"
