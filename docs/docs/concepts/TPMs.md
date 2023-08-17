# Trusted Platform Modules (TPMs)
________________________________________________________

### What is a TPM?

TPMs are secure hardware components (usually in the form of a small chip), with built-in cryptographic capabilities and secure storage in the form of Platform Configuration Registers (PCRs). They are used to store secrets such as passwords with enhanced security since they cannot be directly accessed or tampered with by the OS. They can also be used to ensure the integrity of a whole software supply chain by storing measurements relating to the whole software stack of a machine, from the UEFI to the OS, which can then be verified (**or attested**). Note that we can similarly use TPMs to measure and attest additional arbitrary elements such as customizable items.

The enhanced security and platform integrity of TPMs is leveraged and offered by all the major Cloud providers in the form of vTPMs, or virtual TPMS. Azure leverages TPMs in their [Trusted Launch](https://learn.microsoft.com/en-us/azure/virtual-machines/trusted-launch) offer, AWS with [NitroTPM & Secure Boot](https://aws.amazon.com/blogs/aws/amazon-ec2-now-supports-nitrotpm-and-uefi-secure-boot/) and Google Cloud with vTPM-compatibility provided across their [VMware Engine](https://cloud.google.com/vmware-engine/docs/vmware-ecosystem/howto-vtpm).

A Virtual Trusted Platform Module (vTPM) is a software-based representation of a physical Trusted Platform Module (TPM) chip which provides all the same functions as the physical chip. The hypervisor creates a secure and isolated region of memory which replicates the isolation of a physical TPM.

![tpm-vs-vtpm-light](../../assets/tpm-vs-vtpm-light.png#only-light)
![tpm-vs-vtpm-dark](../../assets/tpm-vs-vtpm-dark.png#only-dark)


## How do we use TPMs in BlindLlama?

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
