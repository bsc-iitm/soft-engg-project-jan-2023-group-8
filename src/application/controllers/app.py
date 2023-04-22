from main import app
from flask_login import login_required
from application.models import User,Ticket,Faq, ResolvedUser, Notification
from main import login_manager, app
from application.db import db
from flask import render_template,redirect, url_for,request
from application.forms import TicketForm,EditTicket,DeleteForm
from  flask_login import current_user, login_required
from datetime import datetime

@app.route('/', methods=['GET'])
@login_required
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = EditTicket()
    form1 = DeleteForm()
    
    if current_user.role == 1:
        tickets = db.session.query(Ticket.ticket_id, Ticket.subject, Ticket.category, Ticket.is_resolved).filter_by(user_id=current_user.user_id).order_by(Ticket.created_date.desc()).all()
    elif current_user.role == 2: 
        tickets = db.session.query(Ticket.ticket_id, Ticket.subject, Ticket.category, Ticket.is_resolved).filter_by(user_id=current_user.user_id).order_by(Ticket.likes.desc(), Ticket.is_resolved).all()
        # My resolved Query
        # tickets = db.session.query(Ticket.ticket_id, Ticket.subject, Ticket.category, Ticket.is_resolved).join(ResolvedUser, ResolvedUser.ticket_id == Ticket.ticket_id).filter_by(user_id=current_user.user_id).order_by(Ticket.created_date.desc()).all()
    else: 
        tickets = db.session.query(Ticket.ticket_id, Ticket.subject, Ticket.category, Ticket.is_resolved).filter((Ticket.user_id==current_user.user_id) & (Ticket.is_resolved==1)).order_by(Ticket.likes.desc()).all()
    
    if request.method == "POST":
        p_item = request.form.get('edit')
        p_item_o = Ticket.query.filter_by(ticket_id=p_item).first()
        if p_item_o:
            p_item_o.subject = form.new_subject.data
            p_item_o.category = form.new_category.data
            db.session.commit()
        return redirect(url_for('dashboard'))

    if request.method == "GET":
        return render_template("dashboard.html", user=current_user, items=tickets, form=form, form1=form1)
    
# --------------------------------- Ticket Controller ---------------------------------

@app.route("/addticket", methods=['GET', 'POST'])
def add_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket_to_create = Ticket(user_id=current_user.user_id, subject=form.subject.data, category=form.category.data,created_date = datetime.now(), is_resolved=False)
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

# ------------------------------------- FAQ Conroller -----------------------

@app.route("/faq", methods=['GET'])
@login_required
def view_faq():
    tickets_faq = Ticket.query.join(Faq, Faq.ticket_id == Ticket.ticket_id).order_by(Ticket.likes.desc()).all()
    return render_template('view_faq.html', tickets=tickets_faq)

@app.route("/faq/detele/<int:ticket_id>", methods=['GET'])
@login_required
def remove_ticket_faq(ticket_id):
    faq = Faq.query.filter_by(ticket_id=ticket_id).one()
    db.session.delete(faq)
    db.session.commit()
    tickets_faq = Ticket.query.join(Faq, Faq.ticket_id == Ticket.ticket_id).order_by(Ticket.likes.desc()).all()
    return render_template('view_faq.html', tickets=tickets_faq)

# ------------------------------------  Notification Controller -------------

# While ticket of the student being resovled by support staff.
def notify_student(ticket_id, user_id):
    notify = Notification(ticket_id, f"Ticket ID: {ticket_id} has been resolved.", user_id, created_date=datetime.now())
    db.session.add(notify)
    db.session.commit()
    
# While student replys to closed ticket.
def notify_staff(ticket_id, user_id): 
    notify = Notification(ticket_id, f"Ticket ID: {ticket_id} has been reopened.", user_id, created_date=datetime.now())
    db.session.add(notify)
    db.session.commit()