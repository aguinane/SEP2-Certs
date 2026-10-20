# SEP2-Certs

Create and verify IEEE 2030.5 (SEP2) PKI certificates

## Certificate Creation

Note the below CLI commands are only intended for testing purposes.
For production certificates, additional functions and policies may be required.

### Signing Certificates

Create a SERCA:

```sh
uvx sep2cert create-serca
```

Create a MICA:

```sh
uvx sep2cert create-key certs/mica.key
uvx sep2cert create-csr certs/mica.key --org-name "Example Org" --country-name "AU" --common-name "IEEE 2030.5 MICA" --serial-no "1"
uvx sep2cert create-mica certs/mica.csr certs/serca.pem certs/serca.key
```


### Device Certificates

To create a device certificate, first create a Key and Certificate Signing Request (CSR).

```sh
uvx sep2cert create-key certs/dev-ABC.key
uvx sep2cert create-csr certs/dev-ABC.key 
```

Once you have the CSR, build the cert by signing it with the MICA.

```sh
uvx sep2cert create-cert certs/dev-ABC.csr certs/mica.pem certs/mica.key --pen 12345 --serno ABC
```

## Certificate Inspection

Get the LFDI for a certificate. It will also do some validation checks.

```sh
uvx sep2cert info certs/dev-ABC-cert.pem
```
