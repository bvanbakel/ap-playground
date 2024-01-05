# Build Base Image
ARG PYTHON_VARIANT=3.10.7

FROM --platform=linux/amd64 python:${PYTHON_VARIANT} as ap_playground_base

RUN apt-get update

# Install Azure CLI
RUN curl -L https://aka.ms/InstallAzureCLIDeb | bash

# Install Terraform
RUN apt-get install -y gnupg software-properties-common

RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list

RUN apt update

RUN apt-get install terraform

# Install NodeJs
RUN curl -fsSL https://deb.nodesource.com/setup_21.x | bash - && \
    apt-get install -y nodejs

# Install CDKTF
RUN npm install --global cdktf-cli@latest

# Install Requirements
COPY ./requirements.txt /usr/local/

RUN pip install --retries 5 -r /usr/local/requirements.txt

# Install CDKTF - Azure Provider
RUN pipenv install cdktf-cdktf-provider-azurerm

CMD ["bash"]