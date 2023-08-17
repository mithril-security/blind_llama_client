from pydantic import BaseModel, validator, ValidationError
from typing import Optional
from .errors import *

from grpc import ssl_channel_credentials

import blind_llama.pb.licensing_pb2 as licensing_pb2
import blind_llama.pb.licensing_pb2_grpc as licensing_pb2_grpc

import os
import grpc
import requests
import json

MITHRIL_SERVICES_URL = os.getenv("MITHRIL_SERVICES_URL", "api.cloud.mithrilsecurity.io")

class BlindLlamaDebugModeWarning(Warning):
    pass

class PromptRequest(BaseModel):
    inputs: str

    @validator("inputs")
    def valid_input(cls, v):
        if not v:
            raise ValidationError("The prompt cannot be empty")
        return v

class Client():
    """A class to represent a connection to a BlindLlama server."""

    def __init__(
        self,
        api_key: str = "",
    ):
        """Connect to the BlindLlama service.
        You needs to provide an API key in order to use the service. 
        Args:
            api_key (str): The API key to use the service. You can either specify an API key here or use the variable environment BLIND_LLAMA_API_KEY. If you specified an API key using the variable environment BLIND_LLAMA_API_KEY, the argument api_key will be ignored. You can get one API key on https://cloud.mithrilsecurity.io/. Default to None.
        Returns:
        """

        channel = grpc.secure_channel(
                MITHRIL_SERVICES_URL,
                ssl_channel_credentials(),
            )

        api_key_env = os.getenv("BLIND_LLAMA_API_KEY", "")
        stub = licensing_pb2_grpc.LicensingServiceStub(channel)
        try:
            enclave_request = licensing_pb2.GetEnclaveRequest(api_key=api_key_env if len(api_key_env) > 0 else api_key)
            response = stub.GetEnclave(enclave_request)
        except grpc.RpcError as rpc_error:
            raise APIKeyException(api_key, rpc_error.details())

        host_ports = response.enclave_url.split(":")
        ports = host_ports[1].split("/")


        if len(response.jwt) > 0: 
            self.jwt = response.jwt
        else:
            raise APIKeyException(
                api_key, "The API Key you provided is invalid."
            )

        self.base_url = f"http://{host_ports[0]}:{ports[1]}"

        super(Client, self).__init__()


    def predict(
        self,
        prompt: str
    ) -> str:
        """Start a prediction on the BlindLlama service.
        Args:
            prompt (str): The prompt on which you want to run a prediction on.
        Returns:
            str: The result of the prediction made by the BlindLlama server
        """

        req = PromptRequest(inputs=prompt)
        Headers = { "accesstoken" : self.jwt }
        resp = requests.post(
            self.base_url + "/",
            json=req.dict(),
            headers=Headers
        )
        ret_json = resp.json()
        generated_text = ""
        for elem in ret_json:
            if "error" in elem:
                raise PredictionException(elem['error'])
            if "generated_text" in elem:
                generated_text += f"{elem['generated_text'].strip()}\n"
        return generated_text.strip()

def connect(api_key: str = "") -> Client:
    """Connect to the BlindLlama service.
    Args:
            api_key (str): The API key to use the service. You can either specify an API key here or use the variable environment BLIND_LLAMA_API_KEY. If you specified an API key using the variable environment BLIND_LLAMA_API_KEY, the argument api_key will be ignored. You can get one API key on https://cloud.mithrilsecurity.io/. Default to None.
   
    Returns:
        Client: A connection to the BlindLlama service.
    """
    return Client(api_key)
