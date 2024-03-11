import pdb
import socket
from time import sleep
import sys

SOCKET_TIMEOUT = 600
PC_IP_ADDRESS = "141.212.84.36"
#PC_IP_ADDRESS = "172.17.32.1"
#PC_IP_ADDRESS = "192.168.0.1"
PORT = 8000

# Define material thickness, Z-axis index
GLASS = 0
SILICON = 1
# Safe zones min, max
SAFE_ZONE_NOZZLE_X = [0, 175]
SAFE_ZONE_NOZZLE_Y = [0, 100]
SAFE_ZONE_NOZZLE_Z = [2.85, 3.45, 5]
SAFE_ZONE_AFM_X = [0, 25]
SAFE_ZONE_AFM_Y = [-15, 200]
SAFE_ZONE_AFM_Z = [3.9, 4.5, 5]

NOTHING = object() #placeholder for self.default_feedrate, do not delete

class Staging(object):
	def __init__(self, material = 0, incremental = False):
		self.default_feedrate = 1.0 # mm/s #Eventually replace with None
		self.x = 0
		self.y = 0
		self.z = 0
		self.initialized = True
		if not incremental:
			#absolute mode
			print('Staging initialized - Absolute mode')
		elif incremental:
			#incremental mode
			print('Staging initialized - Incremental mode')
	def goto(self, x = None, y = None, z = None, f = NOTHING):
		if f is NOTHING:
			f=self.default_feedrate
		print('Moving by', x, ' ', y, ' ', z, ' at speed ', f, ' mm/s.\n')
		if x != None:	
			self.x += x
		if y != None:	
			self.y += y
		if z != None:	
			self.z += z	
	def gotoxyz(self, pos_array=(None,None,None), f=NOTHING):#wrapper
		x=pos_array[0]
		y=pos_array[1]
		z=pos_array[2]
		self.goto(x,y,z,f)
	def goto_rapid(self, x = None, y = None, z = None):
		print('Moving rapidly by', x, ' ', y, ' ', z)
		if x != None:	
			self.x += x
		if y != None:	
			self.y += y
		if z != None:	
			self.z += z			
	def send_message(self, msg):
		print(msg)
	def set_pos(self, x = None , y = None , z = None ): #for testing only
		if x != None:	
			self.x = x
		if y != None:	
			self.y = y
		if z != None:	
			self.z = z	
	def get_coords(self, axis):#for testing
		return (self.x, self.y, self.z)
	def get_pos(self, axis = None):
		if axis in ['x', 'X']:
			return float(self.x)
		elif axis in ['y', 'Y']:
			return float(self.y)
		elif axis in ['z', 'Z']: #Z fine
			return float(self.z)
		else:
			raise ValueError('get_pos was called without a valid axis')


