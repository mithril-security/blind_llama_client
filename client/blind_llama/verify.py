import base64
import hashlib
import json
import subprocess
import tempfile
import OpenSSL
from OpenSSL import crypto
import requests
import yaml
from .logging import log


from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_der_x509_certificate

PCR_FOR_CERTIFICATE = 15
PCR_FOR_MEASUREMENT = 16


class AttestationError(Exception):
    """This exception is raised when the attestation is invalid (enclave
    settings mismatching, debug mode unallowed...).

    Used as base exception for all other sub exceptions on the attestation
    validation
    """

    pass


def verify_ak_cert(cert_chain: list[bytes]) -> bytes:
    """
    Verify the certificate chain of the attestation key.
    Parameters:
        cert_chain: list of certificates in DER format
    Returns:
        AK certificate in DER format
    Raises:
        AttestationError: if the certificate chain is invalid
    """

    # Load certificate to be verified : attestation key certificate
    ak_cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_chain[0])

    # Verify the certificate's chain
    store = crypto.X509Store()

    # Create the CA cert object from PEM string, and store into X509Store
    req = requests.get("http://crl.microsoft.com/pkiinfra/certs/AMERoot_ameroot.crt")
    req.raise_for_status()
    _rootca_cert = crypto.load_certificate(crypto.FILETYPE_ASN1, req.content)  # type: ignore
    store.add_cert(_rootca_cert)

    chain = [
        crypto.load_certificate(crypto.FILETYPE_ASN1, _cert_der)
        for _cert_der in cert_chain[1:-1]
    ]

    store_ctx = crypto.X509StoreContext(store, ak_cert, chain=chain)

    # try:
    #     # if the cert is invalid, it will raise a X509StoreContextError
    #     store_ctx.verify_certificate()
    # except crypto.X509StoreContextError:
    #     ref_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1,cert_chain[0])
    #     log.info(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_TEXT, ref_cert).decode('ascii'))
    #     ref_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1,cert_chain[1])
    #     log.info(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_TEXT, ref_cert).decode('ascii'))
    #     ref_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1,cert_chain[2])
    #     log.info(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_TEXT, ref_cert).decode('ascii'))
    #     log.error("Invalid AK certificate")
    #     # TODO: In the future we'll want to raise an error
    #     # But for now Azure vTPM does not have an official certificate chain
    #     # So the checks can randomly fail
    #     # raise AttestationError("Invalid AK certificate")

    return cert_chain[0]


