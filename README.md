# SEP2-Certs

Create and verify IEEE 2030.5 (SEP2) PKI certificates

## Certificate Inspection

Get the LFDI for a certificate. It will also do some validation checks.

```sh
python -m sep2cert cert-lfdi certs/dev-ABC-cert.pem
```

## Certificate Creation

Note the below CLI commands are only intended for testing purposes.
For production certificates, additional functions and policies may be required.

### Signing Certificates

Create a SERCA, and a MICA.

```sh
python -m sep2cert create-serca
python -m sep2cert create-mica certs/serca.pem certs/serca.key
```

### Device Certificates

To create a device certificate, first create a Key and Certificate Signing Request (CSR).

```sh
python -m sep2cert create-key --key-file certs/dev-ABC.key
```

Once you have the CSR, build the cert by signing with the MICA.

```sh
python -m sep2cert create-cert certs/dev-ABC.csr certs/mica.pem certs/mica.key --pen 12345 --serno ABC
```
