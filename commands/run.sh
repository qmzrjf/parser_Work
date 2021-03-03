#!/bin/bash

cd ..
rm DATA/JSON_DATA/*
rm DATA/TEXT/*
rm DATA/DB/*
python3 parser/main.py
