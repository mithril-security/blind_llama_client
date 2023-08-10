from pydantic import BaseModel, validator, ValidationError
from typing import Optional
from .errors import *

from grpc import ssl_channel_credentials

import blindllama.pb.licensing_pb2 as licensing_pb2
import blindllama.pb.licensing_pb2_grpc as licensing_pb2_grpc

import os
import grpc
import requests

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
            api_key (str): The API key to use the service. Default to None.
        Returns:
        """

        channel = grpc.secure_channel(
                MITHRIL_SERVICES_URL,
                ssl_channel_credentials(),
            )

        stub = licensing_pb2_grpc.LicensingServiceStub(channel)
        enclave_request = licensing_pb2.GetEnclaveRequest(api_key=api_key)

        response = stub.GetEnclave(enclave_request)
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
        return resp.text
        

def connect(api_key: str = "") -> Client:
    """Connect to the BlindLlama service.
    Args:
        api_key (str): The API key to use the service. Default to None.
    Returns:
        Client: A connection to the BlindLlama service.
    """
    return Client(api_key)
