#!/bin/bash

# Remove current sif file
rm -rf ml-container.sif

# Build new image
apptainer build ml-container.sif ml-container.def
