I will create irregular database dumps. If you think I should update the
dump, just send me an email (info@martin-thoma.de).

![A visual overview over the database](https://raw.githubusercontent.com/MartinThoma/write-math/master/database/big-picture-database.png)

The main part of the database, the `wm_raw_data`, can be backed up within 40s
(2014-07-21) from the server. That can be done with `backup_wm_raw_draw_data.py`.

Adding all data from the sql textfiles to the MySQL database takes much longer:

```bash
$ time ./import_database.py 
Import schema
Import Table 'wm_challenges.sql'... done in 0.29 s
Import Table 'wm_formula2challenge.sql'... done in 0.07 s
Import Table 'wm_formula.sql'... done in 0.33 s
Import Table 'wm_formula_svg_missing.sql'... done in 0.11 s
Import Table 'wm_invalid_formula_requests.sql'... done in 0.08 s
Import Table 'wm_languages.sql'... done in 0.08 s
Import Table 'wm_raw_data2formula.sql'... done in 1.11 s
Import Table 'wm_raw_draw_data_1.sql'... done in 782.53 s

```