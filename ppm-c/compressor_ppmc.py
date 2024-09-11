import sys
from ppmc_compress import PPMCCompressor
from ppmc_decompress import PPMCDecompressor

if len(sys.argv) != 2:
    print("Usage: python compressor_ppmc.py [input_file]")
    sys.exit(1)

# Lê o arquivo de entrada
input_file = sys.argv[1]
with open(input_file, 'rb') as file:
    data = file.read()

# Compressão
compressor = PPMCCompressor(max_order=4)
encoded_data = compressor.encode(data)

# Grava o arquivo comprimido
with open(input_file + '.ppmc', 'wb') as file:
    file.write(bytes(str(encoded_data), 'utf-8'))

# Descompressão
decompressor = PPMCDecompressor(max_order=4)
decoded_data = decompressor.decode(eval(str(encoded_data)))

# Grava o arquivo descomprimido
with open(input_file + '_uncompressed.txt', 'wb') as file:
    file.write(bytes(decoded_data))
