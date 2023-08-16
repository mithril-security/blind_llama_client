# Attested TLS
________________________________________________________

## What is TLS?

**BlindLlama protects data in transit**, aka. when data is sent as part of end user queries or responses are returned to the end user, **using TLS**.

> Transport Layer Security, or TLS, refers to a secure protocol used for host-to-host, such as client to server, communications.
  
  TLS keeps all data in transit between two hosts safe by encrypting it before it is sent and decrypting it after it is has been received by the other party.

During an initial phase known as the TLS handshake, both parties authenticate each other and exchange settings and cryptographic material for the upcoming connection. The handshake relies on asymmetric cryptography through the use of certificates. 

The main steps of the handshake are the following:

1. The client sends a message to the server to initiate the connection along with a set of possible settings.
2. The server answers with its certificate and a choice of settings among the one proposed by the server.
3. The client verifies the identity of the server by checking it has a valid certificate (i.e. a certificate issued by a trusted Certificate Authority). It then encrypt some cryptographic material to be shared with the server with the server certificate which contains a public key. Only the server will be able to decrypt these data with its private key.
4. When using mutual authentication, the client may also be requested to send its certificate to the server which will verify it.
5. Both the client and server use the now shared cryptographic material to derive a unique session key. This key is used to symmetrically encrypt the rest of the communication as symmetric encryption is much faster than asymmetric encryption.

## What is attested TLS?

For BlindLLama, we not only use TLS to protect user data in transit but we use secure hardware [TPMs](./TPMs.md) to prove that the client is really talking to the authentic BlindLlama API server.

### How does it work?

Let's take a look at how this works step-by-step:

#### Server side

1. Mithril Security deploys the API server on Mithril Cloud
2. On deployment, the server creates a tls-terminating reverse proxy using [Caddy](https://caddyserver.com/). Caddy takes care of generating the TLS certificate required for secure communications. The client will communicate with this reverse proxy server, which will relay the inbound/outbound communications to the BlindLlama server.
3. The caddy-generated TLS certificate is hashed by the BlindLlama server and stored in the TPM platform register PCR15. For more details about TPMs and PCRs, see our guide on [TPMs](./TPMs.md).
4. The server generates a cryptographic proof file that includes all the hashed values stored in the TPM's PCRs. The TLS certificate is therefore included in the proof file, which is then shared with clients when they connect with the server.


![tls-hash-light](../../assets/tls-hash-light.png#only-light)
![tls-hash-dark](../../assets/tls-hash-dark.png#only-dark)


#### Client side

When the end user connects to the BlindLlama server, the client will receive the following from the server:
  + The server's TLS certificate from the connection
  + The cryptographic proof file from the server


![certificates-light](../../assets/certificates-light.png#only-light)
![certificates-dark](../../assets/certificates-dark.png#only-dark)

This proof file contains a hash of the server's TLS certificate, which is automatically verified against the certificate of the current connection. 

If the TLS certificate hash in the proof file does not match a hash of the TLS certificate of the server in the current connection, the connection will fail and an error is raised.

![matching-light](../../assets/matching-light.png#only-light)
![matching-dark](../../assets/matching-dark.png#only-dark)

As detailed [in the previous section](./TPMs.md), the proof file also contains hashes relating to the stack of the machine the server is deployed on, the inference server's code and the model's weights. This means not only are we sure we are connecting to the correct server using TLS but we know that this server is serving the expected code and model!

<div style="text-align: left;">
  <a href="../TPMs" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="https://blindllama.readthedocs.io/en/latest/" class="btn">Home</a>
</div>