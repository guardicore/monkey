FROM ubuntu:jammy
# Install SSH
RUN apt-get update && apt-get install -y openssh-server \
    && apt-get remove -y sshguard \
    && rm -rf /var/lib/apt/lists/*
# Enable password authentication
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
# Add user
RUN useradd -m -s /bin/bash user -p "$(openssl passwd -1 password)" \
    && mkdir -p /home/user/.ssh \
    && chown user /home/user/.ssh
RUN service ssh start
EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]
