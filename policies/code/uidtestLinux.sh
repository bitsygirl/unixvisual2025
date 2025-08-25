#!/bin/bash

chown averp ../../file_priv.txt
chgrp averp ../../file_priv.txt

chown averp setuidexample
chgrp averp setuidexample
chmod u+s setuidexample

chown root runit
chgrp root runit
chmod u+s runit
