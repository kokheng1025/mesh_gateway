# Copyright (c) 2010 - 2018, Nordic Semiconductor ASA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of Nordic Semiconductor ASA nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL NORDIC SEMICONDUCTOR ASA OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from mesh.access import Model, Opcode
from models.common import TransitionTime
import struct, time

class LightingControlClient(Model):
    LIGHTING_CONTROL_SET_DALI_DIRECT_CMD = Opcode(0xE0, company_id=0x59, name="Lighting control Set Dali direct arc control command")
    LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD = Opcode(0xE1, company_id=0x59, name="Lighting control Set Dali indirect arc control command")
    LIGHTING_CONTROL_SET_DALI_CONFIGURATION_CMD = Opcode(0xE2, company_id=0x59, name="Lighting control Set Dali configuration command")
    LIGHTING_CONTROL_GET_DALI_QUERY_CMD = Opcode(0xE3, company_id=0x59, name="Lighting control Get Dali query command")
    LIGHTING_CONTROL_SET_UNLOCK_DRIVER = Opcode(0xE4, company_id=0x59, name="Lighting control Set unlock Dali driver")
    LIGHTING_CONTROL_GET_DRIVER_SN = Opcode(0xE5, company_id=0x59, name="Lighting control Get Dali light driver serial number")
    LIGHTING_CONTROL_GET_DRIVER_ACT_ENERGY = Opcode(0xE6, company_id=0x59, name="Lighting control Get dali light driver active energy")
    LIGHTING_CONTROL_GET_DRIVER_ACT_POWER = Opcode(0xE7, company_id=0x59, name="Lighting control Get dali light driver active power")
    LIGHTING_CONTROL_GET_DRIVER_VOLTAGE = Opcode(0xE8, company_id=0x59, name="Lighting control Get dali light driver voltage")
    LIGHTING_CONTROL_GET_DRIVER_CURRENT = Opcode(0xE9, company_id=0x59, name="Lighting control Get dali light driver current")
    LIGHTING_CONTROL_GET_LAMP_ON_TIME = Opcode(0xEA, company_id=0x59, name="Lighting control Get dali light on time")

    LIGHTING_CONTROL_GET_GPS_COORDINATES = Opcode(0xEB, company_id=0x59, name="Lighting control Get gps coordinates")
    LIGHTING_CONTROL_GET_ACCELEROMETER = Opcode(0xEC, company_id=0x59, name="Lighting control Get accelerometer roll and pitch angle")
    LIGHTING_CONTROL_SET_GPS_UART_DEVICE = Opcode(0xED, company_id=0x59, name="Lighting control Set enable gps module")    
    LIGHTING_CONTROL_SET_ACCELEROMTER_CALIBRATION = Opcode(0xEE, company_id=0x59, name="Lighting control Set enable accelerometer calibration")    

    LIGHT_CONTROL_STATUS_DALI_CMD = Opcode(0xF0, company_id=0x59, name="Lighting control Status dali command")
    LIGHT_CONTROL_STATUS_DALI_SPECIAL_CMD = Opcode(0xF1, company_id=0x59, name="Lighting control Status dali special command")
    LIGHT_CONTROL_STATUS_GPS_COORDINATES_CMD = Opcode(0xF2, company_id=0x59, name="Lighting control Status gps coordinates command")
    LIGHT_CONTROL_STATUS_ACCELEROMETER_CMD = Opcode(0xF3, company_id=0x59, name="Lighting control Status 3-axis accelerometer command")

    def __init__(self):
        self.opcodes = [
            (self.LIGHT_CONTROL_STATUS_DALI_CMD, self.__light_control_dali_status_handler),
            (self.LIGHT_CONTROL_STATUS_DALI_SPECIAL_CMD, self.__light_control_dali_status_special_handler),
            (self.LIGHT_CONTROL_STATUS_GPS_COORDINATES_CMD, self.__light_control_gps_status_handler),
            (self.LIGHT_CONTROL_STATUS_ACCELEROMETER_CMD, self.__light_control_accelerometer_status_handler)]
        self.__tid = 0
        super(LightingControlClient, self).__init__(self.opcodes)

    def set_lamp_power(self, brightness):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFE, 0, brightness, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_DIRECT_CMD, message)

    def set_lamp_off(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x00, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD, message)
    
    def add_lamp_fade_rate(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x01, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD, message)

    def minus_lamp_fade_rate(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x02, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD, message)
    
    def add_lamp_power_by_one(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x03, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD, message)

    def minus_lamp_power_by_one(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x04, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD, message)
    
    def set_lamp_power_max(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x05, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD, message)

    def set_lamp_power_min(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x06, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_SET_DALI_INDIRECT_CMD, message)

    def set_driver_unlock(self):
        self.send(self.LIGHTING_CONTROL_SET_UNLOCK_DRIVER)

    def reset_driver(self):
        self.set_lamp_off()
        time.sleep(0.5)
        self.set_lamp_power_max()

    def get_lamp_power(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0xA0, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_GET_DALI_QUERY_CMD, message)
    
    def get_driver_status(self):
        message = bytearray()
        message += struct.pack("<BBBB", 0xFF, 0x90, 0, self._tid)
        self.send(self.LIGHTING_CONTROL_GET_DALI_QUERY_CMD, message)

    def get_driver_sn(self):
        self.send(self.LIGHTING_CONTROL_GET_DRIVER_SN)

    def get_driver_active_energy(self):
        self.send(self.LIGHTING_CONTROL_GET_DRIVER_ACT_ENERGY)

    def get_driver_active_power(self):
        self.send(self.LIGHTING_CONTROL_GET_DRIVER_ACT_POWER) 

    def get_driver_voltage(self):
        self.send(self.LIGHTING_CONTROL_GET_DRIVER_VOLTAGE)

    def get_driver_current(self):
        self.send(self.LIGHTING_CONTROL_GET_DRIVER_CURRENT)

    def get_lamp_on_time(self):
        self.send(self.LIGHTING_CONTROL_GET_LAMP_ON_TIME)

    def set_gps_device(self, enable):
        message = bytearray()
        message += struct.pack("<?B", enable, self.__tid)
        self.send(self.LIGHTING_CONTROL_SET_GPS_UART_DEVICE, message)

    def get_gps_coordinates(self):
        self.send(self.LIGHTING_CONTROL_GET_GPS_COORDINATES)

    def get_accel_value(self):
        self.send(self.LIGHTING_CONTROL_GET_ACCELEROMETER)

    def set_accel_calibration(self, enable):
        message = bytearray()
        message += struct.pack("<?B", enable, self.__tid)
        self.send(self.LIGHTING_CONTROL_SET_ACCELEROMTER_CALIBRATION, message)

    @property
    def _tid(self):
        tid = self.__tid
        self.__tid += 1
        if self.__tid >= 255:
            self.__tid = 0
        return tid

    def __light_control_dali_status_handler(self, opcode, message):   
        logstr = "Dali Command, error code: %s, data: %d" % (bytes(message.data[0:4]).hex(), message.data[4])
        self.logger.info(logstr)

    def __light_control_dali_status_special_handler(self, opcode, message):
        logstr = "Dali special command, error code: %s, data: %s" % (bytes(message.data[0:4]).hex(), bytes(message.data[6:16]).hex())
        self.logger.info(logstr)

    def __light_control_gps_status_handler(self, opcode, message):
        latitude = struct.unpack('d', bytes(message.data[4:12]))[0]
        longitude = struct.unpack('d', bytes(message.data[12:20]))[0]
        logstr = "gps command, err code: %s, latitude: %3.4f, longitude: %3.4f" % (bytes(message.data[0:4]).hex(), latitude, longitude)
        self.logger.info(logstr)

    def __light_control_accelerometer_status_handler(self, opcode, message):
        roll_angle = struct.unpack('i', bytes(message.data[4:8]))[0]
        pitch_angle = struct.unpack('i', bytes(message.data[8:12]))[0]
        logstr = "accelerometer command, err code: %s, roll angle: %i, pitch angle: %i" % (bytes(message.data[0:4]).hex(), roll_angle, pitch_angle)
        self.logger.info(logstr)
