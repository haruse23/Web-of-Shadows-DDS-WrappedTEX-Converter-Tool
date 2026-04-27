import struct
import re
import math
import numpy as np   

def read_ubyte(f):
    return struct.unpack("<B", f.read(1))[0]

def read_ushort(f):
    return struct.unpack("<H", f.read(2))[0]

def read_vertex_position_short(f):
    return struct.unpack("<h", f.read(2))[0]

def read_uint(f):
    return struct.unpack("<I", f.read(4))[0]


def read_float(f):
    return struct.unpack("<f", f.read(4))[0]

def read_bytes(f, format):
    match = re.search(r'\d+', format)
    return struct.unpack(format, f.read(int(match.group())))

def convert_half_float_to_float(f):
    """
    Read 2 bytes (half-float) and return as Python float.
    """
    
    # Unpack as 16-bit unsigned integer
    h = struct.unpack('<H', f.read(2))[0]  # Little-endian

    # Convert half-float to float
    s = (h >> 15) & 0x00000001    # sign
    e = (h >> 10) & 0x0000001F    # exponent
    f = h & 0x000003FF             # fraction

    if e == 0:
        if f == 0:
            # Zero
            return float((-1)**s * 0.0)
        else:
            # Subnormal number
            return (-1)**s * (f / 1024) * 2**(-14)
    elif e == 31:
        # Inf or NaN
        return float('inf') if f == 0 else float('nan')
    else:
        # Normalized number
        return (-1)**s * (1 + f / 1024) * 2**(e - 15)


def convert_float_to_half_float(value):
    """
    Convert a Python float to a 16-bit half-float representation (as bytes).
    Returns a bytes object of length 2.
    """

    f = float(value)

    if math.isnan(f):
        h = 0x7E00  # standard half-float NaN
    elif math.isinf(f):
        h = 0x7C00 if f > 0 else 0xFC00
    elif f == 0.0:
        # Preserve sign
        h = 0x8000 if math.copysign(1.0, f) < 0 else 0x0000
    else:
        # Normalized or subnormal number
        s = 0
        if f < 0:
            s = 1
            f = -f

        # Get exponent and fraction
        e = int(math.floor(math.log(f, 2)))
        if e < -14:
            # Subnormal
            f_frac = int(round(f / 2**(-24)))  # f / 2^-24 for 10-bit fraction
            h = (s << 15) | f_frac
        elif e > 15:
            # Overflow → Inf
            h = (s << 15) | (0x1F << 10)
        else:
            # Normalized
            frac = f / (2 ** e) - 1.0
            f_frac = int(round(frac * 1024))  # 10-bit fraction
            h = (s << 15) | ((e + 15) << 10) | (f_frac & 0x3FF)

    return struct.pack('<H', h)


def convert_float_to_half_float_numpy(value):
    return np.float16(value).tobytes()
    
def convert_half_float_to_float_numpy(data):
    return np.frombuffer(data, dtype='<f2').astype(np.float32)
    

def write_ubyte(f, data):
    f.write(struct.pack("<B", data))
    
def write_uint(f, data):
    f.write(struct.pack("<I", data))
    
def write_ushort(f, data):
    f.write(struct.pack("<H", data))
    
def write_float(f, data):
    f.write(struct.pack("<f", data))


def align_to_4(f, offset):
    alignment_bytes = (4 - (offset % 4)) % 4
    f.seek(alignment_bytes, 1)
    
def align_to_16(f, offset):
    alignment_bytes = (16 - (offset % 16)) % 16
    f.seek(alignment_bytes, 1)
    
def write_alignment_4(f, offset):
    alignment_bytes = (4 - (offset % 4)) % 4
    if alignment_bytes:
        f.write(b'\x00' * alignment_bytes)
        
def write_alignment_16(f, offset):
    alignment_bytes = (16 - (offset % 16)) % 16
    if alignment_bytes:
        f.write(b'\x00' * alignment_bytes)
        
def write_alignment_16_A1(f, offset):
    alignment_bytes = (16 - (offset % 16)) % 16
    if alignment_bytes:
        f.write(b'\xA1' * alignment_bytes)

    
