import os
from pathlib import Path
import struct
from encrypt_alg.test import generator_factory

def increment_params(params, incr_1_total, incr_2_total):
    new_params = dict(params)
    keys = list(new_params.keys())
    new_params[keys[0]] += incr_1_total
    for key in keys[1:]:
        new_params[key] += incr_2_total
    return new_params

def extract_mantissa_bits(x):
    u = struct.unpack(">Q", struct.pack(">d", x))[0]
    mant = u & ((1 << 52) - 1)
    word = (mant >> 10) & 0xFFFFFFFF
    return f"{word:032b}"

def generate_bin_from_multiple_seeds(sytem_type, factory, params, mode, first_system_iter, second_system_iter):
    output_dir = Path(f"../dataNist/{sytem_type}")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"logistic_{sytem_type}_multiple_seeds_data.bin"
    file_path = Path(filename)
    if file_path.exists():
        os.remove(filename)
    with open(filename, "wb") as f:
        for i in range(0, 55):
            current_params = increment_params(params, first_system_iter * i, second_system_iter * i)
            generator = factory.create_generator(sytem_type, current_params, mode)
            sequence = generator.get_sequence(31251)
            byte_array = bytearray(
                b
                for element in sequence
                for b in int(extract_mantissa_bits(element),2).to_bytes(4, byteorder='big')
            )
            f.write(byte_array)

def generate_bin_from_one_seed(sytem_type, generator):
        sequence = generator.get_sequence(1718751)
        byte_array = bytearray(
            b
            for element in sequence
            for b in int(extract_mantissa_bits(element), 2).to_bytes(4, byteorder='big')
        )
        output_dir = Path(f"../dataNist/{sytem_type}")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = output_dir / f"logistic_{sytem_type}_one_seed.bin"
        file_path = Path(filename)
        if file_path.exists():
            os.remove(filename)
        with open(filename, "wb") as f:
            f.write(byte_array)

def generate_bin_from_multiple_seeds_SHA(sytem_type, factory, params, mode, first_system_iter, second_system_iter):
    output_dir =  Path(f"../dataNist/{sytem_type}")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"logistic_{sytem_type}_sha_multiple_seeds_data.bin"
    file_path = Path(filename)
    if file_path.exists():
         os.remove(filename)
    with open(filename, "wb") as f:
        for i in range(0, 55):
            current_params = increment_params(params, first_system_iter * i, second_system_iter * i)
            generator = factory.create_generator(sytem_type, current_params, mode)
            sequence = generator.get_sequence(125001)
            generated_sequence_string = b"".join(sequence)
            f.write(generated_sequence_string)

def generate_bin_from_one_seed_SHA(sytem_type, generator):
    output_dir = Path(f"../dataNist/{sytem_type}")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"logistic_{sytem_type}_sha_one_seed.bin"
    sequence = generator.get_sequence(6875001)
    generated_sequence_string = b"".join(sequence)
    file_path = Path(filename)
    if file_path.exists():
        os.remove(filename)
    with open(filename, "wb") as f:
        f.write(generated_sequence_string)

"""-----------------------------Lorenz Nist files generations------------------------------------------------"""

# Number multiple seeds
params = {
    "logisticXLorenz": 0.01,
    "lorenzX": -20,
    "lorenzY": -20,
    "lorenzZ": 0,
}
#gen1= generator_factory.create_generator("lorenz", params, "chars" )
#generate_bin_from_multiple_seeds("lorenz", generator_factory, params, "chars" ,0.01, 0.5)
# Number one seed
# gen2 = generator_factory.create_generator("lorenz", params, "chars" )
# generate_bin_from_one_seed("lorenz", gen2)
# # SHA multiple seeds
# #gen3= generator_factory.create_generator("lorenz", params, "bytes" )
# generate_bin_from_multiple_seeds_SHA("lorenz",generator_factory, params, "bytes", 0.01, 0.5)
# SHA one seed
gen4 = generator_factory.create_generator("lorenz", params, "bytes")
generate_bin_from_one_seed_SHA("lorenz", gen4)

