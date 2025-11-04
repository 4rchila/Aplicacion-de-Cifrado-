class FNV1Hash:
    
    FNV_32_OFFSET = 2166136261
    FNV_32_PRIME = 16777619
    
    FNV_64_OFFSET = 14695981039346656037
    FNV_64_PRIME = 1099511628211
    
    @staticmethod
    def fnv1(data, bits=32):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if bits == 32:
            offset = FNV1Hash.FNV_32_OFFSET
            prime = FNV1Hash.FNV_32_PRIME
            mask = 0xFFFFFFFF
        elif bits == 64:
            offset = FNV1Hash.FNV_64_OFFSET
            prime = FNV1Hash.FNV_64_PRIME
            mask = 0xFFFFFFFFFFFFFFFF
        else:
            raise ValueError("Bits debe ser 32 o 64")
        
        hash_value = offset
        
        for byte in data:
            hash_value = (hash_value * prime) & mask
            hash_value ^= byte
        
        return hash_value
    
    @staticmethod
    def fnv1a(data, bits=32):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if bits == 32:
            offset = FNV1Hash.FNV_32_OFFSET
            prime = FNV1Hash.FNV_32_PRIME
            mask = 0xFFFFFFFF
        elif bits == 64:
            offset = FNV1Hash.FNV_64_OFFSET
            prime = FNV1Hash.FNV_64_PRIME
            mask = 0xFFFFFFFFFFFFFFFF
        else:
            raise ValueError("Bits debe ser 32 o 64")
        
        hash_value = offset
        
        for byte in data:
            hash_value ^= byte
            hash_value = (hash_value * prime) & mask
        
        return hash_value
    
    @staticmethod
    def fnv1_hex(data, bits=32):
        hash_value = FNV1Hash.fnv1(data, bits)
        return hex(hash_value)
    
    @staticmethod
    def fnv1a_hex(data, bits=32):
        hash_value = FNV1Hash.fnv1a(data, bits)
        return hex(hash_value)
    
    @staticmethod
    def fnv1_bytes(data, bits=32):
        hash_value = FNV1Hash.fnv1(data, bits)
        return hash_value.to_bytes(bits // 8, byteorder='big')
    
    @staticmethod
    def fnv1a_bytes(data, bits=32):
        hash_value = FNV1Hash.fnv1a(data, bits)
        return hash_value.to_bytes(bits // 8, byteorder='big')