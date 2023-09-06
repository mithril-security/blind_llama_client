from typing import Optional, List
from pydantic import BaseModel, validator
from .errors import *
from .request_adapters import ForcedIPHTTPSAdapter
from .verify import *

import os
import requests
import json
import grpc
import blind_llama
import tempfile
import typer
import warnings

from grpc import ssl_channel_credentials

import blind_llama.pb.licensing_pb2_grpc as licensing_pb2_grpc
import blind_llama.pb.licensing_pb2 as licensing_pb2

MITHRIL_SERVICES_URL = os.getenv("MITHRIL_SERVICES_URL", "api.cloud.mithrilsecurity.io")

PCR_FOR_MEASUREMENT = 16
PCR_FOR_CERTIFICATE = 15

class AICertInvalidAttestationFormatException(AICertException):
    """AICert attestation parsing error (json)"""
    def __init__(self, err: Exception) -> None:
        self.__err = err
        self.message = f"Invalid attestation format\n{self.__err}"
        super().__init__(self.message)


class AICertInvalidAttestationException(AICertException):
    """Invalid attestation error"""
    pass


class PromptRequest(BaseModel):
    inputs: str
    temperature: float

    @validator("inputs")
    def valid_input(cls, v):
        if not v:
            raise ValidationError("The prompt cannot be empty")
        return v
    
    @validator("temperature")
    def valid_temperature(cls, v):
        if v < 0:
            raise ValidationError("Invalid temperature")
        return v

