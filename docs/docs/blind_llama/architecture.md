# Architecture
________________________________________________________

BlindLlama is composed of two main parts:

+ An **open-source client-side Python SDK** that verifies the remote Zero-trust AI models we serve are indeed guaranteeing data sent is not exposed to us.
+ An **open-source server** that serves models without any exposure to us as the server is hardened and removed potential leakage channels from network to logs, and provides cryptographic proof those privacy controls are indeed in place using TPMs.

The server combines a hardened AI server with attested TLS using [TPMs](../concepts/TPMs.md).

The client performs two main tasks:

+ **Verifying that the server it communicates with is the expected hardened AI server** using attestation.
+ **Securely sending data** to be analyzed by a remote AI model using attested TLS to ensure data is not exposed.

The server has two main tasks:

+ It **loads a hardened AI server** which is inspected to ensure no data is exposed to the outside.
+ It **serves models using the hardened AI server that can be remotely verified** using attestation.