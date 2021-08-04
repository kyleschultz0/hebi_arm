//include SPI library
#include <SPI.h>

//this is the serial baud rate for talking to the Arduino
#define baudRate 115200

//this will be our SPI timout limit
#define timoutLimit 500

//SPI commands used by the AMT20
#define nop 0x00            //no operation
#define rd_pos 0x10         //read position
#define set_zero_point 0x70 //set zero point

//set the chip select pin for the AMT20
int SSS[] = {8, 9,10}; // SSS pins in order of encoder connection

//Arduino uses a setup function for all program initializations
void setup() 
{
  //Initialize the UART serial connection
  Serial.begin(baudRate);

  //Set I/O mode of all SPI pins.
  pinMode(SCK, OUTPUT);
  pinMode(MOSI, OUTPUT);
  pinMode(MISO, INPUT);
  pinMode(SSS[0], OUTPUT);
  pinMode(SSS[1], OUTPUT);
  pinMode(SSS[2], OUTPUT);

  //Initialize SPI using the SPISettings(speedMaxium, dataOrder, dataAMode) function
  //For our settings we will use a clock rate of 500kHz, and the standard SPI settings
  //of MSB First and SPI Mode 0
  SPI.beginTransaction(SPISettings(500000, MSBFIRST, SPI_MODE0));
  
  //Using SPI.beginTransaction seems to require explicitly setting the beginning state
  //of the CS pin as opposed to the SPI.begin() function that does this for us.
  digitalWrite(SSS[0], HIGH);
  digitalWrite(SSS[1], HIGH);  
  digitalWrite(SSS[2], HIGH);  
}

//After the setup() method this loop gets entered and is the main() function for our program
void loop() 
{
  uint8_t data;               //this will hold our returned data from the AMT20
  uint8_t timeoutCounter;     //our timeout incrementer
  uint16_t currentPosition;   //this 16 bit variable will hold our 12-bit position
  byte serial_reading;

    for (int i = 0; i < 3; i++) {
      //reset the timoutCounter;
      timeoutCounter = 0;

      //send the rd_pos command to have the AMT20 begin obtaining the current position
      data = SPIWrite(rd_pos,SSS[i]);
    
      //we need to send nop commands while the encoder proceSSSes the current position. We
      //will keep sending them until the AMT20 echos the rd_pos command, or our timeout is reached.
      while (data != rd_pos && timeoutCounter++ < timoutLimit)
      {
        data = SPIWrite(nop,SSS[i]);
      }
    
      if (timeoutCounter < timoutLimit) //rd_pos echo received
      {
        //We received the rd_pos echo which means the next two bytes are the current encoder position.
        //Since the AMT20 is a 12 bit encoder we will throw away the upper 4 bits by masking.
    
        //Obtain the upper position byte. Mask it since we only need it's lower 4 bits, and then
        //shift it left 8 bits to make room for the lower byte.
        currentPosition = (SPIWrite(nop,SSS[i])& 0x0F) << 8;
    
        //OR the next byte with the current position
        currentPosition |= SPIWrite(nop,SSS[i]);

        //Serial.write("I know my currenct position!");
      }
      else //timeout reached
      {
        //This means we had a problem with the encoder, most likely a lost connection. For our
        //purposes we will alert the user via the serial connection, and then stay here forever.
    
        Serial.write("Error obtaining position.\n");
        Serial.write("Reset Arduino to restart program.\n");
        
        while(true);
      }
      
      Serial.print(currentPosition);
      if(i < 2) {
        // add comma in between readings
        Serial.write(",");
      }
    }

    while(true){
      if (Serial.available() != 0){
        // wait for computer to as for reading
        break;
      }
    }

    while(Serial.available() > 0){
      // clear arduino input buffer by reading all incoming bytes
      // reset for next measurement
      Serial.read();
    }

    // send 
    Serial.write("\n");
}

//We will use this function to handle transmitting SPI commands in order to keep our code clear and concise.
//It will return the byte received from SPI.transfer()
uint8_t SPIWrite(uint8_t sendByte, int SSS)
{
  //holder for the received over SPI
  uint8_t data;

  //the AMT20 requires the release of the CS line after each byte
  digitalWrite(SSS, LOW);
  data = SPI.transfer(sendByte);
  digitalWrite(SSS, HIGH);

  //we will delay here to prevent the AMT20 from having to prioritize SPI over obtaining our position
  delayMicroseconds(10);
  
  return data;
}
