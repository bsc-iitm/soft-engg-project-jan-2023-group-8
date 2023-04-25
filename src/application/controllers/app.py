from main import app
from flask import render_template,flash
from flask_login import login_required
from application.models import User, Ticket, Message, Faq, Notification, ResolvedUser
from flask import render_template,flash
from main import login_manager, app
from application.db import db
from flask import render_template,flash,redirect, url_for,request
from application.forms import TicketForm,EditTicket,DeleteForm,EditMessage, MessageForm
from  flask_login import current_user, login_required
from flask import render_template,request,url_for
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    tickets = Ticket.query.all()
    form = MessageForm()
    notifs=get_notifications(current_user.user_id)
    
    if request.method == "POST":
        if form.validate_on_submit():
            p_item = request.form.get('add_message')
            message_to_create = Message(user_id=current_user.user_id, content=form.content.data, ticket_id=p_item,created_date = datetime.now())
            db.session.add(message_to_create)
            db.session.commit()
        return redirect(url_for('home'))      
    if request.method == "GET":
        return render_template("home.html", user=current_user, items=tickets, notifs=notifs)

# --------------------------------- Ticket Controller ---------------------------------

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = EditTicket()
    form1 = DeleteForm()
    notifs=get_notifications(current_user.user_id)

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
        return render_template("dashboard.html", user=current_user.username, items=tickets, form=form, form1=form1, notifs=notifs)

@app.route("/addticket", methods=['GET', 'POST'])
def add_ticket():
    form = TicketForm()

    if form.validate_on_submit():
        ticket_to_create = Ticket(user_id=current_user.user_id, subject=form.subject.data, category=form.category.data,created_date = datetime.now())
        db.session.add(ticket_to_create)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_ticket.html', form=form)

@app.route("/ticket/<int:ticket_id>", methods=['GET','POST'])
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
    message= Message.query.filter_by(ticket_id=ticket_id).all()
    form = EditMessage()

    if request.method == "POST":
        p_user=request.form.get('user_message')
        if(p_user==current_user.user_id):
            p_item = request.form.get('add_message')
            p_item_o = Message.query.filter_by(message_id=p_item).first()
            if p_item_o:
                p_item_o.content = form.new_content.data
                db.session.commit()
        
        else:
            flash("You cannot Edit this message")
            return redirect(url_for('view_ticket',ticket_id=ticket_id))
    
    if request.method == "GET":
        return render_template('ticket.html',item=ticket,message=message,user=current_user,form=form)


@app.route("/delete/<int:ticket_id>", methods=['GET', 'DELETE'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('dashboard'))

# ------------------------------------- Staff Ticket endpoint -----------------------

@app.route("/markticket/<int:ticket_id>", methods=['GET', 'POST'])
def mark_ticket(ticket_id):
    form = MessageForm()

    if form.validate_on_submit():
        message_to_create = Message(user_id=current_user.user_id, ticket_id=ticket_id, content=form.content.data, created_date = datetime.now())
        ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
        resolved_user = ResolvedUser(user_id = current_user.user_id, ticket_id = ticket_id)
        ticket.is_resolved="Y"
       
        db.session.add(message_to_create)
        db.session.add(ticket)
        db.session.add(resolved_user)
        db.session.commit()
        notify_student(ticket.ticket_id, ticket.user_id)
       
        return redirect(url_for('view_ticket',ticket_id=ticket_id))

    return render_template('add_message.html', form=form)

# ------------------------------------- Message Conroller -----------------------

@app.route("/addmessage/<int:ticket_id>", methods=['GET', 'POST'])
@login_required
def add_message(ticket_id):
    form = MessageForm()

    if form.validate_on_submit():
        ticket = Ticket.query.filter_by(ticket_id = ticket_id).one()
        if ticket.is_resolved == "Y": 
            resolved_user = ResolvedUser.query.filter_by(ticket_id=ticket_id).one()
            notify_staff(ticket_id, resolved_user.user_id)
            ticket.is_resolved = "N" 
        message_to_create = Message(user_id=current_user.user_id, ticket_id=ticket_id, content=form.content.data, created_date = datetime.now())
        db.session.add(message_to_create)
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('view_ticket',ticket_id=ticket_id))
    return render_template('add_message.html', form=form)

@app.route("/deletemsg/<int:message_id>", methods=['GET', 'DELETE'])
@login_required
def delete_message(message_id):
    message = Message.query.filter_by(message_id=message_id).one()
    ticket_id=message.ticket_id
    if(message.user_id==current_user.user_id):
        db.session.delete(message)
        db.session.commit()
    else:
        flash("You cannot delete this message")       
    return redirect(url_for('view_ticket',ticket_id=ticket_id))

# ------------------------------------- Likes Conroller -----------------------

@app.route("/addlike/<int:ticket_id>", methods=['GET', 'POST'])
def add_like(ticket_id):
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).one()
    ticket.likes+=1
    db.session.commit()
    return redirect(url_for('home'))
    

# ------------------------------------- FAQ Conroller -----------------------

@app.route("/faq", methods=['GET'])
@login_required
def view_faq():
    tickets_faq = Ticket.query.join(Faq, Faq.ticket_id == Ticket.ticket_id).order_by(Ticket.likes.desc()).all()
    return render_template('view_faq.html', items=tickets_faq,user=current_user.username)

@app.route("/addfaq/<int:ticket_id>", methods=['GET'])
@login_required
def add_faq(ticket_id):
    tickets_faq = Ticket.query.join(Faq, Faq.ticket_id == Ticket.ticket_id).order_by(Ticket.likes.desc()).all()
    if(Faq.query.filter_by(ticket_id=ticket_id).one() == None):
        ticket_to_add = Faq(user_id=current_user.user_id, ticket_id=ticket_id)
        db.session.add(ticket_to_add)
        db.session.commit()       
        
    else:
        flash("Ticket already in FAQ")
    return render_template('view_faq.html', items=tickets_faq,user=current_user.username)
    
@app.route("/faq/delete/<int:ticket_id>", methods=['GET'])
@login_required
def remove_ticket_faq(ticket_id):
    
    faq = Faq.query.filter_by(ticket_id=ticket_id).one()
    db.session.delete(faq)
    db.session.commit()
    tickets_faq = Ticket.query.join(Faq, Faq.ticket_id == Ticket.ticket_id).order_by(Ticket.likes.desc()).all()
    return render_template('view_faq.html', items=tickets_faq,user=current_user.username)

# ------------------------------------  Notification Controller -------------

# While ticket of the student being resovled by support staff.
def notify_student(ticket_id, user_id):
    notify = Notification(ticket_id=ticket_id, message=f"Ticket ID: {ticket_id} has been resolved.",user_id= user_id, created_date=datetime.now())
    db.session.add(notify)
    db.session.commit()
    
# While student replys to closed ticket.
def notify_staff(ticket_id, user_id): 
    notify = Notification(ticket_id=ticket_id, message=f"Ticket ID: {ticket_id} has been reopened.",user_id= user_id, created_date=datetime.now())
    db.session.add(notify)
    db.session.commit()
    
# Called in dashboard to display all notifications of a user
def get_notifications(user_id): 
    notifications = Notification.query.filter_by(user_id = user_id).order_by(Notification.created_date.desc()).all()
    return notifications
