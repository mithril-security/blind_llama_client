# Trusted Platform Modules (TPMs)
________________________________________________________

### Overview

TPMs are secure hardware components that are commonly used to securely store artifacts, such as passwords and encryption keys, or to ensure the integrity of a whole software supply chain. It is the latter use case which we leverage in BlindLlama.

Platform integrity with TPMs is achieved by storing measurements of the whole software stack of a machine, from the UEFI to the OS, which can then be verified (**attested**). We can also use TPMs to measure and attest additional arbitrary elements such as customizable items.

## How does TPM attestation work in BlindLlama?

### Server-side

#### Measuring the software stack

When the TPM-enabled machine used for server deployment is booted, various default measurements are taken, such as hashes of firmware, boot loaders, and critical system files. These hashes are stored in the TPM's PCRs (Platform Configuration Registers), a set of registers, or location in memory, within the TPM itself.

The BlindLlama server then additionally stores hashes of the following elements in PCRs:

+ The **BlindLlama** inference server code
+ The **model weights** we serve
+ The **TLS certificate** used for secure communications

Let's take a look at the PCR values used by BlindLlama and their associated PCR number:

![PCR-alloc-dark](../../assets/PCR-alloc-dark.png#only-dark)
![PCR-alloc-light](../../assets/PCR-alloc-light.png#only-light)

#### Collecting PCR values

The BlindLlama server then requests a signed quote from the TPM which contains these PCR values and is signed by the TPM's Attestation Key (AK), which is derived from a tamper-proof TPM Endorsement Key (EK), and thus cannot be falsified by a third party.

#### Creating proof file

The BlindLlama server uses the information from this signed quote to create a cryptographic proof file containing hashes from any relevant PCRs and the quote signature.

![proof-dark](../../assets/proof-dark.png#only-dark)
![proof-light](../../assets/proof-light.png#only-light)

### Client-side

#### Verifying the proof file

When an end user queries our BlindLlama API, before a secure connection can be established the client will receive and verify the server's **cryptographic proof file**. The server also sends a **certificate chain** which is used to verify that information in the proof file came from a genuine TPM.

Verification is done in done in two stages:

1. Firstly, the client verifies that the TPM signature is genuine. This is done using the `cert chain` provided by the server. The client verifies the signatures of a chain of certificates, starting with the TPM's signature and going up to a root certificate which is checked against a certificate by the Cloud/hardware provider in question.

2. Once we have established our proof file is derived from a genuine TPM, each of the hashes in this proof file is checked by the client against expected values hardcoded into the client. If any of these hashes does not match with the expected hash, an error will be raised and no user data will be sent to the server!

![matching-light](../../assets/matching-light.png#only-light)
![matching-dark](../../assets/matching-dark.png#only-dark)

By using TPMs to verify that our code and stack have not been modified or tampered with, we are able to provide robust assurances about code integrity to end users.

<div style="text-align: left;">
  <a href="../TCB" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="../attested-tls" class="btn">Next</a>
</div>
