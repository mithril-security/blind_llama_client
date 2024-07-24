# Quick Tour
## Introduction 
________________________________________________________
<div class="alert"><span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>
⚠️ This quick tour uses a <b>prototype</b> version of BlindLlama which enables you to test our solution and learn more about it.<br><br>
It does not yet have the full security features.
Do not test it with confidential information... yet!
</div>

BlindLlama-v2 is a **technical framework** for serving Kubernetes-based applications on verifiable and isolated environments called **enclaves** and deploying them on Cloud VMs equipped with **GPUs and vTPMs**.

By deploying models like Llama 2 with BlindLlama-v2, end-users can consume AI models **with guarantees the admins of the AI infrastructure cannot see users' data** as they can verify data is only processed in verifiable environments isolated (leveraging hypervisor isolation) and data will not leave (network isolation).

> Llama2 is is a text-generation LLM (large language model) that can be queried in a similar way to OpenAI's ChatGPT.

For developers wishing to deploy their applications with BlindLlama-v2, the process is done in 4 steps:

- Prepare the image
  - Model
  - OS
  - Network configuration
- Generate measurements
- Deploy on Azure
- Integrate the secure client-side SDK

More information about the security properties, the architecture, and the workflow can be found in our [Whitepaper](https://github.com/mithril-security/blind_llama_client/blob/main/docs/docs/whitepaper/blind_llama_whitepaper.pdf).

In this quick tour, we will show how one can package a Kubernetes application to serve either Llama 2 7b or GPT 2 using TensorRT, prepare measurements to prove the model is served in an enclave, deploy it on Azure VMs with A100 and vTPMs, and finally consume the AI model with confidentiality.

## 🛠️ Prerequisites

To run this example, you will need to use a VM with a GPU such as Standard_NC24ads_A100_v4. To run a larger model than the Llama 7B, you may need to use larger machines with more memory and more GPUs, such as the Standard_NC48ads_A100_v4 or the Standard_NC96ads_A100_v4.

The code requires `python 3.11` or later. You will also need to install `git lfs`, which can be done with:

```bash
$ git clone git@github.com:mithril-security/blindllama-v2.git
$ apt-get update && apt-get install git-lfs pesign -y --no-install-recommends
$ git lfs install

$ git submodule update --init --recursive blindllama-v2/
```

## 🖼️ Preparing the image

BlindLlama-v2 serves Kubernetes-based images inside enclaves and, therefore, requires developers to package their applications in the appropriate manner.

### A - Model weights
The model weights have to be prepared to be used by TensorRT. Triton with TensorRT requires the creation of a model engine that has the weights embedded in it. The following script will generate a model engine for Llama 2 7b.

`./launch_container_create_model_engine.sh "Llama-2-7b-hf"`

To create a model engine for GPT2-medium, use:

`./launch_container_create_model_engine.sh "gpt2-medium"`
> The model engines are specific to the GPU they are generated on. If you use an A100 GPU to create the model engine, you must run the BlindLlama-v2 VM on a machine with an A100 GPU.

**By default, the engine generated uses 1 engine. To create the model engine according to your specifications, you may change the create_engine.sh script present at tritonRT/create_engine.sh before creating the model engine.**

```bash
$ python /tensorrtllm_backend/tensorrt_llm/examples/llama/build.py --model_dir /$1/ \
                --dtype bfloat16 \
                --use_gpt_attention_plugin bfloat16 \
                --use_inflight_batching \
                --paged_kv_cache \
                --remove_input_padding \
                --use_gemm_plugin bfloat16 \
                --output_dir /engines/1-gpu/ \
                --world_size 1
```

### B - Production mode:

The Mithril OS, which is a minimal OS designed to be easily verifiable and provide measurements, has to be integrated into the final image. This will create an OS image in production mode with no means of access to the image. The only point of access is the ingress controller and the endpoints it serves. There is no shell access, SSH, etc.

`earthly -i -P +mithril-os --OS_CONFIG='config.yaml'`

### C - Application disk

The application disk is a data disk containing the required container images, such as the attestation generator, the triton server, and the attestation server.
This command will create an application disk with the Llama 2 7B model engine (generated earlier) included in it.

`earthly -i -P +blindllamav2-appdisk --MODEL="Llama-2-7b-hf"`

To create an application disk with GPT2-medium use:

`earthly -i -P +blindllamav2-appdisk --MODEL="gpt2-medium"`

The application disk can be measured and a root hash generated, attesting to every file in the disk. Any changes to the disk will alter the root hash and, therefore, be detected.

### D - Network policy

While the network policy will be part of the disk, it is interesting to explore it further, as it is important for security and privacy.

The network policy that will be used will be included in the final measurement of the application disk. For instance, we will use the following one to allow data to be loaded inside the enclave, but nothing will leave it except the output of the AI model that will be sent back to the requester.

The network policy file can be found in the annex.

## 🔍 Go Furthur

For more information, visit our [GitHub repository](https://github.com/mithril-security/blindllama-v2). There, you can:


- [Generate measurements of the disks](https://github.com/mithril-security/blindllama-v2?tab=readme-ov-file#2---generating-measurements) used by the client to verify the server
- [Deploy the image on the appropriate Azure VM](https://github.com/mithril-security/blindllama-v2?tab=readme-ov-file#3---deploying-it-on-azure) once the disks are created
- [Consume the model securely](https://github.com/mithril-security/blindllama-v2?tab=readme-ov-file#4---confidential-consumption-with-attested-tls) through our Python Client SDK, which performs attestation by verifying the measurements of the enclave, ensuring they come from genuine vTPMs and that the measurements match the expected secure version of our code

## 🔒 Security
________________________________________________________

BlindLlama is doing a lot under the hood to make sure user data remains confidential!

When you connect to the BlindLlama server, the client will:
- Check that it is talking to an authentic BlindLlama server, through [attested TLS](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/attested-tls/)
- Check that the server is [serving the expected code](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/TPMs/) and is deployed withing [a hardened Confidential & transparent environment](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/hardened-systems/)

If either of these checks fail, you will see an error and will be unable to connect to the server!

You can check out our overview of how we make our solution confidential [in the next section](https://blindllama.mithrilsecurity.io/en/latest/docs/getting-started/how-we-achieve-zero-trust/) and learn more about the underlining key concepts in our [concept guide](https://blindllama.mithrilsecurity.io/en/latest/docs/concepts/overview/).