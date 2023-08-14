# Hardened environments
________________________________________________________

One of the key concepts behind BlindLlama to ensure data privacy is hardened environments. The server that serves AI to users has been stripped of all possible ways to expose data to the outside, including to the admins operating such service. 

This means in practice that all I/O, telemetry, logs, etc. have been removed. Only users encrypted data is allowed to go inside the hardened environment. It is then decrypted inside this hardened environment, used for analysis only, and only results of the inference are allowed to leave the hardened environment These are the private, secure environments in which we deploy our APIs.

Those measures ensure that users’ data remains private, as it does not leave the hardened environment, therefore preventing any exposure to even our admins.

We block service provider access to the environment so that third-parties cannot access any data being processed by our APIs.

![hardened-env-dark](../../assets/hardened-dark.png#only-dark)
![hardened-env-light](../../assets/hardened-light.png#only-light)

We also take additional security measures to make sure our environments have a heightened security posture, such as using a minimal OS only and running the OS in RAM to mitigate the risk of data being tampered with through mounting malicious disks by running the OS in RAM.

While serving AI models inside hardened environments is necessary, it is not sufficient to fully provide privacy guarantees to users as there is no way to prove that such data protection mechanism are in place.

That is why we leverage secure hardware modules, known as TPMs, to provide cryptographic proof that such privacy controls are deployed, therefore blinding even ourselves from users’ data.

We will see in the next pages how we can use TPMs to create such irrefutable proof to convince external users their data is only handled by trustworthy code. 

<div style="text-align: left;">
  <a href="../overview" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="../TCB" class="btn">Next</a>
</div>