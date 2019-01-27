from string import Template

with open('./template.html', 'r', encoding='utf-8') as f:
    basic_template = Template(f.read())

def error_page(environ, start_response, message, code='400 Bad Request'):
    start_response(code, [('Content-Type', 'text/html')])
    yield basic_template.substitute(title='Error', main='Error: ' + message).encode('utf-8')
