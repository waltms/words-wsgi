from urllib.parse import parse_qs
from html import escape
import sys, os, re
import subprocess

words_bin = "bin/words"
words_path = "/var/www/wsgi/words/"
acceptable_referers = ['anastrophe2.lib.uchicago.edu', 'logeion.org', 'logeion.uchicago.edu']
logeion_url = "https://logeion.uchicago.edu/"
need_referer = False

def referer_check(env):
    # check if HTTP_REFERER is set in the envronment passed to the webserver
    # and if set, then check whether we need a referer, in which case
    # loop through the acceptable_referers and see if any are a substring
    # of the referer, otherwise return False
    if 'HTTP_REFERER' in env and need_referer:
        referer = env['HTTP_REFERER']
        for host in acceptable_referers:
            if host in referer: return True
        return False
    return not need_referer

def word_check(env):
    params = parse_qs(env['QUERY_STRING'])
    word = params.get('word')

    if word:
        word = escape(word[0])
        return word
    return False

def word_sanitize(ws):
    ws = ws.replace('MORE - hit RETURN/ENTER to continue', '')
    ws = ws.replace('Unexpected exception in PAUSE', '')
    return ws

def parse_word(word):
    words = os.path.join(words_path, words_bin)
    command = ' '.join([words, word])
    word = subprocess.run([command], capture_output=True, shell=True, cwd=words_path, encoding='utf8')
    if word.stdout:
        return word.stdout
    return None

def words_to_html(words_result):

    path = os.path.join(words_path, "words.html")
    file = open(path, "r")
    html = file.read()

    ws = words_result
    #ws = words_result.replace("b'", "").strip("'")
    #ws = ws.replace(r'\r', '')

    ws = word_sanitize(ws)

    # split on \n
    ws = ws.split('\n')

    # get list element with lemma
    lines = [l for l in ws if re.match(r'^.*\[[A-Z]+\].*?$', l)]
    for lemmaline in lines: 
        idx = ws.index(lemmaline)

        # add a logeion url to the lemma 
        ws[idx] = re.sub(r'^([A-Za-z]+)', r'<a href='+ logeion_url + r'\1' + r'>\1</a>', ws[idx])

    # join with <br>
    out_html = '<div style="position:relative; margin: 0 auto; display: inline-block; border-radius: 10px; border: 2px solid #800000; padding: 20px;">%s</div>' % '<br>'.join(ws)
    html = html.replace("%WORDS%", out_html)

    return html

def application(env, start_response):

    start_response('200 OK', [('Content-Type','text/html')])

    if referer_check(env):
        word = word_check(env)
        if word:
            words_result = parse_word(word)
            if words_result:
                result = words_to_html(words_result)
                return[bytes(result, 'utf8')]
            else:
                return[b'Unknown word.']
        else:
            return[b'No word supplied.']
    else:
        return[b'Please search Logeion first.']
