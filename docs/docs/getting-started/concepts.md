# Concepts
________________________________________________________

## Overview

In this section, we will describe the main concepts that are at the core of BlindLlama, namely how we harden an AI inference server to remove data exposure even to our admins and how we use TPMs to provide cryptographic proof to outsiders that those controls are in place.

The first concept to understand is how we make an 

Then we will explain how secure hardware with TPMs can provide irrefutable proof we indeed serve AI models only inside hardened environments that mask customers to us.

## Hardened environments

One of the key concepts behind BlindLlama is hardened environments. These are the private, secure environments in which we deploy our APIs.

We block service provider access to the environment so that third-parties cannot access any data being processed by our APIs.

We also take additional security measures to make sure our environments have a heightened security posture, such as using a minimal OS only and running the OS in RAM to mitigate the risk of data being tampered with through mounting malicious disks by running the OS in RAM.

![hardened-env-dark](../../assets/hardened-dark.png#only-dark)
![hardened-env-light](../../assets/hardened-light.png#only-light)

## TCB

Normally, when you deploy an application on a machine, you have to trust multiple components: the application code itself, the operating system, the hypervisor and the hardware.

This doesn't mean we "trust" these elements in the everyday sense of the word- it means that our application could be affected by a bug or vulnerability in these elements. These trusted elements make up what we call the Trusted Computing Base or TCB of our application.

![tcb-dark](../../assets/TCB-dark.png#only-dark)
![tcb-light](../../assets/TCB-light.png#only-light)

## Trusted Platform Modules (TPMs)

### Overview

TPMs are secure hardware components that are commonly used to securely store artifacts, such as passwords and encryption keys, or to ensure the integrity of a whole software supply chain. It is the latter use case which we leverage in BlindLlama.

Platform integrity with TPMs is achieved by storing measurements of the whole software stack of a machine, from the UEFI to the OS, which can then be verified (**attested**). We can also use TPMs to measure and attest additional customizable items. 

In the case of BlindLlama, we measure and provide proofs of:
+ The **software stack** of the environment our API is deployed on
+ The **BlindLlama** server image
+ The **weights** of the model our API serves
+ Our server's **ssl certificate**

![proof-dark](../../assets/blindllama-proof-dark.png#only-dark)
![proof-light](../../assets/blindllama-proof-light.png#only-light)

### How does TPM attestation work in BlindLlama?

When a TPM-enabled system is booted, various measurements are taken, such as hashes of firmware, boot loaders, and critical system files. These measurements are then stored in the TPM's PCRs (Platform Configuration Registers), a set of registers within the TPM. 

> PCRs can be considered a log of the system state, capturing the integrity of various components during the boot process and other critical stages.

We can then request a signed quote from the TPM which contains these PCR values and is signed by the TPM's Attestation Key (AK), which is derived from a tamper-proof TPM Endorsement Key (EK), and thus cannot be falsified by a third party. 

The BlindLlama server uses this signed quote to create a cryptographic proof file for each of our APIs, which can then be verified at any time using the `verify` method available in our Python SDK.

If any of the hashes in the certificate created when deploying our server do not match with the the expected values hardcoded into our API client- an error will be raised and the end user will know this is not an authentic API built with the expected codebase on the expected stack.

![proof-fail](../../assets/verification-cropped.png)

By enabling users to verify that our code and stack have not been modified or tampered with, we are able to provide robust assurances about code integrity to end users.


## Attested TLS

Transport Layer Security, or TLS, refers to a secure protocol used for host-to-host, such as client to server, communications.

TLS keeps all data sent between two hosts safe by encrypting the data using a unique session key known to the two parties. The data remains encrypted in transit before being decrypted by the receiving party.

With BlindLlama, end users can verify that TLS is implemented for our APIs as part of TPM-based attestation.