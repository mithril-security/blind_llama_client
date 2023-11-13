#!/bin/sh
set -e  # Exit if any command fails

sed -i '/<head>/a <meta name="description" content="Tour BlindLlama's APIs: Query open-source models with guaranteed data confidentiality, protecting user info from admins.">' $READTHEDOCS_OUTPUT/html/docs/getting-started/quick-tour/index.html