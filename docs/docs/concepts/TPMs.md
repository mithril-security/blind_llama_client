# Trusted Platform Modules (TPMs)
________________________________________________________

### Overview

TPMs are secure hardware components that are commonly used to securely store artifacts, such as passwords and encryption keys, or to ensure the integrity of a whole software supply chain. It is the latter use case which we leverage in BlindLlama.

Platform integrity with TPMs is achieved by storing measurements of the whole software stack of a machine, from the UEFI to the OS, which can then be verified (**attested**). We can also use TPMs to measure and attest additional arbitrary elements such as customizable items.

In the case of BlindLlama, we additionally attest:

+ The **BlindLlama** inference server code
+ The **weights** we serve
+ The **ssl certificate** used for secure communications

![proof-dark](../../assets/blindllama-proof-dark.png#only-dark)
![proof-light](../../assets/blindllama-proof-light.png#only-light)

### How does TPM attestation work in BlindLlama?

When a TPM-enabled system is booted, various measurements are taken, such as hashes of firmware, boot loaders, and critical system files. These measurements are then stored in the TPM's PCRs (Platform Configuration Registers), a set of registers within the TPM. 

> PCRs can be considered a log of the system state, capturing the integrity of various components during the boot process and other critical stages.

We can then request a signed quote from the TPM which contains these PCR values and is signed by the TPM's Attestation Key (AK), which is derived from a tamper-proof TPM Endorsement Key (EK), and thus cannot be falsified by a third party. 

The BlindLlama server uses this signed quote to create a cryptographic proof file for each of our APIs, which can then be verified at any time using the `verify` method available in our Python SDK.

If any of the hashes in the certificate created when deploying our server do not match with the the expected values hardcoded into our API client- an error will be raised and the end user will know this is not an authentic API built with the expected codebase on the expected stack.

![verification-light](../../assets/verification-cropped.png)

By enabling users to verify that our code and stack have not been modified or tampered with, we are able to provide robust assurances about code integrity to end users.

<div style="text-align: right;">
  <a href="../attested-tls" class="btn">Next</a>
</div>
