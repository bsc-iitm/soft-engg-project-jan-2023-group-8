from main import app
from flask import render_template,flash
from flask_login import login_required
from application.models import User,Ticket,Message
from flask import render_template,flash
from main import login_manager, app
from application.db import db
from flask import render_template,flash,redirect, url_for,request
from application.forms import TicketForm,EditTicket,DeleteForm
from  flask_login import current_user, login_required
from flask import render_template,request,url_for
from datetime import datetime

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    tickets = db.session.query(Ticket.ticket_id, Ticket.subject, Ticket.category, Ticket.is_resolved).filter_by(user_id=current_user.user_id).all()
    form = EditTicket()
    form1 = DeleteForm()
    if request.method == "POST":
        p_item = request.form.get('edit')
        p_item_o = Ticket.query.filter_by(ticket_id=p_item).first()
        if p_item_o:
            p_item_o.subject = form.new_subject.data
            p_item_o.category = form.new_category.data
            db.session.commit()
        return redirect(url_for('dashboard'))
    if request.method == "GET":
        return render_template("dashboard.html", user=current_user.username, items=tickets, form=form, form1=form1)

@app.route("/addticket", methods=['GET', 'POST'])
def add_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket_to_create = Ticket(user_id=current_user.user_id, subject=form.subject.data, category=form.category.data,created_date = datetime.now())
        db.session.add(ticket_to_create)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_ticket.html', form=form)

@app.route("/delete/<int:ticket_id>", methods=['GET', 'DELETE'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('dashboard'))
