<a name="readme-top"></a>

<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache License][license-shield]][license-url] -->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mithril-security/blind_llama">
    <img src="https://github.com/mithril-security/blindai/raw/main/docs/assets/logo.png" alt="Logo" width="80" height="80">
  </a>

<h1 align="center">BlindLlama</h1>

[![Website][website-shield]][website-url]
[![Blog][blog-shield]][blog-url]
[![Docs][docs-shield]][docs-url]
</div>

 <p align="center">
    <b>Making AI Confidential & Transparent</b><br /><br />
   <!-- 
    <a href="https://blindllama.mithrilsecurity.io/en/latest"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://aicert.mithrilsecurity.io/en/latest/docs/getting-started/quick-tour/">Get started</a>
    ·
    <a href="https://github.com/mithril-security/aicert/issues">Report Bug</a>
    ·
    <a href="https://github.com/mithril-security/aicert/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#-about-the-project">About the project</a></li>
    <li><a href="#-use-cases">Use cases</a></li>
    <li><a href="#-getting-started">Getting started</a></li>
    <li><a href="#-vision-and-roadmap">Vision and roadmap</a></li>
    <li><a href="#about-us">About us</a></li>
    <li><a href="#-contact">Contact</a></li>
  </ol>
</details>

## 📜 About the project

### Introduction

🛠️ **BlindLlama** makes it easy to use open-source LLMs by using **Zero-trust AI APIs** that abstract all the complexity of model deployment while ensuring **users’ data is never exposed** to us thanks to end-to-end protection with **secure hardware**.

🔐 To provide guarantees to developers that data sent to our managed infrastructure is not exposed, we have developed a **Zero-trust architecture to serve AI models**. 

Our backend has two key properties:

+ **Confidentiality**: Your data is **never accessible to us**. We serve AI models inside **hardened environments** that do not expose data even to our admins. All points of access, such as SSH, logs, networks, etc., are blocked to ensure the isolation of data.

