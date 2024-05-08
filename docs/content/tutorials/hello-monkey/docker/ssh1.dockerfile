FROM ubuntu:jammy
# Install SSH
RUN apt-get update && apt-get install -y openssh-server \
    && apt-get remove -y sshguard \
    && rm -rf /var/lib/apt/lists/*
# Enable password authentication
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
# # Remove sshguard
# RUN apt-get remove -y sshguard
# Add user
RUN useradd -m -s /bin/bash user -p j688yq\pB{5=
USER user
