Downloads
=========

.. _Downloads Required Technical:

Downloads required
------------------

🐧 On Debian and Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo apt install build-essential python3 python3-pip python3-venv
    sudo apt install curl apt-transport-https ca-certificates software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install docker-ce
    sudo usermod -aG docker $(whoami)

It is preferable to restart your machine after these downloads for them to take effect.

🎩 On Fedora
~~~~~~~~~~~~~

.. code-block:: bash

    sudo dnf install build-essential python3 python3-pip python3-venv
    sudo dnf install dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
    sudo dnf install docker-ce docker-ce-cli containerd.io
    sudo groupadd docker && sudo gpasswd -a ${USER} docker

It is preferable to restart your machine after these downloads for them to take effect.

.. _Downloads Python For Windows:

🏁 On Windows
~~~~~~~~~~~~~

Download and install the 3.12.4 version of Python from the official website :

`🔗 Download Python <https://www.python.org/>`_

Install the Windows library to launch Luna and reboot your machine :

`Install Windows library <https://learn.microsoft.com/fr-fr/cpp/windows/latest-supported-vc-redist?view=msvc-170>`_

.. _Downloads Required Technical To Launch From Code:

Downloads required to launch from code
--------------------------------------

🏁 On Windows
~~~~~~~~~~~~~

Follow this tutorial to install python on Windows : :ref:`How to install python<Downloads Python For Windows>`

🐧 On Debian and Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo apt install build-essential python3 python3-pip python3-venv
    sudo apt install gcc
    sudo apt install python3.12-dev
    sudo apt install portaudio19-dev

It is preferable to restart your machine after these downloads for them to take effect.

🎩 On Fedora
~~~~~~~~~~~~~

.. code-block:: bash

    sudo dnf install build-essential python3 python3-pip python3-venv
    sudo dnf install gcc
    sudo dnf install python3-devel
    sudo dnf install portaudio-devel

It is preferable to restart your machine after these downloads for them to take effect.