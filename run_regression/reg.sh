#!/bin/bash

rm e_*.txt

for a in fire mechadd mechremove wind insects; do python3 regress.py $a > e_$a.txt; done

for a in fire mechadd mechremove wind insects; do echo $a && tail -3 e_$a.txt; done
