from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import mail_api as mail


app = Flask(__name__)


@app.route('/')
def index():
    token = request.cookies.get('token')
    if token is None: 
        email = mail.Mail()
        if email.check_connection() == 200:
            email.create_account()
            address = email.address
            password = email.password
            token = email.get_token(address, password)
            messages = email.get_messages(token)
            if messages == []:
                resp = make_response(render_template('index_without_messages.html', email_address=email.address))
                resp.set_cookie('token', token)
                return resp
            else:
                resp = make_response(render_template('index_with_messages.html', email_address=email_address, messages=messages))
                resp.set_cookie('token', token)
                return resp
        else:
            return 500
    else:
        email = mail.Mail()
        if email.check_connection() == 200:
            email_address = email.me(token)['address']
            messages = email.get_messages(token)
            if messages == []:
                return render_template('index_without_messages.html', email_address=email_address)
            else:
                return render_template('index_with_messages.html', email_address=email_address, messages=messages)
        else:
            return 500


@app.route('/message/<id>')
def message(id):
    token = request.cookies.get('token')
    email = mail.Mail()
    if email.check_connection() == 200:
        email_address = email.me(token)['address']
        message = email.get_message(token, id)
        html = email.get_message_html(token, id)
        parts = str(render_template('message.html', email_address=email_address, message=message)).split('||html||')
        return parts[0] + html + parts[1]
    else:
        return 500


@app.route('/change_email')
def change_email():
    email = mail.Mail()
    if email.check_connection() == 200:
        email.create_account()
        address = email.address
        password = email.password
        token = email.get_token(address, password)
        messages = email.get_messages(token)
        if messages == []:
            resp = make_response(redirect('/'))
            resp.set_cookie('token', token)
            return resp
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('token', token)
            return resp
    else:
        return 500
    


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
    