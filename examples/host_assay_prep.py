#!/usr/bin/env python

import json
import logging
from cutlass import HostAssayPrep
from cutlass import iHMPSession
from pprint import pprint
import tempfile
import sys

username = "test"
password = "test"

session = iHMPSession(username, password)

print("Required fields: ")
print(HostAssayPrep.required_fields())

prep = HostAssayPrep()

prep.comment = "Hello world!"
prep.pride_id = "PRIDE ID"
prep.center = "the center"
prep.contact = "first name last name"
prep.sample_name = "name of the sample"
prep.experiment_type = "PRIDE:0000429, Shotgun proteomics"
prep.study = "prediabetes"
prep.title = "the title"

# Optional properties
prep.short_label = "the short label"
prep.urls = [ "http://prep.url" ]
prep.species = "the species"
prep.cell_type = "the cell type"
prep.tissue = "test tissue"
prep.reference = "the reference"
prep.prep_id = "the prep id"
prep.protocol_name = "name of the protocol"
prep.protocol_steps = "steps of the protocol"
prep.exp_description = "exp description"
prep.sample_description = "description of the sample"
prep.storage_duration = 30

print("Creating a temp file for example/testing purposes.")
temp_file = tempfile.NamedTemporaryFile(delete=False).name
print("Local file: %s" % temp_file)

# HostAssayPreps are 'prepared_from' a Sample
prep.links = { "prepared_from": [ "610a4911a5ca67de12cdc1e4b4011876" ] }

prep.tags = [ "prep", "ihmp" ]
prep.add_tag("another")
prep.add_tag("and_another")

print(prep.to_json(indent=2))

if prep.is_valid():
    print("Valid!")

    success = prep.save()

    if success:
        prep_id = prep.id
        print("Succesfully saved prep ID: %s" % prep_id)

        prep2 = HostAssayPrep.load(prep_id)

        print(prep2.to_json(indent=2))

        deletion_success = prep.delete()

        if deletion_success:
            print("Deleted prep with ID %s" % prep_id)
        else:
            print("Deletion of prep %s failed." % prep_id)
    else:
        print("Save failed")
else:
    print("Invalid...")
    validation_errors = prep.validate()
    pprint(validation_errors)
