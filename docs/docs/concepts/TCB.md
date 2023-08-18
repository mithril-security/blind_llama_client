# Trusted Computing Base (TCB)
________________________________________________________

## What is the TCB?

Normally, when you run an application on a machine, you need to trust multiple elements: from the hardware of the machine you deploy your application on, to the application itself, through the operating system, hypervisor, etc. This doesn't mean we "trust" them in the everyday sense of the word- this means that our application could be affected by a bug or vulnerability in these elements! 

These trusted elements make up what we call the **Trusted Computing Base** or **TCB** of our application.

With a typical AI API, the Cloud provider buys the **hardware** and provides a VM with a particular **OS** through a **hypervisor** to the AI API provider, who deploys **their server code and model weights** on that VM.

These elements all need to be trusted and make up the TCB of the API.

## What is the TCB for BlindLlama?

With BlindLlama, like with a typical API set-up, we still have to trust the **Cloud provider's hardware & hypervisor**. However, we deploy an auditable OS and server code which are verified using secure hardware-based attestation, which we will learn about in [the next section](./TPMs.md).

![tcb-dark](../../assets/tcb-dark.png#only-dark)
![tcb-light](../../assets/tcb-light.png#only-light)

> Note, this is simplified as there are many more components that are part of the stack we could have included, such as the bootloader, kernel, etc.

<div style="text-align: left;">
  <a href="../hardened-environments" class="btn">Back</a>
</div>

<div style="text-align: right;">
  <a href="../TPMs" class="btn">Next</a>
</div>
