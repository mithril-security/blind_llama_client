# How we protect your data
________________________________________________________

We will present in this page the overall idea of how we ensure that data sent to our Zero-trust AI APIs remain confidential and especially prove that even our own admins cannot see users’ data. The concepts section provides more in-depth explanation of the building blocks that make our Zero-trust AI APIs preserve the privacy of data sent to us.

There are two main phases to ensure privacy:

+ **Secure toolchain building:** in an offline phase, we prepare the hardened verifiable AI server, the client SDK and have everything audited.
At the end of this process, users will know that when using our Python SDK, they will be able to verify that they are talking to a privacy-friendly AI service that will not expose their data.

![toolchain-light](../../assets/toolchain-light.png#only-light)
![toolchain-dark](../../assets/toolchain-dark.png#only-dark)

+ **Secure AI consumption:** once users trust the Python SDK to properly verify that the remote AI service it talks to cannot expose data, they can communicate with the server, verify that indeed the hardened AI server is deployed in the backend, and then send data securely.

## Secure toolchain building

### 1. Hardening the AI server to ensure privacy

We remove all admin access from the AI server, such as SSH access to the machine, logs, telemetry, I/O, etc. so that once the AI server is running, we are *virtually blind* to data sent to us. Because we have no access to data, we can neither see it or use it for other purposes.

We provide more details about **hardened environments** on our [concepts page](./concepts.md/#hardened-environments).

### 2. Proving privacy controls are applied

While other solutions can also claim that they put such control in place, there is today no actual proof that AI providers will do what they say they will do. Even where a code base is open-source, users cannot easily verify the final application they interact with is built from this exact version of the code.

With BlindLlama, we use secure hardware, Trusted Platform Modules (TPMs), to create a certificate with cryptographic proof that the hardened server we developed previously is indeed deployed in our backend. Before sending any data, external users can verify this certificate to make sure they talk to a privacy-preserving AI infrastructure using our client-side SDK. 

Basically, the TPMs create a hash of the whole stack used to perform AI serving, from the OS all the way to our hardened AI server. 

We provide more information about TPMs on our [concepts page](./concepts.md/#trusted-platform-modules-tpms).

### 3. Auditing the whole stack

The security and privacy we provide are derived from code integrity, i.e. having cryptographic proof that the AI service we talk to is a secure and trustworthy one.

Therefore for users to fully trust us, there needs to be reviews of both the Python SDK that performs verification, as it must itself be verified to ensure the right verifications are done, and also verify the backend, aka 

Our code is open-source for people to review it, and we have previously had BlindAI, a similar AI deployment solution audited. We will have BlindLlama audited, too to provide a high level of confidence that our hardened environment for privacy-friendly AI consumption indeed implements all the security checks we mention.

You can find more about the low-level details of our implementation of a Zero-trust AI service using hardened AI servers that can be verified with TPMs in our advanced security section.


## Secure AI consumption

![consumption-light](../../assets/consumption-light.png#only-light)
![consumption-dark](../../assets/consumption-dark.png#only-dark)

### 1. Attestation

Before any data is sent, a user can verify that an hardened AI server that does not expose data to the outside, including to our admins, is indeed deployed.
This is done by verifying a certificate which contains a cryptographic proof derived from the secure hardware that attests that a specific code base is launched.

We can verify that the code base launched corresponds to the audited/verified codebase of the previous step by making sure the hash measured with the remote server corresponds to the hash of the trustworthy server.

### 2. Attested TLS

Once the user knows they are talking to a hardened AI server, they can use a public key attached to the certificate, which is associated with a private key that only lives inside the hardened environment and is not accessible even to us, to initiate a TLS connection that ends inside the hardened AI server.

More information about attestation and attested TLS can be found on the [concepts page](./concepts.md/#attested-tls)