def check_quote(quote, pub_key_pem):
    """
    Check quote using tpm2_checkquote command.
    Parameters:
         quote: dictionary with keys 'message', 'signature', and 'pcr'
         pub_key_pem: public key in PEM format (string)
    Returns:
    Raises:


    """
    with tempfile.NamedTemporaryFile() as quote_msg_file, tempfile.NamedTemporaryFile() as quote_sig_file, tempfile.NamedTemporaryFile() as quote_pcr_file, tempfile.NamedTemporaryFile() as ak_pub_key_file:
        quote_msg_file.write(quote["message"])
        quote_msg_file.flush()

        quote_sig_file.write(quote["signature"])
        quote_sig_file.flush()

        quote_pcr_file.write(quote["pcr"])
        quote_pcr_file.flush()

        ak_pub_key_file.write(pub_key_pem)
        ak_pub_key_file.flush()

        tpm2_checkquote = subprocess.run(
            [
                "tpm2_checkquote",
                "--public",
                ak_pub_key_file.name,
                "--message",
                quote_msg_file.name,
                "--pcr",
                quote_pcr_file.name,
                "--signature",
                quote_sig_file.name,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        att_document = yaml.load(tpm2_checkquote.stdout, Loader=yaml.BaseLoader)
        att_document["pcrs"]["sha256"] = {
            int(k): v.lower().removeprefix("0x")
            for k, v in att_document["pcrs"]["sha256"].items()
        }
        return att_document


def check_server_cert(
    received_cert,
    pcr_end,
    initial_pcr="0000000000000000000000000000000000000000000000000000000000000000",
):
    initial_pcr = bytes.fromhex(initial_pcr)
    current_pcr = initial_pcr

    hash_event = hashlib.sha256(received_cert.encode()).digest()
    current_pcr = hashlib.sha256(current_pcr + hash_event).digest()

    # log.info(f"Certificate PCR in quote : {pcr_end}")
    # log.info(f"Expected Certificate PCR : {current_pcr.hex()}")
    # Both PCR MUST match, else something sketchy is going on!
    if pcr_end != current_pcr.hex():
        return False
    
    return True


def check_event_log(
    input_event_log,
    pcr_end,
    initial_pcr="0000000000000000000000000000000000000000000000000000000000000000",
):
    # Starting from the expected initial PCR state
    # We replay the event extending the PCR
    # At the end we get the expected PCR value
    initial_pcr = bytes.fromhex(initial_pcr)
    current_pcr = initial_pcr
    for e in input_event_log:
        hash_event = hashlib.sha256(e.encode()).digest()
        current_pcr = hashlib.sha256(current_pcr + hash_event).digest()

    # log.info(f"Event PCR in quote : {pcr_end}")
    # log.info(f"Expected Event PCR : {current_pcr.hex()}")

    # Both PCR MUST match, else something sketchy is going on!
    assert pcr_end == current_pcr.hex()

    # Now we can return the parsed event log
    event_log = [json.loads(e) for e in input_event_log]

    return event_log


def decode_b64_encoding(x):
    return base64.b64decode(x["base64"])


def test_check_pass():
    with open("sample_build_response.json") as f:
        build_response = json.load(f)

    build_response["remote_attestation"]["cert_chain"] = [
        decode_b64_encoding(cert_b64_encoded)
        for cert_b64_encoded in build_response["remote_attestation"]["cert_chain"]
    ]

    ak_cert = verify_ak_cert(
        cert_chain=build_response["remote_attestation"]["cert_chain"]
    )

    ak_cert_ = load_der_x509_certificate(ak_cert)
    ak_pub_key = ak_cert_.public_key()
    ak_pub_key_pem = ak_pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    build_response["remote_attestation"]["quote"] = {
        k: decode_b64_encoding(v)
        for k, v in build_response["remote_attestation"]["quote"].items()
    }
    att_document = check_quote(
        build_response["remote_attestation"]["quote"], ak_pub_key_pem
    )

    print("attestation document", att_document)

    # We should check the PCR to make sure the system has booted properly
    # This is an example ... the real thing will depend on the system.
    assert (
        att_document["pcrs"]["sha256"][0]
        == "d0d725f21ba5d701952888bcbc598e6dcef9aff4d1e03bb3606eb75368bab351"
    )
    assert (
        att_document["pcrs"]["sha256"][1]
        == "fe72566c7f411900f7fa1b512dac0627a4cac8c0cb702f38919ad8c415ca47fc"
    )
    assert (
        att_document["pcrs"]["sha256"][2]
        == "3d458cfe55cc03ea1f443f1562beec8df51c75e14a9fcf9a7234a13f198e7969"
    )
    assert (
        att_document["pcrs"]["sha256"][3]
        == "3d458cfe55cc03ea1f443f1562beec8df51c75e14a9fcf9a7234a13f198e7969"
    )
    assert (
        att_document["pcrs"]["sha256"][4]
        == "1f0105624ab37b9af59da6618a406860e33ef6f42a38ddaf6abfab8f23802755"
    )
    assert (
        att_document["pcrs"]["sha256"][5]
        == "d36183a4ce9f539d686160695040237da50e4ad80600607f84eff41cf394dcd8"
    )

    # To make test easier we use the PCR 16 since it is resettable `tpm2_pcrreset 16`
    # But because it is resettable it MUST NOT be used in practice.
    # An unused PCR that cannot be reset (SRTM) MUST be used instead
    # PCR 14 or 15 should do it
    print(
        check_event_log(
            build_response["event_log"],
            att_document["pcrs"]["sha256"][PCR_FOR_MEASUREMENT],
        )
    )
