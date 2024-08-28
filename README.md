# Whitaker's Words with WSGI

This is a short and simple WSGI web interface for Whitaker's Words as currently maintained by [mk270](https://mk270.github.io/whitakers-words/index.html). In order to use this, you will need a running copy of Whitaker's Words, which can be compiled from source found [here](https://github.com/mk270/whitakers-words). 

## Installation

 - Your webserver must have WSGI enabled. In the appropriate web directory (e.g. `/var/www/wsgi/words-wsgi/`) copy your entire Whitaker's Words install contents.
 - Copy `words.py` and `words.html` from this repository into the same directory.
 - Add the following directives into your webserver config file:

```apacheconf
    <Directory "/var/www/wsgi/words-wsgi">
        Require all granted
    </Directory>

    WSGIScriptAlias /whitakers-words /var/www/wsgi/words-wsgi/words.py
```

 - Restart your webserver.

## Usage

The web interface should now be usable as: `https://my-web-site/whitakers-words?word=bellum`

The results resemble standard Whitaker's Words output, with minimal styling.

[!NOTE]
Lemmas have a link to the corresponding entries in [Logeion](https://logeion.uchicago.edu/).

[!TIP]
In `words.py` there are two variables worthy of being mentioned. One is `acceptable_referers`, a list of acceptable referers, in case you would like the interface to only be accessible from a pre-designated website link. This functionality will only be enforced if the variable `need_referer` is set to `True`.
