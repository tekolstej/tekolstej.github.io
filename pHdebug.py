import spidev
import time

#Initialize SPI
spi = spidev.SpiDev() #Create and instance of the SpiDev class
spi.open(0,0) #Open SPI bus 0, device 0 (CEO)
spi.max_speed_hz = 1000000 #Set the SPI clock speed

#Define VREF (reference voltage for ADC)
VREF = 5.0 #Set to 5.0 if the ADC0834 is using a 5v reference

def read_adc0834(channel):
    """Read a channel from the ADC0834."""
    assert 0 <= channel <= 3, "Channel must be 0-3"
    #SPI command to read the specified channel 
    cmd = [1, (8 + channel) << 4, 0]
    adc = spi.xfer2(cmd)
    adc_value = ((adc[1] & 3) << 8) + adc[2] #Combine the 10-bit result
    return adc_value

try:
    while True:
        # Read pH from CH0
        adc_value_ph = read_adc0834(0)  #Read from  CH0
        voltage_ph = adc_value_ph * (VREF / 255) #Convert to voltage

        # Read temperature from CH1
        adc_value_temp = read_adc0834(1)  #Read from CH1
        voltage_temp = adc_value_temp * (VREF / 255) #Conver to voltage

        #Print both readings
        print(f"pH Voltage: {voltage_ph:.2f}V, Temp Voltage: {voltage_temp:.2f}V")
        time.sleep(1)
except KeyboardInterrupt:
    #Cleanup SPI connection on exit
    spi.close()
    print("Exiting...")
