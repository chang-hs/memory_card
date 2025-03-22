import locale
from flask import Flask, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask import render_template
from models import Card, User
from forms import CardRegisterForm, EditCardForm, LoginForm
from models import db_session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory_card.db'
app.config['SECRET_KEY'] = 'hansoo77jp'

bootstrap = Bootstrap5(app)

# Set locale (change "fr_FR" to your desired locale, e.g., "de_DE" for German)
locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def set_user_password(username, password):
    new_user = User(username=username, password=generate_password_hash(password))
    db_session.add(new_user)
    db_session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('list_cards', lang='all'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = CardRegisterForm()
    if form.validate_on_submit():
        new_card = Card(lang=form.lang.data, word=form.word.data, func=form.func.data, meaning=form.meaning.data,
                    memo=form.memo.data)
        db_session.add(new_card)
        db_session.commit()
        return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/list/<lang>')
@login_required
def list_cards(lang):
    if lang == 'all':
        cards = Card.query.all()
    else:
        cards = Card.query.filter_by(lang=lang)
    return render_template('list_card.html', title="List of cards", cards=cards)




@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_card(id):
    card = db_session.query(Card).filter_by(id=id).first()
    form = EditCardForm(obj=card)
    if form.validate_on_submit():
        card.lang = form.lang.data
        card.word = form.word.data
        card.func = form.func.data
        card.meaning = form.meaning.data
        card.memo = form.memo.data
        card.learnt = form.learnt.data
        card.difficulty = form.difficulty.data
        
        db_session.commit()
        return redirect(url_for('list_cards'))
    return render_template('edit_card.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5500)
