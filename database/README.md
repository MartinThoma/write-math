I will create irregular database dumps. If you think I should update the
dump, just send me an email (info@martin-thoma.de).

![A visual overview over the database](https://raw.githubusercontent.com/MartinThoma/write-math/master/database/big-picture-database.png)

The main part of the database, the `wm_raw_data`, can be backed up within 40s
(2014-07-21) from the server. That can be done with `backup_wm_raw_draw_data.py`.

Adding all data from the sql textfiles to the MySQL database takes much longer:

```bash
$ time ./import_database.py
Import schema
Import Table 'wm_formula.sql'... done in 0.33 s
Import Table 'wm_formula_svg_missing.sql'... done in 0.11 s
Import Table 'wm_invalid_formula_requests.sql'... done in 0.08 s
Import Table 'wm_languages.sql'... done in 0.08 s
Import Table 'wm_raw_draw_data_1.sql'... done in 782.53 s

```

## License

The database is licensed under the [ODbL](odbl-10.txt). This license is also
used by [OpenStreetMap](http://wiki.openstreetmap.org/wiki/Open_Database_License).
A human-readable form of the license can be found at http://opendatacommons.org/licenses/odbl/summary/.

Feel free to contact [me](info@martin-thoma.de) if you have questions.

## Credits

The major part of the data is from [detexify-data](https://github.com/kirel/detexify-data).
It was included into the dataset by the user "Detexify".

## raw draw data

The most important part - the `wm_raw_draw_data` table - is too big to put it
under version control.

This data can be downloaded via [www.dropbox.com](https://www.dropbox.com/sh/rov7qyxi1c00dmi/AADLbZitMVLTQVY1D89tif8pa)

## Importing

* Download this repository
* Download all `wm_raw_draw_data` files and put them into
  `database/complete-dump/single-tables` (should be at least 24)
* adjust the `/var/www/write-math/website/clients/python/db.config.yml`
* create a `write-math` MySQL database
* `./clean_database.py`: About 5 seconds
* `./import_database.py`: 5-6 hours