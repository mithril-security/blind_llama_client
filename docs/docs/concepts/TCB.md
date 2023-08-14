# Trusted Computing Base (TCB)
________________________________________________________

Before talking about the actual technology that allows us to provide code integrity, aka cryptographic proof that a specific code base is used in the backend, we have to first cover the notion of Trusted Computing Base (TCB).

TCB refers to the different technical components you need to trust, from the hardware all the way up to the software, through the hypervisor, OS, and so on.
We refer to the page on TCB and parties that are trusted in regular AI SaaS and Zero-trust AI SaaS.

For instance, as an external user of an AI SaaS application, here are the different components we need to trust:

![tcb-dark](../../assets/TCB-dark.png#only-dark)
![tcb-light](../../assets/TCB-light.png#only-light)

The Cloud provider typically buys the hardware and serves VMs through a hypervisor to AI providers, who then are in charge of choosing the OS and providing the AI inference server. This is simplified as there are many more components that are part of the stack we could have omitted, such as bootloader, kernel, etc.

Now that we have introduced the concept of TCB, we will see in the next page how TPMs can provide non-forgeable measurements of the TCB to attest that a specific code is loaded.

<div style="text-align: left;">
  <a href="../hardened-environments" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="../TPMs" class="btn">Next</a>
</div>
