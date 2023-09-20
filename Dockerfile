FROM ubuntu:20.04

USER root
WORKDIR /root

# install utility software packages
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y software-properties-common&& rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y inetutils-ping net-tools wget && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y htop screen zip nano && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
	
# install and configure git
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y git && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
RUN DEBIAN_FRONTEND=noninteractive git config --global commit.gpgsign false

# configure ssh daemon
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y openssh-server && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
RUN if ! [ -d /var/run/sshd ]; then mkdir /var/run/sshd; fi
RUN echo 'root:password!!' | chpasswd
RUN sed -i 's/^[# ]*PermitRootLogin .*$/PermitRootLogin yes/g' /etc/ssh/sshd_config
RUN sed -i 's/^[# ]*PubkeyAuthentication .*$/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
RUN service ssh start

# generate ssh keys for all instances of this image (useful for building SSH clusters on docker compose)
RUN ssh-keygen -b 4096 -f /root/.ssh/id_rsa -N '' << y
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys

# download and install Gradle
RUN wget https://services.gradle.org/distributions/gradle-5.4.1-bin.zip -O /opt/gradle-5.4.1-bin.zip
RUN unzip /opt/gradle-5.4.1-bin.zip -d /opt
ENV GRADLE_HOME=/opt/gradle-5.4.1
RUN echo 'export GRADLE_HOME=/opt/gradle-5.4.1' >> ~/.bashrc
ENV PATH=/opt/gradle-5.4.1/bin:$PATH
RUN echo 'export PATH=/opt/gradle-5.4.1/bin:$PATH' >> ~/.bashrc

# install Open JDK 8
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y openjdk-8-jdk && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/' >> ~/.bashrc

# install Python 3
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y python3 python3-pip python3-dev && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# install PyCOMPSs
RUN DEBIAN_FRONTEND=noninteractive apt update -y && apt install -y graphviz xdg-utils libtool automake build-essential \
	python python-dev libpython2.7 libboost-serialization-dev libboost-iostreams-dev libxml2 libxml2-dev csh gfortran \
	libgmp3-dev flex bison texinfo libpapi-dev && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip setuptools
RUN python3 -m pip install dill guppy3
RUN python3 -m pip install "pycompss==3.1" -v
RUN echo ". /etc/profile.d/compss.sh" >> /root/.bashrc

# install apps requirements
COPY ./requirements-apps.txt /requirements-apps.txt
RUN python3 -m pip install -r "/requirements-apps.txt"

# install test requirements
COPY ./requirements-test.txt /requirements-test.txt
RUN python3 -m pip install -r "/requirements-test.txt"

# install ParSoDA sources and pip package
COPY ./ /parsoda/

# setup entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
CMD ["/docker-entrypoint.sh"]

# expose container resources
EXPOSE 22
VOLUME ["/parsoda"]
WORKDIR /parsoda
