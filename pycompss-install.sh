# require root user or sudo
if ! [ $(id -u) = 0 ]; then
   echo "The script needs to be run as root."
   exit 1
fi

# installs software dependencies through APT package manager
apt update -y
apt upgrade -y
apt install -y software-properties-common wget
apt install -y zip openjdk-8-jdk graphviz xdg-utils libtool automake build-essential python python-dev libpython2.7 libboost-serialization-dev libboost-iostreams-dev libxml2 libxml2-dev csh gfortran libgmp3-dev flex bison texinfo libpapi-dev
apt install -y python3 python3-dev python3-pip

# downloads and installs gradle
wget https://services.gradle.org/distributions/gradle-5.4.1-bin.zip -O /opt/gradle-5.4.1-bin.zip
unzip /opt/gradle-5.4.1-bin.zip -d /opt

# exports environment variables
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/' >> ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
echo 'export GRADLE_HOME=/opt/gradle-5.4.1' >> ~/.bashrc
export GRADLE_HOME=/opt/gradle-5.4.1
echo 'export PATH=/opt/gradle-5.4.1/bin:$PATH' >> ~/.bashrc
export PATH=/opt/gradle-5.4.1/bin:$PATH

# upgrade pip and setuptools
python3 -m pip install --upgrade pip setuptools

# installs library dependencies for PyCOMPSs
python3 -m pip install dill guppy3

# installs the latest version of PyCOMPSs
python3 -m pip install pycompss==3.1 -v