+ **Transparency**: We provide you with verifiable **cryptographic proof** that these controls are in place, thanks to the use of [Trusted Platform Modules (TPMs)](https://blindllama.readthedocs.io/en/latest/docs/getting-started/concepts/).
  
	⚠️ **WARNING:** BlindLlama is still **under development**. Do not use it in production!

	We are working towards the first audit of BlindLlama in the following months. Please refer to the <a href="#-vision-and-roadmap">roadmap</a> to know the current status of the project.

We welcome contributions to our project from the community! Don't hesitate to [raise issues](https://github.com/mithril-security/blind_llama/issues) on GitHub, <a href="#-contact">reach out to us</a> or see our guide on how to audit BlindLlama (**coming soon!**).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Architecture

BlindLlama is composed of two main parts:

+ An **open-source client-side Python SDK** that verifies the remote Zero-trust AI models we serve are indeed guaranteeing data sent is not exposed to us.
+ An **open-source server** that serves models without any exposure to us as the server is hardened and removed potential leakage channels from network to logs, and provides cryptographic proof those privacy controls are indeed in place using TPMs.

The server combines a hardened AI server with attested TLS using [TPMs](./docs/docs/concepts/TPMs.md).

The client performs two main tasks:

+ **Verifying that the server it communicates with is the expected hardened AI server** using attestation.
+ **Securely sending data** to be analyzed by a remote AI model using attested TLS to ensure data is not exposed.

The server has two main tasks:

+ It **loads a hardened AI server** which is inspected to ensure no data is exposed to the outside.
+ It **serves models using the hardened AI server that can be remotely verified** using attestation.

### Trust model

On this page, we will explain more precisely what components/parties have to be trusted when using BlindLlama.

To understand better which components and parties are trusted with BlindLlama, let’s start by examining what is trusted with regular AI services.

To do so, we will use the concept of a [Trusted Computing Base (TCB)](./docs/docs/concepts/TCB.md), which refers to the set of all hardware, firmware, and software components that are critical to a system's security.

#### Trusted Computing Base with regular AI providers

We can imagine that an AI provider serves AI APIs to their users using a Cloud infrastructure. Then the parties to be trusted are:

+ **The AI provider**: they provide the software application that is in charge of applying AI models to users’ data.

+ **The Cloud provider**: they provide the infrastructure, Hypervisor, VMs, OS, to the AI provider.

+ **The hardware providers**: they provide the lowest physical components, CPU, GPU, TPMs, etc. to the Cloud provider who then manages those to resell infrastructure to the AI providers. 

The higher the party in the stack, the closer they are to the data, and the more they are in a position to expose data.

In most scenarios today, there is often blind trust in the AI provider, aka we send data to them without any technical guarantees that they will do what they said they would do. For instance, the AI provider could say they just do inference on data, while they could actually train models on users’ data.

For privacy-demanding users that require more technical guarantees, they often choose not to send data to AI providers as they cannot trust them with their confidential data.

#### Trusted parties with BlindLlama

With BlindLlama, we remove the AI provider from the list of trusted parties. When models are served with BlindLlama, users' data cannot be seen by the AI provider because we use a Zero-trust AI infrastructure that removes the service/AI provider from the trust base. We can prove such controls are in place using [TPM-based attestation](./docs/docs/concepts/TPMs.md).

![trust-model-dark](./docs/assets/trust-model-dark.png)

## 👩🏻‍💻 Use cases

BlindLlama is meant to **help developers working with sensitive data to easily get started with LLMs** by using **managed AI APIs** that abstract the hardware and software complexity of model deployment while ensuring their data remains unexposed.

Several scenarios can be answered by using BlindLlama, such as:

+ Benchmarking the best open-source LLMs against one’s private data to find out which one is the most relevant without having to do any provisioning
+ Structuring medical documents
+ Analysis or auto-completion of a confidential code base

### ✅ When should you use BlindLlama?

+ You want to get started with LLMs that are complex to deploy, such as Llama 2 70B
+ You don’t want to manage that infrastructure as it requires too much time, expertise and/or budget
+ You don’t want to expose your data to a third party AI provider that manages the infrastructure for you due to privacy/compliance issues

#### ❌ What is not covered by BlindLlama?

+ BlindLlama is simply a drop-in replacement to query a remotely hosted model instead of having to go through complex local deployment. We do not cover training from scratch, but we will cover fine-tuning soon.
+ BlindLlama allows you to quickly and securely leverage models which are open-source, such as Llama 2, StarCoder, etc. **Proprietary models from OpenAI, Anthropic, and Cohere are not supported** yet as we would require them to modify their backend to offer a Zero-trust AI infrastructure like ours.
+ **BlindLlama’s trust model implies some level of trust in Cloud providers and hardware providers** since we leverage secure hardware available and managed by Cloud providers (see our [trust model section](https://blindllama.readthedocs.io/en/latest/docs/getting-started/blindllama-101/) for more details).

BlindLlama virtually provides the same level of security, privacy, and control as solutions provided by Cloud providers like Azure OpenAI Services.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🚀 Getting started

- Check out our [Quick tour](https://blindllama.readthedocs.io/en/latest/docs/getting-started/quick-tour/), which will enable you to play with an example using the [Llama 2](https://huggingface.co/meta-llama/Llama-2-7b) model while ensuring your data remains private and without the hassle of provisioning!
- Find out more about [How we protect your data](https://blindllama.readthedocs.io/en/latest/docs/getting-started/how-we-protect-your-data/)
- Refer to our [Concepts](https://blindllama.readthedocs.io/en/latest/docs/getting-started/concepts/) guide for more information on key concepts
- Learn more about BlindLlama's design with our [BlindLlama 101](https://blindllama.readthedocs.io/en/latest/docs/getting-started/blindllama-101/) guide

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!--
## 📚 How is the documentation structured?
____________________________________________
<!--
- [Tutorials](./docs/tutorials/core/installation.md) take you by the hand to install and run BlindBox. We recommend you start with the **[Quick tour](./docs/getting-started/quick-tour.ipynb)** and then move on to the other tutorials!  

- [Concepts](./docs/concepts/nitro-enclaves.md) guides discuss key topics and concepts at a high level. They provide useful background information and explanations, especially on cybersecurity.

- [How-to guides](./docs/how-to-guides/deploy-API-server.md) are recipes. They guide you through the steps involved in addressing key problems and use cases. They are more advanced than tutorials and assume some knowledge of how BlindBox works.

- [API Reference](https://blindai.mithrilsecurity.io/en/latest/blindai/client.html) contains technical references for BlindAI’s API machinery. They describe how it works and how to use it but assume you have a good understanding of key concepts.

- [Security](./docs/security/remote_attestation/) guides contain technical information for security engineers. They explain the threat models and other cybersecurity topics required to audit BlindBox's security standards.

- [Advanced](./docs/how-to-guides/build-from-sources/client/) guides are destined to developers wanting to dive deep into BlindBox and eventually collaborate with us to the open-source code.

- [Past Projects](./docs/past-projects/blindai) informs you of our past audited project BlindAI, of which BlindBox is the evolution. 
-->

<!-- ## ❓ Why trust us?
___________________________

+ **Our core security features are open source.** We believe that transparency is the best way to ensure security and you can inspect the code yourself on our [GitHub page](https://github.com/mithril-security/blindbox).

+ **Our historical project [BlindAI](docs/past-projects/blindai.md) was successfully audited** by Quarkslab. Although both projects differ (BlindAI was meant for the confidential deployment of ONNX models inside Intel SGX enclaves), we want to highlight that we are serious about our security standards and know how to code secure remote attestation. -->

## 🎯 Vision and roadmap

**Planned new features**:

+ **Confidential GPUs** for additional shielding
+ **Sandboxes** for additional isolation
+ **Finetuning endpoints** for all our APIs
+ **More APIs** to cover a wider range of popular open-source models

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🦙 Who made BlindLlama? 
<a name="about-us"></a>

BlindLlama is developed by **Mithril Security**, a startup focused on **democratizing privacy-friendly AI using secure hardware solutions**. 

We have already had our first project, [BlindAI](https://github.com/mithril-security/blindai), an open-source Rust inference server that deploys ONNX models on Intel SGX secure enclaves, audited by [Quarkslab](https://www.quarkslab.com/).

BlindLlama builds on the foundations of BlindAI but provides much faster performance and focuses on serving managed models directly to developers instead of helping AI engineers to deploy models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📇 Contact

[![Contact us][contact]][contact-url]
[![Twitter][twitter]][website-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://github.com/alexandresanlim/Badges4-README.md-Profile#-blog- -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/mithril-security/aicert.svg?style=for-the-badge
[contributors-url]: https://github.com/mithril-security/aicert/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mithril-security/aicert.svg?style=for-the-badge
[forks-url]: https://github.com/mithril-security/blindbox/network/members
[stars-shield]: https://img.shields.io/github/stars/mithril-security/aicert.svg?style=for-the-badge
[stars-url]: https://github.com/mithril-security/blindbox/stargazers
[issues-shield]: https://img.shields.io/github/issues/mithril-security/aicert.svg?style=for-the-badge
<!-- [issues-url]: https://github.com/mithril-security/aicert/issues -->
[project-url]: https://github.com/mithril-security/aicert
[twitter-url]: https://twitter.com/MithrilSecurity
[contact-url]: https://www.mithrilsecurity.io/contact
[docs-shield]: https://img.shields.io/badge/Docs-000000?style=for-the-badge&colorB=555
[docs-url]: https://blindllama.readthedocs.io/en/latest/
[license-shield]: https://img.shields.io/github/license/mithril-security/aicert.svg?style=for-the-badge
[contact]: https://img.shields.io/badge/Contact_us-000000?style=for-the-badge&colorB=555
[project]: https://img.shields.io/badge/Project-000000?style=for-the-badge&colorB=555
[license-url]: https://github.com/mithril-security/aicert/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&colorB=555
[twitter]: https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white
[linkedin-url]: https://www.linkedin.com/company/mithril-security-company/
[website-url]: https://www.mithrilsecurity.io
[docs-url]: https://blindllama.readthedocs.io/en/latest/
[website-shield]: https://img.shields.io/badge/website-000000?style=for-the-badge&colorB=555
[blog-url]: https://blog.mithrilsecurity.io/
[blog-shield]: https://img.shields.io/badge/Blog-000?style=for-the-badge&logo=ghost&logoColor=yellow&colorB=555
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[Python-url]: https://www.python.org/
[Rust]: https://img.shields.io/badge/rust-FFD43B?style=for-the-badge&logo=rust&logoColor=black
[Rust-url]: https://www.rust-lang.org/fr
[Intel-SGX]: https://img.shields.io/badge/SGX-FFD43B?style=for-the-badge&logo=intel&logoColor=black
[Intel-sgx-url]: https://www.intel.fr/content/www/fr/fr/architecture-and-technology/software-guard-extensions.html
[Tract]: https://img.shields.io/badge/Tract-FFD43B?style=for-the-badge
<!-- [tract-url]: https://github.com/mithril-security/tract/tree/6e4620659837eebeaba40ab3eeda67d33a99c7cf -->
