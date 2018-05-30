# Webapp application

This charm uses the apache layer to setup an apache website. 

The basic website installs adminer.php from a tar.

After requesting a database, it will render the template file with the database details. Note that you won't be able to connect to the database with adminer as this host is not allowed to access the database!
