#!/bin/bash

cd ..
rm JSON_DATA/*
rm TEXT/*
rm DB/*
python3 db_connect.py
python3 main.py
