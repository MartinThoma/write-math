Run `composer update` to update all third-party software.


## Installation

### Apache

For local testing, set `sudo sublime /etc/apache2/apache2.conf`:

```text
<Directory /var/www/>
    Options Indexes FollowSymLinks ExecCGI
    AddHandler cgi-script .py
    AllowOverride All
    Require all granted
</Directory>
```

(AllowOverride is important for htaccess files)

Then:

```bash
$ sudo service apache2 restart
```


### Composer

This website contains some third party packages. They are administrated via
composer.

Install composer:

```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
```

Now run

```bash
composer update
```

### Misc

* Create `cache-data` folder.

## Status

The lines of code (countet with `cloc`, excluding blank lines and comments)
gives an impression how big the project is:


| Date       | Total | PHP  | HTML | JS  | CSS | Python | Remarks
| ---------- | ----- | ---- | ---- | --- | --- | ------ | -------
| 2015-03-04 | 6633  | 3904 | 2533 | 133 | 42  | 19     | Initial measurement
| 2015-03-06 | 6419  | 3611 | 2612 | 133 | 42  | 19     | Cleanup actions