class Client():
    """A class to represent a connection to a BlindLlama server."""

    def __init__(
        self,
        verbose: bool = False
    ):
        self.verbose = verbose
        #self.__base_url = f"{openai2.api_base}:8000"
        self.__base_url = "https://llama_worker"
        self.__attest_url = "https://aicert_worker"
        self.__session = requests.Session()
        self.__session.mount(
            self.__base_url, ForcedIPHTTPSAdapter(dest_ip=blind_llama.api_base)
        )

        ca_cert = self.verify_server_certificate(blind_llama.security_config["expected_pcrs"]["codebasepcr"])

        server_ca_crt_file = tempfile.NamedTemporaryFile(mode="w+t", delete=False)
        server_ca_crt_file.write(ca_cert)
        server_ca_crt_file.flush()
        self.__session.verify = server_ca_crt_file.name

        channel = grpc.secure_channel(
                MITHRIL_SERVICES_URL,
                ssl_channel_credentials(),
            )
        
        api_key_env = blind_llama.api_key
        stub = licensing_pb2_grpc.LicensingServiceStub(channel)
        try:
            enclave_request = licensing_pb2.GetEnclaveRequest(api_key=api_key_env)
            response = stub.GetEnclave(enclave_request)
        except grpc.RpcError as rpc_error:
            raise APIKeyException(api_key_env, rpc_error.details())

        if len(response.jwt) > 0: 
            self.jwt = response.jwt
        else:
            raise APIKeyException(
                api_key_env, "The API Key you provided is invalid."
        )

        super(Client, self).__init__()

    def verify_server_certificate(self, expected_pcr):
        """Retrieve server certificate and validate it with 
        the attestation report.
        """
        session = requests.Session()
        session.mount(
                self.__attest_url, ForcedIPHTTPSAdapter(dest_ip=blind_llama.api_base)
            )
        
        attestation = session.get(f"{self.__attest_url}/aTLS",verify=False)

        attestation_json = json.loads(attestation.content)
        ca_cert = attestation_json["ca_cert"]

        # Verify quote and CA TLS certificate
        self.verify_build_response(attestation.content, ca_cert, expected_pcr)
        return ca_cert
    
    def verify_build_response(self, build_response: bytes, ca_cert = "", expected_pcr = ""):
        """Verify received attesation validity

        1. Parse the JSON reponse
        2. Check simulation mode
        3. Verify certificate chain
        4. Verify quote signature
        5. Verify boot PCRs (firmware, bootloader, initramfs, OS)
        6. Verify event log (final hash in PCR_FOR_MEASUREMENT) by replaying it (works like a chain of hashes)
        7. Verify TLS certificate (final hash in PCR_FOR_CERTIFICATE)
        
        Args:
            build_response (bytes): reponse of the attestation endpoint
            verbose (bool, default = False): whether to print verification information in stdout
        """
        try:
            build_response = json.loads(build_response)
        except Exception as e:
            AICertInvalidAttestationFormatException(e)
        
        if "simulation_mode" in build_response["remote_attestation"]:
            if self.__simulation_mode:
                warnings.warn(f"Attestation generated in simulation mode", RuntimeWarning)
                return
            else:
                raise AICertInvalidAttestationException(f"Attestation generated in simulation mode")

        build_response["remote_attestation"]["cert_chain"] = [
            decode_b64_encoding(cert_b64_encoded)
            for cert_b64_encoded in build_response["remote_attestation"]["cert_chain"]
        ]

        ak_cert = verify_ak_cert(
            cert_chain=build_response["remote_attestation"]["cert_chain"]
        )
        if self.verbose:
            warnings.warn(f"Bypassing certificate chain verification", RuntimeWarning)

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

        if self.verbose:
            typer.secho(f"Valid quote", fg=typer.colors.GREEN)

            log.info(
                f"Attestation Document > PCRs :  \n{yaml.safe_dump(att_document['pcrs']['sha256'])}"
            )

        # To make test easier we use the PCR 16 since it is resettable `tpm2_pcrreset 16`
        # But because it is resettable it MUST NOT be used in practice.
        # An unused PCR that cannot be reset (SRTM) MUST be used instead
        # PCR 14 or 15 should do it
        event_log = check_event_log(
            build_response["event_log"],
            att_document["pcrs"]["sha256"][PCR_FOR_MEASUREMENT],
        )

        measured_pcr = att_document["pcrs"]["sha256"][PCR_FOR_MEASUREMENT]

        if self.verbose:
            log.info(f"Server's Codebase PCR : {measured_pcr}")
            log.info(f"Expected Codebase PCR : {expected_pcr}")

        if expected_pcr == measured_pcr:
            if self.verbose:
                typer.secho(f"Code base PCR is expected value")
        else:
            if self.verbose:
                typer.secho(f"Codebase PCR does not match expected value")
            raise ValidationError(f"Expected Codebase PCR does not match the one provided by the server. Expected PCR: {expected_pcr} Measured PCR: {measured_pcr}")


        result = check_server_cert(
            ca_cert,
            att_document["pcrs"]["sha256"][PCR_FOR_CERTIFICATE],
        )
        if not result:
            # Disconnect destroys the runner, this might not be required for an attestation failure
            # self.disconnect()
            raise AICertInvalidAttestationException(f"Attestation validation failed.")
        
        if self.verbose:
            typer.secho(f"Valid event log")
            print(yaml.safe_dump(event_log))
            typer.secho(f"ALL CHECKS PASSED")

        warnings.warn(f"The quote from the TPM is not endorsed by the Cloud provider for the alpha version of BlindLlama v0.1. For more information look at https://github.com/mithril-security/blind_llama")

    def predict(
        self,
        prompt: str,
        temperature: float,
    ) -> str:
        """Start a prediction.
        Args:
            prompt (str): The prompt on which you want to run a prediction on.
            temperature (float): The temperature requested.
        Returns:
            str: The result of the prediction made by the server
        """

        req = PromptRequest(inputs=prompt, temperature=temperature)
        Headers = { "accesstoken" : self.jwt }
        resp = self.__session.post(
            self.__base_url + "/",
            json=req.dict(),
            headers=Headers
        )
        ret_json = resp.json()
        generated_text = ""
        for elem in ret_json:
            if "error" in elem:
                raise PredictionException(elem)
            if "generated_text" in elem:
                generated_text += f"{elem['generated_text'].strip()}\n"
        return generated_text.strip()

def create(model: str = "meta-llama/Llama-2-70b-chat-hf", prompt: str = "", temperature: float = 0.7, verbose: bool = False) -> str:
    """Start a prediction.
    Args:
        model (str): The model on which you want to run a prediction on (default to meta-llama/Llama-2-70b-chat-hf).
        prompt (str): The prompt on which you want to run a prediction on.
        temperature (float): The temperature requested (default to 0.7).
    Returns:
        str: The result of the prediction made by the server
    """
    return Client(verbose).predict(prompt, temperature)
