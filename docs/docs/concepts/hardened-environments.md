# Hardened environments
________________________________________________________

## What are hardened environments?

Hardened environments are the name we give to the secure, isolated environments that the BlindLlama API is deployed within. At the heart of hardened environments is the principle that the AI/software provider (Mithril Security in the case of BlindLlama) should not have access to the environment in which the BlindLlama API is deployed, meaning we cannot manipulate or access user data.

Protecting data within an environment from external access and manipulation, is not a new concept, with one of the most robust examples coming in the form of [Confidential Computing's](https://www.ibm.com/topics/confidential-computing) [Trusted Execution Environments](https://www.techtarget.com/searchitoperations/definition/trusted-execution-environment-TEE).

Let's now find out more about BlindLlama's hardened environments and we protect these environments from outside access.

## How do we create hardened environments in BlindLlama?

We create "hardened" environments by modifying the server image and the VM configuration on which the server image is executed to remove all possible ways to expose data to the outside, including to the admins operating the service. In practice, this means that all I/O, telemetry, logs, etc. have been removed to prevent any data exposure, even to our admins.

Users' data is encrypted up until it arrives in our verified hardened environment. It is decrypted within the hardened environment for analysis only and only results of the inference returned to the end user are allowed to leave that environment.

![hardened-env-dark](../../assets/hardened-dark.png#only-dark)
![hardened-env-light](../../assets/hardened-light.png#only-light)

We also take additional security measures to make sure our environments have a heightened security posture, such as using a minimal OS only and running the OS in RAM to mitigate the risk of data being tampered with through mounting malicious disks by running the OS in RAM.

While serving AI models inside hardened environments is necessary, it is not sufficient to fully provide privacy guarantees to users as there is no way to prove that such data protection mechanism are in place.

That is why we leverage secure hardware modules, known as TPMs, to provide cryptographic proof that such privacy controls are deployed, therefore blinding even ourselves from users’ data.

<div style="text-align: left;">
  <a href="../overview" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="../TCB" class="btn">Next</a>
</div>