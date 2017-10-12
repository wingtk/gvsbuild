#!/usr/bin/env python3

import os

certificates = [
  '/etc/pki/tls/certs/ca-bundle.crt',
  '/etc/ssl/certs/ca-certificates.crt',
  '/etc/ssl/ca-bundle.pem',
]

for cert in certificates:
  if os.path.isfile(cert):
    print(cert)
    exit(0)

exit(1)
