# Trusted Computing Base (TCB)
________________________________________________________

Before talking about the actual technology that allows us to provide code integrity, aka cryptographic proof that a specific code base is used in the backend, we have to first cover the notion of Trusted Computing Base (TCB).

TCB refers to the different technical components you need to trust, from the hardware all the way up to the software, through the hypervisor, OS, and so on.
We refer to the page on TCB and parties that are trusted in regular AI SaaS and Zero-trust AI SaaS.

Let's take a look at the TCB of a typical AI API vs BlindLLama's TCB.

![tcb-dark](../../assets/tcb-dark.png#only-dark)
![tcb-light](../../assets/tcb-light.png#only-light)

With a typical AI API, the Cloud provider buys the **hardware** and **provides a VM with a particular OS** through a **hypervisor** to **the AI API provider**, who deploys **their server code and model** on the VM. 

With BlindLlama, we still have to trust the **Cloud provider's hardware & hypervisor** but we deploy an auditable OS and server code which are attested using secure hardware, TPMS. We will see in [the next section](./TPMs.md) how TPMs can provide non-forgeable measurements of the TCB to attest that a specific code is loaded.

> Note, this is simplified as there are many more components that are part of the stack we could have included, such as the bootloader, kernel, etc.

<div style="text-align: left;">
  <a href="../hardened-environments" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="../TPMs" class="btn">Next</a>
</div>
