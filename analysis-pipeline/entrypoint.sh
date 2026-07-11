#!/bin/sh

# Used for copying over secret variables
export EDGAR_IDENTITY=$(cat /run/secrets/EDGAR_IDENTITY)
exec "$@"