# Attested TLS
________________________________________________________

## What is TLS?

BlindLlama protects data in transit, aka. when data is sent as part of end user queries or responses are returned to the end user, using TLS.

Transport Layer Security, or TLS, refers to a secure protocol used for host-to-host, such as client to server, communications.

TLS keeps all data sent between two hosts safe by encrypting the data using a unique session key known to the two parties. The data remains encrypted in transit before being decrypted by the receiving party.


## What is attested TLS?

For BlindLLama, we not only use TLS to protect user data in transit but we use secure hardware [TPMs](./TPMs.md) to prove that the client is really talking to the authentic BlindLlama API server.

### How does it work?

Let's take a look at how this works step-by-step:

**Server side**:

1. Mithril Security deploys the API server on Mithril Cloud
2. On deployment, the server creates a tls-terminating reverse proxy using [Caddy](https://caddyserver.com/). Caddy takes care of generating the TLS certificate required for secure communications. The client will communicate with this reverse proxy server, which will relay the inbound/outbound communications to the BlindLlama server.
3. The caddy-generated TLS certificate is hashed by the BlindLlama server and stored in the TPM platform register PCR15. For more details about TPMs and PCRs, see our guide on [TPMs](./TPMs.md).
4. The server generates a cryptographic proof file that includes all the hashed values stored in the TPM's PCRs. The TLS certificate is therefore included in the proof file, which is then shared with clients when they connect with the server.

[tls-hash](../../assets/tls-hash.png)

**Client-side**:

1. When the end user connects to the BlindLlama server, the client will receive the following from the server:
  + The server's TLS certificate from the connection
  + The cryptographic proof file from the server

[certificates](../../assets/certificates.png)

2. This proof file which contains the hash of the server's TLS certificate is automatically verified against the certificate of the current connection. 
3. If the TLS certificate hash in the proof file does not match a hash of the TLS certificate of the server in the current connection, the connection will fail and an error is raised.

[matching](../../assets/matching.png)


<div style="text-align: left;">
  <a href="../TPMs" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="https://blindllama.readthedocs.io/en/latest/" class="btn">Home</a>
</div>