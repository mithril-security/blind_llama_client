# Attested TLS
________________________________________________________

## What is attested TLS?

Attested TLS combines the security of data in transit with [TLS](https://hpbn.co/transport-layer-security-tls/) with the security and privacy of data in computation via an isolated and hardware-attested endpoint environment.

It has been said of TLS that:

*"Using encryption on the Internet is the equivalent of arranging an armored car to deliver credit-card information from someone living in a cardboard box to someone living on a park bench."* [Source here](http://catless.ncl.ac.uk/Risks/19.37.html)

It is all very well to secure our data in transit with TLS when using APIs, but data is often left exposed and accessible once it arrives at the endpoint.

Attested TLS is often deployed in the context of [Confidential Computing](https://www.fortanix.com/platform/confidential-computing-manager/what-is-confidential-computing) where a secure TLS connection is directs communications to within an attested isolated environment, or [Trusted Execution Environments](https://www.techtarget.com/searchitoperations/definition/trusted-execution-environment-TEE), which cannot be accessed or interfered with from the outside.

By binding a TLS certificate to an attested secure environment we protect ourselves against man-in-the-middle (MITM) attacks, as we have proof that we are communicating with our attested secure environment and not one that is merely forwarding a quote from a valid machine.

## How does attested TLS work in BlindLlama?

Let's take a look at how we attested TLS works in BlindLlama step-by-step:

### Server side

1. We deploy the BlindLlama server on Mithril Cloud
2. On deployment, the server creates a tls-terminating reverse proxy. The reverse proxy provider takes care of generating the TLS certificate required for secure communications. The client will communicate with this reverse proxy server, which will relay the inbound/outbound communications to the BlindLlama server.
3. The caddy-generated TLS certificate is hashed by the BlindLlama server and stored in the TPM platform register PCR15. For more details about TPMs and PCRs, see our guide on [TPMs](./TPMs.md).
4. The server generates a cryptographic proof file that includes all the hashed values stored in the TPM's PCRs. The TLS certificate is therefore included in the proof file, which is then shared with clients when they connect with the server.


![tls-hash-light](../../assets/tls-hash-light.png#only-light)
![tls-hash-dark](../../assets/tls-hash-dark.png#only-dark)


### Client side

When the end user connects to the BlindLlama server, the client will receive the following from the server:
  + The server's TLS certificate from the connection
  + The cryptographic proof file from the server


![certificates-light](../../assets/certificates-light.png#only-light)
![certificates-dark](../../assets/certificates-dark.png#only-dark)

This proof file contains a hash of the server's TLS certificate, which is automatically verified against the certificate of the current connection. 

If the TLS certificate hash in the proof file does not match the hash of the TLS certificate of the server in the current connection, the connection will fail and an error is raised.

![matching-light](../../assets/matching-light.png#only-light)
![matching-dark](../../assets/matching-dark.png#only-dark)

As detailed [in the previous section](./TPMs.md), the proof file also contains hashes relating to the stack of the machine the server is deployed on, the inference server's code and the model's weights. This means not only are we sure we are connecting to the correct server using TLS but we know that this server is serving the expected code and model!

<div style="text-align: left;">
  <a href="../TPMs" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="https://blindllama.readthedocs.io/en/latest/" class="btn">Home</a>
</div>