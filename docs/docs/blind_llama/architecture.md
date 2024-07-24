---
description: "Uncover BlindLlama's architecture: Open-source client-side Python SDK and server with three integral components."
---

# Architecture
________________________________________________________

BlindLlama is composed of two main parts:

1. An **open-source client-side Python SDK** that verifies the **hardened environment** is indeed guaranteeing data sent is not exposed to malicious servers that could intercept and forward it.
2. An **open-source server** we call enclaves, made up of three key components which work together to serve models without any exposure to the AI provider. We remove all potential server-side leakage channels from network to logs and provide cryptographic proof that those privacy controls are in place using TPMs.

![arch-light](../../assets/arch-light.png#only-light)
![arch-dark](../../assets/arch-dark.png#only-dark)

## Client

The client performs two main tasks:

+ **Verifying that it is communicating with the expected hardened AI environment** using attestation.
+ **Securely sending data** to be analyzed by a remote AI model using attested TLS to ensure data is not exposed.

## Server

The server is split into three components:

+ The **hardened AI container**: This element serves the AI model in an isolated [hardened environment](../concepts/hardened-systems.md).
+ The **attesting launcher**: The launcher loads the hardened AI container and creates a proof file which is used to verify we are communicating with a genuine hardened environment using [TPM-based attestation](../concepts/TPMs.md). 
+ The **reverse proxy**: The reverse proxy handles communications to and from the client and the container and launcher using [atested TLS](../concepts/attested-tls.md).

![serv-arch-light](../../assets/serv-arch-light.png#only-light)
![serv-arch-dark](../../assets/serv-arch-dark.png#only-dark)