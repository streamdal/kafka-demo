#!/bin/bash
plumber read kafka --topic rsvps --address="localhost:9092" --follow --json
