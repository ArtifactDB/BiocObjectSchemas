# Bioconductor object schema 

## Overview

This repository contains JSON schemas for saving Bioconductor objects to file using a language-agnostic format.
Each schema generally corresponds to a single Bioconductor class and contains the metadata required to restore that object in memory.
We use both schema-based composition and inheritance to capture complex object classes and their BioC inheritance hierarchy.
The aim is to portably save and read BioC objects in different language ecosystems like R (obviously), Python and Javascript.