"""-----------------------------Rossler Nist files generations------------------------------------------------"""
#
# params = {
#     "logisticXRossler":0.01,
#     "rosslerX": -15,
#     "rosslerY": -15,
#     "rosslerZ": 0
# }
#
# # Number multiple seeds
# #gen5 = generator_factory.create_generator("rossler", params, "chars" )
# generate_bin_from_multiple_seeds("rossler",  generator_factory, params, "chars" , 0.01, 0.4)
# # Number one seed
# gen6 = generator_factory.create_generator("rossler", params, "chars" )
# generate_bin_from_one_seed("rossler", gen6)
# # SHA multiple seeds
# #gen7= generator_factory.create_generator("rossler", params, "bytes" )
# generate_bin_from_multiple_seeds_SHA("rossler", generator_factory, params, "bytes", 0.01, 0.4)
# # SHA one seed
# gen8 = generator_factory.create_generator("rossler", params, "bytes")
# generate_bin_from_one_seed_SHA("rossler", gen8)
#
# """-----------------------------Chua Nist files generations----------------------------------------------------"""
#
# params = {
#     "logisticXChua":0.01,
#     "chuaX": -3,
#     "chuaY": -2,
#     "chuaZ": -3
# }
#
#
# # Number multiple seeds
# #gen9 = generator_factory.create_generator("chua", params, "chars" )
# generate_bin_from_multiple_seeds("chua",  generator_factory, params, "chars" , 0.01, 0.06)
# # Number one seed
# gen10 = generator_factory.create_generator("chua", params, "chars" )
# generate_bin_from_one_seed("chua", gen10)
# # SHA multiple seeds
# #gen11= generator_factory.create_generator("chua", params, "bytes" )
# generate_bin_from_multiple_seeds_SHA("chua",  generator_factory, params, "bytes", 0.01, 0.06)
# # SHA one seed
# gen12 = generator_factory.create_generator("chua", params, "bytes")
# generate_bin_from_one_seed_SHA("chua", gen12)
#
#
# """-----------------------------Duffing Nist files generations------------------------------------------------"""
#
#
# params = {
#     "logisticXDuffing":0.01,
#     "duffingX": -2,
#     "duffingY": -2,
#     "duffingT": 0
# }
#
#
# # = generator_factory.create_generator("duffing", params, "chars" )
# generate_bin_from_multiple_seeds("duffing", generator_factory, params, "chars" ,  0.01, 0.06)
# # Number one seed
# gen14 = generator_factory.create_generator("duffing", params, "chars" )
# generate_bin_from_one_seed("duffing", gen14)
# # SHA multiple seeds
# #gen15= generator_factory.create_generator("duffing", params, "bytes" )
# generate_bin_from_multiple_seeds_SHA("duffing", generator_factory, params, "bytes", 0.01, 0.06)
# # SHA one seed
# gen16 = generator_factory.create_generator("duffing", params, "bytes")
# generate_bin_from_one_seed_SHA("duffing", gen16)
#
#
# """-----------------------------Van der Pol Nist files generations----------------------------------------------------"""
#
# params = {
#     "logisticXPol":0.01,
#     "polX": -3,
#     "polY": -8,
#     "polT": 0
# }
#
# #gen17 = generator_factory.create_generator("pol", params, "chars" )
# generate_bin_from_multiple_seeds("pol", generator_factory, params, "chars", 0.01, 0.1)
# # Number one seed
# gen18 = generator_factory.create_generator("pol", params, "chars" )
# generate_bin_from_one_seed("pol", gen18)
# # SHA multiple seeds
# #gen19= generator_factory.create_generator("pol", params, "bytes" )
# generate_bin_from_multiple_seeds_SHA("pol", generator_factory, params, "bits", 0.01, 0.1)
# # SHA one seed
# gen20 = generator_factory.create_generator("pol", params, "bytes")
# generate_bin_from_one_seed_SHA("pol", gen20)
#
#
#
# """-----------------------------Forced Pendulum Nist files generations------------------------------------------------"""
#
# params = {
#     "logisticXForced":0.01,
#     "forcedX": -math.pi,
#     "forcedY": -6,
#     "forcedT": 0
# }
#
# #gen21 = generator_factory.create_generator("forced", params, "chars" )
# generate_bin_from_multiple_seeds("forced", generator_factory, params, "chars", 0.01, 0.1)
# # Number one seed
# gen22 = generator_factory.create_generator("forced", params, "chars" )
# generate_bin_from_one_seed("forced", gen22)
# # SHA multiple seeds
# #gen23= generator_factory.create_generator("forced", params, "bytes" )
# generate_bin_from_multiple_seeds_SHA("forced", generator_factory, params, "bits", 0.01, 0.1)
# # SHA one seed
# gen24 = generator_factory.create_generator("forced", params, "bytes")
# generate_bin_from_one_seed_SHA("forced", gen24)
#
#
#
#
#
#
