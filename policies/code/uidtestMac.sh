#!/bin/bash

chown test ../../file_priv.txt

chown test setuidexample
chmod u+s setuidexample

chown root ../../runit
chmod u+s ../../runit
