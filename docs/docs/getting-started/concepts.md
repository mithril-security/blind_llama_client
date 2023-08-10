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

## TCB

Normally, when you deploy an application on a machine, you have to trust multiple components: the application code itself, the operating system, the hypervisor and the hardware.

This doesn't mean we "trust" these elements in the everyday sense of the word- it means that our application could be affected by a bug or vulnerability in these elements. These trusted elements make up what we call the Trusted Computing Base or TCB of our application.

## Attested TLS

Transport Layer Security, or TLS, refers to a secure protocol used for host-to-host, such as client to server, communications.

TLS keeps all data sent between two hosts safe by encrypting the data using a unique session key known to the two parties. The data remains encrypted in transit before being decrypted by the receiving party.

We talk about attested TLS with BlindLlama because end users can verify that TLS is implemented for our APIs through TPM-based attestation which we explain in the following section.

## Intro to TPMs

### Overview

TPMs are secure hardware components that are commonly used to securely store artifacts, such as passwords and encryption keys, or to ensure the integrity of a whole software supply chain. It is the latter use case which we leverage in BlindLlama.

This is achieved by storing measurements of the whole software stack of a machine, from the UEFI to the OS, which can then be verified. We can also use TPMs to measure and attest additional customizable items- in the case of BlindLlama, we additionally attest the BlindLlama server code, and the AI models we serve and the SSL certificate used for secure communications.

### How does it work?

When a TPM-enabled system boots, various measurements are taken, such as hashes of firmware, boot loaders, and critical system files. These measurements are then stored in the TPM's PCRs (Platform Configuration Registers), a set of registers within the TPM. PCRs can be considered a log of the system state, capturing the integrity of various components during the boot process and other critical stages.

We can then check the values stored in the PCRs against known values, allowing us to attest that the software stack has not changed from the expected values.

To do this, we can request a signed quote from the TPM which contains these PCR values and is signed by the TPM's Attestation Key (AK), which is derived from a tamper-proof TPM Endorsement Key (EK), and thus cannot be falsified by a third party.

Measuring the whole software stack, plus the Blind Llama server, the models we serve and the SSL certificate we use (by registering them in the final PCR) enables us to provide assurances about code integrity to end users.