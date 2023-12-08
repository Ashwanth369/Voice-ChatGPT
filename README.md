# **Voice ChatGPT**

### **Source Files**
1. main.py: <br>
    This is the main file that runs on the android device. It has the code for the UI, invocation to TTS and STT files for the functionalities
2. requirements.txt: <br>
    This files contains the list of modules you need to download for running the application
3. speechToText.py: <br>
    It contains the code for the Speech-to-Text integration
4. textToSpeech.py: <br>
    It contains the code for the Text-to-Speech integration
5. client.py: <br>
    This file is used to communicate with the server via socket programming. Its sends the converted input speech from the user in the form of chunks 
6. server.py: <br>
    It contains the code to run as the server processing all the queries it receives from the client. It receives the response from the Open AI API and sends it back to the client at text in the form of chunks
7. cgpt.py: <br>
    This file contains the ChatGPT integration code and also the the Open AI secret API key used to authenticate the API access for the application

### **User Manual:**

#### **Server**
1. The server.py and cgpt.py files are uploaded in Amazon AWS EC2 instance. This is the Public IPv4 DNS name of the EC2 instance : ec2-3-17-4-67.us-east-2.compute.amazonaws.com
2. The server is already up and running and we also have the Open AI secret API key in the cgpt.py file. You don't need to start any server or create any new Open AI account.

#### **App**
1. Download the code from github <br>
  `$ git clone https://github.com/Ashwanth369/Voice-ChatGPT.git`
2. Open the folder <br>
  `$ cd Voice-ChatGPT`
3. Open a terminal and run the main.py file using this command <br>
  `$ python3 main.py`
4. The application window opens up. Hit the microphone button and give the input speech.
5. Hit the Stop button and wait for the output response speech.
