import locale
from flask import Flask, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap5
from flask import render_template, request, abort
from models import Card, User
from forms import CardRegisterForm, EditCardForm, LoginForm, StartTestForm
from models import db_session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memory_card.db"
app.config["SECRET_KEY"] = "hansoo77jp"

bootstrap = Bootstrap5(app)

# Set locale (change "fr_FR" to your desired locale, e.g., "de_DE" for German)
locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def set_user_password(username, password):
    new_user = User(username=username, password=generate_password_hash(password))
    db_session.add(new_user)
    db_session.commit()


def update_user_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        user.password = generate_password_hash(password)
    db_session.commit()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("list_cards", lang="all"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = CardRegisterForm()
    if form.validate_on_submit():
        new_card = Card(
            lang=form.lang.data,
            word=form.word.data,
            func=form.func.data,
            meaning=form.meaning.data,
            memo=form.memo.data,
        )
        db_session.add(new_card)
        db_session.commit()
        return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route("/list/<lang>")
@login_required
def list_cards(lang):
    if lang == "all":
        cards = Card.query.all()
    else:
        cards = Card.query.filter_by(lang=lang)
    return render_template("list_card.html", title="List of cards", cards=cards)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
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
        return redirect(url_for("list_cards", lang="all"))
    return render_template("edit_card.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/test/<string:lang>/<int:dif>/<int:index>/<int:side>",
            methods=["GET", "POST"])
@login_required
def test_words(lang, dif, index=0, side=0):
    action = request.form.get('action')
    
    plus_ids = session.get('plus_ids', None)
    if plus_ids is None:
        plus_ids = []
    minus_ids = session.get('minus_ids', None)
    if minus_ids is None:
        minus_ids = []
        
    words = Card.query.filter(Card.lang == lang, Card.difficulty >= dif).all()

    if action == "failure" and index > 0:
        prev_word = words[index-1]
        plus_ids.append(prev_word.id)
    elif action == "success" and index > 0:
        prev_word = words[index-1]
        if prev_word.difficulty != 0:
            minus_ids.append(prev_word.id)

    if index == len(words):
        print(f"minus_ids: {minus_ids}")
        print(f"plus_ids: {plus_ids}")
        for word_id in minus_ids:
            word = Card.query.filter(Card.id == word_id).first()
            print(f"word: {word.word}, difficulty: {word.difficulty}")
            word.difficulty = word.difficulty - 1
            db_session.commit()
        for word_id in plus_ids:
            word = Card.query.filter(Card.id == word_id).first()
            print(f"word: {word.word}, difficulty: {word.difficulty}")
            word.difficulty = word.difficulty + 1
            db_session.commit()
        session.pop("minus_ids", None)
        session.pop("plus_ids", None)
        return render_template("message.html", message="Congratulation! You finished the test.")
    elif not (0 <= index < len(words)):
        abort(404)
    else:
        session["minus_ids"] = minus_ids
        session["plus_ids"] = plus_ids
        word = words[index]
        if side == 0:
            return render_template("show_top.html", word=word.word, lang=lang, dif=dif, index=index)
        else:
            return render_template("show_bottom.html", word=word.word, lang=lang, dif=dif, index=index,
                                meaning=word.meaning, function=word.func,
                                memo=word.memo, next_index=index+1)
    

@app.route("/test", methods=["GET", "POST"])
@login_required
def start_test():
    form = StartTestForm()
    if form.validate_on_submit():
        lang = form.lang.data
        dif = form.dif.data
        return redirect(url_for("test_words", lang=lang, dif=dif, index=0, side=0))
    return render_template("start_test.html", form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5500)