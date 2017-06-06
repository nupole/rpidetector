import time
import spidev

spi0 = spidev.SpiDev()
spi0.open(0,0)
spi0.max_speed_hz=int(10000000)
print spi0.max_speed_hz * 1E-06
command = 0b11 << 6
command |= (0 & 0x07) << 3
print command
starttime = time.time()
for i in range(0, 100000):
    tme = time.time()
    spi0.xfer2([command, 0x0, 0x0])
endtime = time.time()
print 99999.0 / (endtime - starttime)
spi0.close()
"""Read the current value of the specified ADC channel (0-7).  The values
can range from 0 to 1023 (10-bits).

assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
# Build a single channel read command.
# For example channel zero = 0b11000000
command = 0b11 << 6                  # Start bit, single channel read
command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
# Note the bottom 3 bits of command are 0, this is to account for the
# extra clock to do the conversion, and the low null bit returned at
# the start of the response.
resp = self._spi.transfer([command, 0x0, 0x0])
# Parse out the 10 bits of response data and return it.
result = (resp[0] & 0x01) << 9
result |= (resp[1] & 0xFF) << 1
result |= (resp[2] & 0x80) >> 7
return result & 0x3FF
"""
