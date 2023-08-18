# How we protect your data
________________________________________________________

On this page, we will present a global overview of how we ensure that data sent to our Zero-trust AI APIs remains confidential and how we prove that even our own admins cannot see users’ data. The [concepts section](../concepts/overview.md) provides a more in-depth explanation of the building blocks we use to ensure user data remains private in our Zero-trust AI APIs.

There are two main phases to how we ensure privacy:

+ **Secure toolchain building:** In an offline phase, we prepare the hardened verifiable AI server and the client SDK and then have our code audited.
At the end of this process, users will know that when using our Python SDK, they will be able to verify that they are talking to a privacy-friendly AI service that will not expose their data.

+ **Secure AI consumption:** Once users have confidence in our Python SDK to verify that the remote AI service it talks to cannot expose data, they can communicate with the server, verify that it is a genuine hardened AI server, and then send data to it securely.

## Server side: Secure toolchain building

![toolchain-light](../../assets/secure-tooling-light.png#only-light)
![toolchain-dark](../../assets/secure-tooling-dark.png#only-dark)

### 1. Hardening the AI server to ensure privacy

We remove all admin access from the AI server, such as SSH access to the machine, logs, telemetry, I/O, etc. This means that once the AI server is running, we are *virtually blind* to data sent to us. Because we have no access to data, we can neither see it nor use it for any other purposes.

We provide more details about **hardened environments** in our [concepts guide](../concepts/hardened-environments.md).

### 2. Proving privacy controls are applied

While other solutions may also claim to put similar control in place, there is currently no robust evidence that AI providers will do what they say they will do. Even where a code base is open-source, users cannot easily verify the final application they interact with is built from this exact version of the code.

With BlindLlama, we use secure hardware, [Trusted Platform Modules (TPMs)](../concepts/TPMs.md), to create a certificate with cryptographic proof that the hardened server we developed previously really is deployed in our backend. Before sending any data, end users can verify this certificate to make sure they are talking to a privacy-preserving AI infrastructure using our client-side SDK. 

We provide more information about TPMs in our [concepts guide](../concepts/TPMs.md).

### 3. Auditing the whole stack

The security and privacy we provide are derived from code integrity, i.e. having cryptographic proof that the AI service we talk to is a secure and trustworthy one.

Therefore, for users to fully trust us, there needs to be reviews of both the Python SDK that performs verification, as we must ensure it performs these verifications correctly, and the BlindLlama server.

Our code is open-source and we encourage the community to review our codebase. We also have already had one of our similar AI deployment solutions, [BlindAI](https://github.com/mithril-security/blindai), audited by [Quarkslab](https://www.quarkslab.com/). This is to provide a high level of confidence that our hardened environment for privacy-friendly AI consumption implements all the security checks we say it does.

You can find more about the low-level details of our implementation of a Zero-trust AI service using hardened AI servers that can be verified with TPMs in our [advanced security section](../advanced-security/overview.md)(**coming soon!**).


## Client side: Secure AI consumption

![consumption-light](../../assets/consumption-light.png#only-light)
![consumption-dark](../../assets/consumption-dark.png#only-dark)

### 1. Attestation

Before any data is sent, a user can verify that they are communicating with a hardened AI server that does not expose data.

This is done by verifying a certificate which contains a cryptographic proof derived from the secure hardware that attests that a specific code base is launched.

We can verify that the code base launched corresponds to the audited/verified codebase of the previous step by making sure the hash measured with the remote server corresponds to the hash of the trustworthy server.

### 2. Attested TLS

Once the user knows they are talking to a hardened AI server, they can use a public TLS key attached to the certificate, which is associated with a private TLS key that lives inside the hardened environment and is not accessible to anyone, even Mithril Security admins, to initiate a TLS connection that ends inside the hardened AI server.

More information about attestation and attested TLS can be found in our [concepts guide](../concepts/attested-tls.md).