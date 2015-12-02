#!usr/bin/python
import smbus
import time

bus = smbus.SMBus(1)	# 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

#Define some address values
DEVICE_ADDRESS = 0x29	#7 bit address (will be left shifted to add the r/w bit) 
VL6180X_SYSRANGE_START_MSB = 0x00   #VL6180X_SYSRANGE_START = 0x0018
VL6180X_SYSRANGE_START_LSB = 0x18  

VL6180X_RESULT_RANGE_VAL_MSB = 0x00   # VL6180X_RESULT_RANGE_VAL = 0x0062
VL6180X_RESULT_RANGE_VAL_LSB = 0x62

VL6180X_SYSTEM_INTERRUPT_CLEAR_MSB = 0x00 #VL6180X_SYSTEM_INTERRUPT_CLEAR = 0x0015
VL6180X_SYSTEM_INTERRUPT_CLEAR_LSB = 0x15

def VL6180_SensorInitOnStartup():
  
    #Initializations to be called on system startup (VL6180 IR Sensor)
    #Madatory: Private registers
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x02, [0x07, 0x01])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x02, [0x08, 0x01])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x96, 0x00])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x97, 0xfd])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xe3, 0x00])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xe4, 0x04])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xe5, 0x02])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xe6, 0x01])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xe7, 0x03])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xf5, 0x02])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xd9, 0x05])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xdb, 0xce])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xdc, 0x03])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xdd, 0xf8])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x9f, 0x00])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xa3, 0x3c])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xb7, 0x00])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xbb, 0x3c])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xb2, 0x09])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xca, 0x09])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x98, 0x01])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0xb0, 0x17])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0xad, 0x00])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0xff, 0x05])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x00, 0x05])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x99, 0x05])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0xa6, 0x1b])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0xac, 0x3e])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0xa7, 0x1f])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x30, 0x00])

    #Recommended: Public registers (see data sheet for more details)
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x11, 0x10]) # Enables 'new sa ready' polling
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, [0x0a, 0x30]) # Set the avergaging sa period
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x3f, 0x46]) #Sets light and dark gain
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x31, 0xFF]) #Sets # of range measurements before auto-cal
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x40, 0x63]) #Set ALS integration time to 100 ms
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x2e, 0x01]) #Perform a single temp calib of the ranging sensor

    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x1b, 0x09])
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x3e, 0x31]) 
    bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x14, 0x24]) 

    return 0

def VL6180_PollRange():
  
 #Poll 0x4f to see if new sample is ready
    bus.write_byte_data(DEVICE_ADDRESS, 0x00, 0x4f)
    pollStatus = bus.read_byte(DEVICE_ADDRESS)
    rangeStatus = pollStatus & 0x07
    
    while rangeStatus != 0x04:
        pollStatus = bus.read_byte(DEVICE_ADDRESS)   
        rangeStatus = pollStatus & 0x07
        #print("Polling 0x04f - %d" % rangeStatus)
        time.sleep(0.01)
    return 0

    


VL6180_SensorInitOnStartup()

#Clear fresh off reset register (need to do this like this?)
bus.write_i2c_block_data(DEVICE_ADDRESS, 0x00, [0x16, 0x00]) 

#Set to start continuous mode (move into while loop for single-shot mode)
bus.write_i2c_block_data(DEVICE_ADDRESS,  VL6180X_SYSRANGE_START_MSB, [VL6180X_SYSRANGE_START_LSB, 0x03])  #Start continuous mode (0x03) , use 0x01 single-shot mode
        #delay 10 ms here nefore calling next function?
  
# main loop for sensor polling
while 1:
   # time.sleep(0.1)

    VL6180_PollRange()
        
    #Read the Range value
    bus.write_byte_data(DEVICE_ADDRESS, VL6180X_RESULT_RANGE_VAL_MSB, VL6180X_RESULT_RANGE_VAL_LSB)
    val = bus.read_byte(DEVICE_ADDRESS)
  
    #clear interrupts
    bus.write_i2c_block_data(DEVICE_ADDRESS, VL6180X_SYSTEM_INTERRUPT_CLEAR_MSB, [VL6180X_SYSTEM_INTERRUPT_CLEAR_LSB, 0x07])

    #print the value to console
    print "Distance = %d" % val;        #Need to convert the sensor value? chk datasheet

