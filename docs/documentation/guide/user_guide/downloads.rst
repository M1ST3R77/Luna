Downloads
=========

.. _Downloads Required User:

Downloads required
------------------

🐧 On Debian and Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
    
    sudo apt install build-essential python3 python3-pip python3-venv

🎩 On Fedora
~~~~~~~~~~~~~~

.. code-block:: bash

    sudo dnf install build-essential python3 python3-pip python3-venv

🏁 On Windows
~~~~~~~~~~~~~

Download and install the 3.12.4 version of Python from the official website :

`🔗 Download Python <https://www.python.org/>`_

Install the Windows library to launch Luna and reboot your machine :

`Install Windows library <https://learn.microsoft.com/fr-fr/cpp/windows/latest-supported-vc-redist?view=msvc-170>`_

.. _Voice Installation:

Voice installation
------------------

This section explains how to add additional voices to Luna on Windows and Linux systems.

🏁 Windows
~~~~~~~~~~

1. **Access voice settings** :

    - Open Windows **Settings**.
    - Click on **Time and Language**.
    - Select **Speech** from the left-hand menu.

2. **Add Microsoft voices**:

    - In the **Manage voices** section, you can add new voices.
    - Install **Microsoft Hortense** and **Microsoft Paul**.

If this didn't work while using audio, I'll redirect you to this tutorial: `How to add more speakers and their voices in pyttsx3 offline text to speech <https://puneet166.medium.com/how-to-added-more-speakers-and-voices-in-pyttsx3-offline-text-to-speech-812c83d14c13>`_ 

🐧 Linux (Ubuntu/Debian)
~~~~~~~~~~~~~~~~~~~~~~~~

Use the following commands to install MBROLA and related voices :

.. code-block:: bash

    sudo apt-get install mbrola mbrola-{name_file}

Replace `{name_file}` with the name of the voice file you wish to install.

Here is a list of all the voices: `MBROLA-voices <https://github.com/numediart/MBROLA-voices>`_

🎩 Linux (Fedora 40)
~~~~~~~~~~~~~~~~~~~~~

1. **Install espeak-ng** :

.. code-block:: bash

    sudo dnf install espeak-ng

2. **Install MBROLA** :

    - Download the MBROLA RPM package :

        .. code-block:: bash
            
            wget https://raw.githubusercontent.com/rpmsphere/x86_64/master/m/mbrola-3.3-1.x86_64.rpm -O mbrola-3.3-1.x86_64.rpm
    
    - Install MBROLA with dependencies :

        .. code-block:: bash

            sudo dnf install glibc
            sudo dnf install ./mbrola-3.3-1.x86_64.rpm

3. **Create MBROLA directories** :

.. code-block:: bash
    
    sudo mkdir -p /usr/share/mbrola
    sudo mkdir -p /usr/share/mbrola/en3
    sudo mkdir -p /usr/share/mbrola/en4

4. **Download and move voice files** :

    - Download the `fr3` and `fr4` voice files from the GitHub repository:

        .. code-block:: bash
        
            wget https://raw.githubusercontent.com/numediart/MBROLA-voices/blob/master/data/fr3/fr3
            wget https://raw.githubusercontent.com/numediart/MBROLA-voices/blob/master/data/fr4/fr4
    
    - Move the files to the MBROLA directories:

        .. code-block:: bash
            
            sudo mv fr3 /usr/share/mbrola/fr3
            sudo mv fr4 /usr/share/mbrola/fr4