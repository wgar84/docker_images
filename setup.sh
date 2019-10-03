#!/usr/bin/env bash

docker build base -t base

docker build scrap -t scrap

nvidia-docker build spacy -t spacy
