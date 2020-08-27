from flask import Flask,redirect,jsonify,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///records.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
ma=Marshmallow(app)
class records(db.Model):
    email=db.Column(db.String(15),primary_key=True,nullable=False)
    name=db.Column(db.String(25),nullable=False)
    company_name=db.Column(db.String(15))
    mobile_no=db.Column(db.Integer,primary_key=True,nullable=False)
    def __init__(self,email,name,company_name,mobile_no):
        self.email=email
        self.company_name=company_name
        self.name=name
        self.mobile_no=mobile_no

class schma(ma.Schema):
    class Meta:
        fields = ("email","name","company_name","mobile_no")

srow=schma()
mrow=schma(many=True)
@app.route('/create',methods=['POST'])
def create():
    email=request.json['email']
    rw=records.query.filter_by(email=email).first()
    if (rw== None):
        name=request.json['name']
        company_name=request.json['company_name']
        mobile_no=request.json['mobile_no']
        newrec=records(email,name,company_name,mobile_no)
    
        db.session.add(newrec)
        db.session.commit()
    
        if(request.method=='POST'):
            return jsonify({"data":"added"})
        else:
            return jsonify({"data":"not added"})
    else:
        return jsonify({"data" : "redundant"})
@app.route('/list',methods=['GET'])
def view():
    table=records.query.with_entities(records.name,records.company_name,records.mobile_no).all()
    if(len(table) != 0):
        op=mrow.dump(table)
    else:
        return jsonify("empty database")
    return jsonify(op)

@app.route('/update',methods=['POST'])
def modify():
    email=request.json["email"]
    rslt=records.query.filter_by(email=email).first()
    if(rslt != None):
        rslt.name=request.json['name']
        rslt.company_name=request.json['company_name']
        rslt.mobile_no=request.json['mobile_no']
        db.session.commit()
        if(request.method=="POST"):
            return jsonify({"data": "modified"})
        else:
            return jsonify({"data": "not modified"})
    else:
        return jsonify({"User": "not found"})
@app.route('/delete',methods=['POST'])
def remove():
    email=request.json["email"]
    rslt=records.query.filter_by(email=email).first()
    if(rslt != None):
        db.session.delete(rslt)
        db.session.commit()
        return jsonify({email: "deleted"})
    else:
        return jsonify({"User": "not found"})
@app.route('/deleteall',methods=['POST'])
def removeall():
    rslt=records.query.all()
    if(rslt != None):
        for r in rslt:
            db.session.delete(r)
        db.session.commit()
        return jsonify({"database": "deleted"})
    else:
        return jsonify({"database": "already empty"})
if(__name__=='__main__'):
    app.run(debug=True)