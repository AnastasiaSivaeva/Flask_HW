#Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна 
#(шапка, меню, подвал), и дочерние шаблоны для страниц категорий товаров и отдельных 
#товаров. 
#Например, создать страницы «Одежда», «Обувь» и «Куртка», используя базовый шаблон.

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/clothes/')
def clothes():
    return render_template('clothes.html')

@app.route('/jacket/')
def jacket():
    return render_template('jacket.html')

@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')



if __name__ == '__main__':
    app.run()