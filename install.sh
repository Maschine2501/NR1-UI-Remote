#!/bin/bash
set +e #
sudo dpkg-reconfigure tzdata #
sudo apt-get update #
sudo apt-get upgrade #
sudo apt-get install -y build-essential libffi-dev libc6-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev #
cd #
sudo chmod +x /home/pi/NR1-UI-Remote/PreConfiguration.sh #
#sudo cp /home/pi/NR1-UI-Remote/ConfigurationFiles/config.txt /boot/ #
echo "dtparam=spi=on" >> /boot/userconfig.txt #
echo "dtparam=i2c=on" >> /boot/userconfig.txt #
echo "Installing OpenSSL 1.1.1b" #
mkdir /home/pi/src #
cd /home/pi/src && mkdir openssl && cd openssl #
wget https://www.openssl.org/source/openssl-1.1.1b.tar.gz #
tar xvf openssl-1.1.1b.tar.gz && cd openssl-1.1.1b #
./config --prefix=/home/pi/src/openssl-1.1.1b --openssldir=/home/pi/src/openssl-1.1.1b && make && sudo make install #
cd #
sudo cp /home/pi/NR1-UI-Remote/ConfigurationFiles/ldconf/libc.conf /etc/ld.so.conf.d #
sudo ldconfig #
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/pi/src/openssl-1.1.1b/lib #
echo "Installing 3.8.5 and related modules" #
cd /home/pi/src && mkdir python && cd python #
wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tar.xz #
tar xf Python-3.8.5.tar.xz #
cd Python-3.8.5 #
sudo cp /home/pi/NR1-UI-Remote/ConfigurationFiles/python/Setup /home/pi/src/python/Python-3.8.5/Modules #
./configure --prefix=/home/pi/src/Python-3.8.5 --with-openssl=/home/pi/src/openssl-1.1.1b && make && sudo make altinstall #
export PATH=/home/pi/src/Python-3.8.5/bin:$PATH #
export LD_LIBRARY_PATh=/home/pi/src/Python-3.8.5/bin #
sudo /home/pi/src/Python-3.8.5/bin/pip3.8 install -U pip #
sudo /home/pi/src/Python-3.8.5/bin/pip3.8 install -U setuptools #
sudo apt-get install -y python3-dev python3-setuptools python3-pip libfreetype6-dev libjpeg-dev python-rpi.gpio libcurl4-openssl-dev libssl-dev git-core autoconf make libtool libfftw3-dev libasound2-dev libncursesw5-dev libpulse-dev libtool #
sudo /home/pi/src/Python-3.8.5/bin/pip3.8 install --upgrade setuptools pip wheel #
sudo /home/pi/src/Python-3.8.5/bin/pip3.8 install --upgrade luma.oled #
sudo /home/pi/src/Python-3.8.5/bin/pip3.8 install psutil socketIO-client pycurl readchar requests #
echo "all Python related modules arre installed..." #
echo "Installing NR1-UI..."  #
chmod +x /home/pi/NR1-UI-Remote/nr1ui.py #
sudo cp /home/pi/NR1-UI-Remote/service-files/nr1ui.service /lib/systemd/system/ #
sudo systemctl daemon-reload #
sudo systemctl enable nr1ui.service #
echo "_________________________________________________________________ " #
echo " " #
echo " " #
echo "_______________________________" #
echo "Should the Display be rotated?" #
echo "_______________________________"
echo " " #
echo "_____________________ " #
echo "Valid selections are:" #
echo "1 -> Display not rotated" #
echo "2 -> Display rotated 180 degrees " #
echo "---> " #
getDisplayRotation() { #
  read -p "Enter your decision: " RotationNumber #
  case "$RotationNumber" in #
    1) #    
      sed -i 's/\(oledrotation = \)\(.*\)/\10/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      echo " " #
      echo "Set Display-Rotation to zero Rotation." #
      return 0 #
      ;; #
    2) #
      sed -i 's/\(oledrotation = \)\(.*\)/\12/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      echo "Set Display-Rotation to 180 degrees Rotation" #
      return 0 #
      ;; #         
    *) #
      printf %s\\n "Please enter '1' or '2'" #
      return 1 #
      ;; #
  esac #
} #
until getDisplayRotation; do : ; done #
echo "_________________________________________________________________ " #
echo " " #
echo " " #
echo "__________________________________________________" #
echo "Please select your Button- / Rotary- configuration" #
echo "__________________________________________________ " #
echo " " #
echo "*standard*-configuration means a conection like this: " #
echo "https://raw.githubusercontent.com/Maschine2501/NR1-UI/master/wiki/wiring/Wiring.jpg" #
echo " " #
echo "_____________________" #
echo "Valid selections are:" #
echo "1 -> standard" #
echo "2 -> custom" #
echo "--->" #
getGPIONumberA() { #
  read -p "Please enter the BCM Number for Button A :" ANumber #
  case "$ANumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledBtnA = \)\(.*\)/\1$ANumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberB() { #
  read -p "Please enter the BCM Number for Button B :" BNumber #
  case "$BNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledBtnB = \)\(.*\)/\1$BNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberC() { #
  read -p "Please enter the BCM Number for Button C :" CNumber #
  case "$CNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledBtnC = \)\(.*\)/\1$CNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberD() { #
  read -p "Please enter the BCM Number for Button D :" DNumber #
  case "$DNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledBtnD = \)\(.*\)/\1$DNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberLL() { #
  read -p "Please enter the BCM Number for Left-Rotary-Left :" LLNumber #
  case "$LLNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledLtrLeft = \)\(.*\)/\1$LLNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberLR() { #
  read -p "Please enter the BCM Number for Left-Rotary-Right :" LRNumber #
  case "$LRNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledLtrRight = \)\(.*\)/\1$LRNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberLRB() { #
  read -p "Please enter the BCM Number for Left-Rotary-Button :" LRBNumber #
  case "$LRBNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledLtrBtn = \)\(.*\)/\1$LRBNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
}
getGPIONumberL() { #
  read -p "Please enter the BCM Number for Right-Rotary-Left :" LNumber #
  case "$LNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledRtrLeft = \)\(.*\)/\1$LNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberR() { #
  read -p "Please enter the BCM Number for Right-Rotary-Right :" RNumber #
  case "$RNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledRtrRight = \)\(.*\)/\1$RNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
} #
getGPIONumberRB() { #
  read -p "Please enter the BCM Number for Right-Rotary-Button :" RBNumber #
  case "$RBNumber" in #
    0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27) #    
      sed -i "s/\(oledRtrBtn = \)\(.*\)/\1$RBNumber/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Number was out of range...(must be 0-26)" #
      return 1 #
      ;; #
  esac #
}
getButtonLayout() { #
  read -p "Enter your decision: " ButonNumber #
  case "$ButonNumber" in #
    1) #    
      sed -i 's/\(oledBtn = \)\(.*\)/\14/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      sed -i 's/\(oledBtn = \)\(.*\)/\117/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      sed -i 's/\(oledBtn = \)\(.*\)/\15/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      sed -i 's/\(oledBtn = \)\(.*\)/\16/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      sed -i 's/\(oledLtrLeft = \)\(.*\)/\15/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      sed -i 's/\(oledLtrRight = \)\(.*\)/\16/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      sed -i 's/\(oledLtrBtn = \)\(.*\)/\13/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #  
      sed -i 's/\(oledRtrLeft = \)\(.*\)/\122/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      sed -i 's/\(oledRtrRight = \)\(.*\)/\123/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py # 
      sed -i 's/\(oledRtrBtn = \)\(.*\)/\127/' /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #  
      echo " " #
      echo "Set standard-buttonlayout" #
      return 0 #
      ;; #
    2) #
      echo "Please Enter the BCM-(GPIO) Number for each Button." #
      echo " " #
      echo "For BCM2 enter 2, for BCM17 enter 17..." #
      echo "BCM-list: https://de.pinout.xyz/#" #
      echo " " #
      echo "the input is not filtered!!!"  #
      echo "-> if you enter something wrong, something wrong will happen!" #
      echo " " #
      until getGPIONumberA; do : ; done #
      until getGPIONumberB; do : ; done #
      until getGPIONumberC; do : ; done #
      until getGPIONumberD; do : ; done #  
      until getGPIONumberLL; do : ; done #
      until getGPIONumberLR; do : ; done #
      until getGPIONumberLRB; do : ; done #      
      until getGPIONumberL; do : ; done #
      until getGPIONumberR; do : ; done #
      until getGPIONumberRB; do : ; done #      
      echo " " #
      echo "Set custom-buttonlayout" #
      return 0 #
      ;; #        
    *) #
      printf %s\\n "Please enter '1' or '2'" #
      return 1 #
      ;; #
  esac #
} #
until getButtonLayout; do : ; done #
echo "_________________________________________________________________" #
echo " " #
echo " " #
echo "___________________________________________________" #
echo "Please enter a Value for Pause -> to -> Stop -Time." #
echo "___________________________________________________ " #
echo " " #
echo "Value is in Seconds = 15 = 15 Seconds." #
echo "After this time, while playback is paused, player will Stop and return to Standby-Screen." #
echo " " #
echo "____________________________________________ " #
echo "Valid values are numbers between 1 and 86400" #
echo "86400 seconds are 24 hours..." #
echo " " #
getPlay2PauseTime() { #
  read -p "Enter a Time (in seconds): " Play2PauseT #
  case "$Play2PauseT" in #
    [1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-8][0-6][0-3][0-9][0-9]|86400) #     
      sed -i "s/\(oledPause2StopTime = \)\(.*\)/\1$Play2PauseT.0/" /home/pi/NR1-UI-Remote/ConfigurationFiles/PreConfiguration.py #
      echo " " #
      echo -n "Set Play-to-Pause timer to "; echo -n "${Play2PauseT} "; echo -n "seconds" #
      return 0 #
      ;; #
    *) #
      printf %s\\n "Please enter a number between '1' and '86400'" #
      return 1 #
      ;; #
  esac #
} #
until getPlay2PauseTime; do : ; done #
echo " " #
echo " " #
echo " " #
echo " " #
echo "Installation has finished, congratulations!" #
echo " " #
echo " " #
echo "Please have a look in the Installation instructions to finish setup." #                                                                                                                        
echo " " #
echo " " #
echo " " #
echo " " #
exit 0
