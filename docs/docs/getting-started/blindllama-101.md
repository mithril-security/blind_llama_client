# BlindLlama 101: how we make AI Zero-trust

________________________________________________________

## Architecture

BlindLlama is composed of two main parts:

+ An **open-source client-side Python SDK** that verifies the remote Zero-trust AI models we serve are indeed guaranteeing data sent is not exposed to us.
+ An **open-source server** that serves models without any exposure to us as the server is hardened and removed potential leakage channels from network to logs, and provides cryptographic proof those privacy controls are indeed in place using TPMs.

The server combines a hardened AI server with attested TLS using [TPMs](./concepts.md#trusted-platform-modules-tpms).

The client performs two main tasks:

+ **Verifying that the server it communicates with is the expected hardened AI server** using attestation.
+ **Securely sending data** to be analyzed by a remote AI model using attested TLS to ensure data is not exposed.

The server has two main tasks:

+ It **loads a hardened AI server** which is inspected to ensure no data is exposed to the outside.
+ It **serves models using the hardened AI server that can be remotely verified** using attestation.

## Trust model

On this page, we will explain more precisely what components/parties have to be trusted when using BlindLlama.

To understand better which components and parties are trusted with BlindLlama, let’s start by examining what is trusted with regular AI services.

To do so, we will use the concept of a [Trusted Computing Base (TCB)](./concepts.md/#tcb), which refers to the set of all hardware, firmware, and software components that are critical to a system's security.

### Trusted Computing Base with regular AI providers

We can imagine that an AI provider serves AI APIs to their users using a Cloud infrastructure. Then the parties to be trusted are:

+ **The AI provider**: they provide the software application that is in charge of applying AI models to users’ data.

+ **The Cloud provider**: they provide the infrastructure, Hypervisor, VMs, OS, to the AI provider.

+ **The hardware providers**: they provide the lowest physical components, CPU, GPU, TPMs, etc. to the Cloud provider who then manages those to resell infrastructure to the AI providers. 

The higher the party in the stack, the closer they are to the data, and the more they are in a position to expose data.

In most scenarios today, there is often blind trust in the AI provider, aka we send data to them without any technical guarantees that they will do what they said they would do. For instance, the AI provider could say they just do inference on data, while they could actually train models on users’ data.

For privacy-demanding users that require more technical guarantees, they often choose not to send data to AI providers as they cannot trust them with their confidential data.

### Trusted parties with BlindLlama

With BlindLlama, we remove the AI provider from the list of trusted parties. When models are served with BlindLlama, users' data cannot be seen by the AI provider because we use a Zero-trust AI infrastructure that removes the service/AI provider from the trust base. We can prove such controls are in place using [TPM-based attestation](./concepts.md/#trusted-platform-modules-tpms).

![trust-model-light](../../assets/trust-model-light.png#only-light)
![trust-model-dark](../../assets/trust-model-dark.png#only-dark)