class Aerotech(Staging):
    def __init__(self, material=0, incremental=False):
        self.default_feedrate = 1.0
        print(f'IncrementalB: {incremental}')

        # Absolute Mode
        self.socket = socket.socket()
        self.socket.settimeout(SOCKET_TIMEOUT)
        self.socket.connect((PC_IP_ADDRESS, PORT))
        sleep(1)
        self.send_message('ENABLE X Y Z\n')
        self.send_message('METRIC\n')
        self.send_message('SECOND\n')
        self.send_message('RAMP RATE 100\n')
        self.send_message('WAIT MODE INPOS\n')
        print(f'Incremental: {incremental}')
        if not incremental:
            # absolute mode
            self.send_message('ABSOLUTE\n')
            self.send_message('G92 X0 Y0 Z0\n')
            print('Aerotech initialized = Absolute mode')
            pdb.set_trace()
            self.mode = 'Absolute'
        elif incremental:
            # incremental mode
            self.send_message('INCREMENTAL\n')
            print('Aerotech initialized = Incremental mode')
            self.mode = 'Incremental'

    def __del__(self):
        self.delete_safe_zones()
        print('Aerotech closed')

    def create_safe_zone(self, material):
        # Define Nozzle safe zone
        self.send_message('SAFEZONE 0 CLEAR\n')
        self.send_message('SAFEZONE 0 TYPE SAFEZONETYPE_NoEnter \n')
        self.send_message('SAFEZONE 0 SET X ' + repr(SAFE_ZONE_NOZZLE_X[0]) + ', ' + repr(SAFE_ZONE_NOZZLE_X[1]) + '\n')
        self.send_message('SAFEZONE 0 SET Y ' + repr(SAFE_ZONE_NOZZLE_Y[0]) + ', ' + repr(SAFE_ZONE_NOZZLE_Y[1]) + '\n')
        self.send_message('SAFEZONE 0 SET Z ' + repr(SAFE_ZONE_NOZZLE_Z[material]) + ', ' + repr(SAFE_ZONE_NOZZLE_Z[len(SAFE_ZONE_NOZZLE_Z) - 1]) + '\n')
        self.send_message('SAFEZONE 0 ON\n')

        # Define AFM safe zone
        self.send_message('SAFEZONE 1 CLEAR\n')
        self.send_message('SAFEZONE 1 TYPE SAFEZONETYPE_NoEnter \n')
        self.send_message('SAFEZONE 1 SET X ' + repr(SAFE_ZONE_AFM_X[0]) + ', ' + repr(SAFE_ZONE_NOZZLE_X[1]) + '\n')
        self.send_message('SAFEZONE 1 SET Y ' + repr(SAFE_ZONE_AFM_Y[0]) + ', ' + repr(SAFE_ZONE_NOZZLE_Y[1]) + '\n')
        self.send_message('SAFEZONE 1 SET Z ' + repr(SAFE_ZONE_AFM_Z[material]) + ', ' + repr(SAFE_ZONE_AFM_Z[len(SAFE_ZONE_AFM_Z) - 1]) + '\n')
        self.send_message('SAFEZONE 1 ON\n')

    def delete_safe_zones(self):
        self.send_message('SAFEZONE 0 CLEAR\n')
        self.send_message('SAFEZONE 1 CLEAR\n')

    def get_socket(self):
        return self.socket

    def goto(self, x = None, y = None, z = None, f = NOTHING):
        if f is NOTHING:
            f = self.default_feedrate
        if x != None or y != None or z != None:
            msg = 'LINEAR' #G1
            if x != None:
                msg += ' X' + ('%0.6f' %x)
            if y != None:
                msg += ' Y' + ('%0.6f' %y)
            if z != None:
                msg += ' Z' + ('%0.6f' %z)
            if f != None:
                msg += ' F' + ('%0.6f' %f)
        elif f != None:
            msg = 'F' + repr(f)
        else:
            raise ValueError('staging.goto() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)

    def setPressure(self, pressure = None):
        if pressure != None:
            msg = '$AO[1].X = '
            msg += '%0.6f' %pressure

        else:
            raise ValueError('staging.setPressure() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)

    def goto_xyz(self, pos_array=(None, None, None), f=NOTHING):
        x = pos_array[0]
        y = pos_array[1]
        z = pos_array[2]
        self.goto(x, y, z, f)

    def goto_rapid(self, x = None, y = None, z = None):
        if x != None or y != None or z != None:
            msg = 'RAPID' #G0
            if x != None:
                msg += ' X' + repr(x)
            if y != None:
                msg += ' Y' + repr(y)
            if z != None:
                msg += ' Z' + repr(z)
        else:
            raise ValueError('staging.goto_rapid() wad called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)

    def send_message(self, msg):
        print(msg)
        self.socket.send(msg.encode())
        number_of_msg = msg.count('\n')
        for msg_counter in range(number_of_msg):
            self.recv_msg = ''
            recv_str = self.socket.recv(1024).decode()
            print(recv_str)
            self.recv_msg += recv_str # builds a received message for the last command only
        if (len(self.recv_msg)>1):
            return str(self.recv_msg[1:-1])

