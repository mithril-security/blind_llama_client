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
    <li><a href="#-advanced-security">Advanced security</a></li>
    <li><a href="#-vision-and-roadmap">Vision and roadmap</a></li>
    <li><a href="#-about-us">About us</a></li>
    <li><a href="#-contributing">Contributing</a></li>
    <li><a href="#-get-in-touch">Contact</a></li>
  </ol>
</details>

## 📜 About the project

### Introduction

🛠️ **BlindLlama** makes it easy to use open-source LLMs by using **Confidential & transparent AI APIs** that abstract all the complexity of model deployment while ensuring **users’ data is never exposed** to us thanks to end-to-end protection with **secure hardware**.

🔐 To provide guarantees to developers that data sent to our managed infrastructure is not exposed, we have developed a **Confidential & transparent architecture to serve AI models**.

> We currently serve [Llama2](https://ai.meta.com/llama/) but will be making more open-source models available in the near future!

Our backend has two key properties:

+ **Confidentiality**: Your data is **never accessible to us**. We serve AI models inside **hardened environments** that do not expose data even to our admins. All points of access, such as SSH, logs, networks, etc., are blocked to ensure the isolation of data.

+ **Transparency**: We provide you with verifiable **cryptographic proof** that these controls are in place, thanks to the use of [Trusted Platform Modules (TPMs)](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/TPMs/).

> **Warning**
> BlindLlama is still **under development** and does have the full security features.
>
> Do not test our APIs with confidential information... yet!
>
> You can follow our progress towards the next beta and 1.0 versions of BlindLLama on our [roadmap](https://mithril-security.notion.site/BlindLlama-roadmap-d55883a04be446e49e01ee884c203c26).


We welcome contributions to our project from the community! Don't hesitate to [raise issues](https://github.com/mithril-security/blind_llama/issues) on GitHub, <a href="#-contact">reach out to us</a> or see our guide on how to audit BlindLlama (**coming soon!**).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 🚀 Getting started

- Check out our [Quick tour](https://blindllama.mithrilsecurity.io/en/latest/docs/getting-started/quick-tour/), which will enable you to play with an example using the [Llama 2](https://huggingface.co/meta-llama/Llama-2-7b) model while ensuring your data remains private and without the hassle of provisioning!
- Find out more about [How we protect your data](https://blindllama.mithrilsecurity.io/en/latest/docs/getting-started/how-we-achieve-zero-trust/)
- Refer to our [Concepts](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/overview/) guide for more information on key concepts
- Learn more about BlindLlama's design [here](https://blindllama.mithrilsecurity.io/en/latest/docs/blind_llama/architecture/) guide

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Architecture

BlindLlama is composed of two main parts:

+ An **open-source client-side Python SDK** that verifies the remote AI models we serve are indeed guaranteeing data sent is not exposed to us.
+ An **open-source server** that serves models without exposing any user data to the AI provider (Mithril security). This is achieved by hardening the server components and removing any potential leakage channels from network to logs. We provide cryptographic proof those privacy controls are indeed in place using [TPMs](./docs/docs/concepts/TPMs.md).

The client performs two main tasks:

+ **Verifying that the server it communicates with is the expected hardened AI server** using attestation.
+ **Securely sending data** to be analyzed by a remote AI model using attested TLS to ensure data is not exposed.

The server has two main tasks:

+ It **loads a hardened AI server** which is inspected to ensure no data is exposed to the outside.
+ It **serves models using the hardened AI server that can be remotely verified** using attestation.

> Note that there are three key components behind what we call the "server" here. You can find out more about each of these components and how they interact [in our docs](https://blindllama.mithrilsecurity.io/en/latest/docs/blind_llama/architecture/).

### Trust model

On this page, we will explain more precisely what components/parties have to be trusted when using BlindLlama.

To understand better which components and parties are trusted with BlindLlama, let’s start by examining what is trusted with regular AI services.

To do so, we will use the concept of a [Trusted Computing Base (TCB)](./docs/docs/concepts/TCB.md), which refers to the set of all hardware, firmware, and software components that are critical to a system's security.

#### Trusted Computing Base with regular AI providers

In the case of an AI provider serving an AI API to end users on a Cloud infrastructure, the parties to be trusted are:

+ **The AI provider**: they provide the software application that is in charge of applying AI models to users’ data. Examples of AI providers in the industry include Hugging Face, OpenAI, Cohere, etc.

+ **The Cloud provider**: they provide the infrastructure, Hypervisor, VMs and OS, to the AI provider. Examples of Cloud providers in the industry include Azure, GCP, AWS, etc. 

+ **The hardware providers**: they provide the physical components, CPU, GPU, TPMs, etc. to the Cloud provider. Examples of hardware providers in the industry include Intel, AMD, Nvidia, etc. 

The higher the party in the stack, the closer they are to the data. Thus, the AI provider if malicious or negligent represents the biggest security risk for the user of the API.

In most scenarios today, there is often blind trust in the AI provider, aka **we send data to them without any technical guarantees regarding how they will handle or use our data**. For instance, the AI provider could say they just do inference on data, while they could actually train models on users’ data. And even if most AI providers are honest, there is no way to know if their security practices are strong enough to protect your data.

For privacy-demanding users that require more technical guarantees, they often choose simply not to use AI APIs as they cannot trust AI providers with their confidential data.

## Trusted parties with BlindLlama

With BlindLlama, we remove the AI provider (Mithril Security) from the list of trusted parties. When models are served with BlindLlama, our admins cannot see user data because we use a Confidential & transparent AI infrastructure, removing the need for users to blindly trust us. 
	
We can prove such controls are in place using [TPM-based attestation](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/TPMs/).

![trust-model-dark](./docs/assets/trust-model-dark.png#gh-dark-mode-only)
![trust-model-light](./docs/assets/trust-model-light.png#gh-light-mode-only)

> See our section on BlindLlama's [Trusted Computing Base (TCB)](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/TCB/) to see which components we trust or verify in our stack!

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
+ BlindLlama allows you to quickly and securely leverage models which are open-source, such as Llama 2, StarCoder, etc. **Proprietary models from OpenAI, Anthropic, and Cohere are not supported** yet as we would require them to modify their backend to offer a Confidential & transparent AI infrastructure like ours.
+ **BlindLlama’s trust model implies some level of trust in Cloud providers and hardware providers** since we leverage secure hardware available and managed by Cloud providers (see our [trust model section](https://blindllama.mithrilsecurity.io/en/latest/docs/blind_llama/trust-model/) for more details).

BlindLlama virtually provides the same level of security, privacy, and control as solutions provided by Cloud providers like Azure OpenAI Services.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!--
## 📚 How is the documentation structured?
____________________________________________
<!--
- [Tutorials](./docs/tutorials/core/installation.md) take you by the hand to install and run BlindBox. We recommend you start with the **[Quick tour](./docs/getting-started/quick-tour.md)** and then move on to the other tutorials!  

- [Concepts](./docs/concepts/nitro-enclaves.md) guides discuss key topics and concepts at a high level. They provide useful background information and explanations, especially on cybersecurity.

- [How-to guides](./docs/how-to-guides/deploy-API-server.md) are recipes. They guide you through the steps involved in addressing key problems and use cases. They are more advanced than tutorials and assume some knowledge of how BlindBox works.

- [API Reference](https://blindai.mithrilsecurity.io/en/latest/blindai/client.html) contains technical references for BlindAI’s API machinery. They describe how it works and how to use it but assume you have a good understanding of key concepts.

- [Security](./docs/security/remote_attestation/) guides contain technical information for security engineers. They explain the threat models and other cybersecurity topics required to audit BlindBox's security standards.

- [Advanced](./docs/how-to-guides/build-from-sources/client/) guides are destined to developers wanting to dive deep into BlindBox and eventually collaborate with us to the open-source code.

- [Past Projects](./docs/past-projects/blindai) informs you of our past audited project BlindAI, of which BlindBox is the evolution. 
-->

## 📚 Advanced security

We created the BlindLlama whitepaper to cover the architecture and security features behind BlindLLama in greater detail.

The whitepaper is intended for an audience with security expertise.

You can read or download the whitepaper [here](https://github.com/mithril-security/blind_llama/tree/main/docs/docs/whitepaper/blind_llama_whitepaper.pdf)!

## 🎯 Roadmap

There are three key milestones planned for the BlindLlama project.

### BlindLlama Alpha launch (not attestable): 

The alpha launch of BlindLlama provides a regular API for the Llama2-70b model which you can query with our python SDK. 

Users can test out and query our API **but should not yet send any confidential data to the API** as it is does not yet have full implementation of security features.

The server-side code already includes the backbones for our attestation feature (which will enable us to be able to prove the server is deploying the expected code to end users) but this feature will be fully launched in the following beta phase.

> Expected launch date: week ending 08/09/2023

### BlindLlama Beta launch (with attestation):

The beta version adds the full implementation of TPM-based attestation, meaning our APIs can be fully verified remotely. This version will not yet have full hardening of server-side environment or audit and thus is not yet recommended in production!

> Provisional launch date: week ending 06/10/2023

### BlindLlama 1.0 launch (audit-ready):

A fully-secure version of BlindLlama ready for audit, with a fully hardened server environment.

> Provisional launch date: week ending 08/12/2023

You can check out more details about these stages and our progress to achieveing these milestones on our [official roadmap](https://mithril-security.notion.site/BlindLlama-roadmap-d55883a04be446e49e01ee884c203c26).


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 🦙 Who made BlindLlama? 
<a name="about-us"></a>

BlindLlama is developed by **Mithril Security**, a startup focused on **democratizing privacy-friendly AI using secure hardware solutions**. 

We have already had our first project, [BlindAI](https://github.com/mithril-security/blindai), an open-source Rust inference server that deploys ONNX models on Intel SGX secure enclaves, audited by [Quarkslab](https://www.quarkslab.com/).

BlindLlama builds on the foundations of BlindAI but provides much faster performance and focuses on serving managed models directly to developers instead of helping AI engineers to deploy models.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🤝 Contributing

Here’s how you can help us make AI confidential:

### 🛠️ Code contribution

You can contribute our code by forking our project on [GitHub](https://github.com/mithril-security/blind_llama) and creating a new pull request. Make sure to detail the modifications you are suggesting in your pull request description.

### 🌎 Spread the word

Share our project on social media!

[![share-on-twitter][twitter]][twitter-share]
[![share-on-fb][fb-shield]][facebook-share]
[![share-on-reddit][reddit-shield]][reddit-share]
[![share-on-linkedin][linkedin-shield]][linkedin-share]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📇 Get in touch

We would love to hear your feedback or suggestions, here are the ways you can reach us:
  - Found a bug? [Open an issue!](https://github.com/mithril-security/blind_llama/issues)
  - Got a suggestion? [Join our Discord community and let us know!](https://discord.com/invite/TxEHagpWd4)
  - Set up [a one-on-one meeting](https://www.mithrilsecurity.io/contact) with a member of our team

Want to hear more about our work on privacy in the field AI?
- Check out our [blog](https://blog.mithrilsecurity.io/)
- Subscribe to our newsletter [here](https://blog.mithrilsecurity.io/)

Thank you for your support!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[project-url]: https://github.com/mithril-security/aicert
[twitter-url]: https://twitter.com/MithrilSecurity
[contact-url]: https://www.mithrilsecurity.io/contact
[docs-shield]: https://img.shields.io/badge/Docs-000000?style=for-the-badge&colorB=555
[docs-url]: https://blindllama.mithrilsecurity.io/en/latest/
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&colorB=555
[reddit-shield]: https://img.shields.io/badge/reddit-0077B5?style=for-the-badge&logo=reddit&logoColor=white&colorB=FF4500
[twitter]: https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white
[fb-shield]: https://img.shields.io/badge/Facebook-0077B5?style=for-the-badge&logo=facebook&logoColor=white&colorB=3b5998
[license-shield]: https://img.shields.io/github/license/mithril-security/aicert.svg?style=for-the-badge
[contact]: https://img.shields.io/badge/Contact_us-000000?style=for-the-badge&colorB=555
[project]: https://img.shields.io/badge/Project-000000?style=for-the-badge&colorB=555
[license-url]: https://github.com/mithril-security/aicert/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&colorB=555
[twitter]: https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white
[linkedin-url]: https://linkedin.com/company/mithril-security-company/
[website-url]: https://www.mithrilsecurity.io
[docs-url]: https://blindllama.mithrilsecurity.io/en/latest/
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
[facebook-share]: https://www.facebook.com/sharer/sharer.php?u=https%3A//github.com/mithril-security/blind_llama
[twitter-share]: https://twitter.com/intent/tweet?url=https://github.com/mithril-security/blind_llama&text=Check%20out%20this%20open-source%20project%20that%20aims%20to%20make%20AI%20private
[linkedin-share]: https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/mithril-security/blind_llama
[reddit-share]: https://www.reddit.com/submit?url=github.com%2Fmithril-security%2Fblind_llama&title=Private%20in-browser%20Conversational%20AI%20with%20BlindLlama