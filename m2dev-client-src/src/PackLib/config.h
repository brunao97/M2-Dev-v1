#pragma once
#include <cstdint>
#include <array>
#include <vector>
#include <string>
#include <memory>
#include <unordered_map>

#include <gcm.h>
#include <modes.h>
#include <osrng.h>
#include <secblock.h>
#include <camellia.h>

constexpr std::array<uint8_t, 32> PACK_KEY = {
	0x00,0x11,0x22,0x33, 0x44,0x55,0x66,0x77,
	0x88,0x99,0xAA,0xBB, 0xCC,0xDD,0xEE,0xFF,
	0x01,0x23,0x45,0x67, 0x89,0xAB,0xCD,0xEF,
	0xFE,0xDC,0xBA,0x98, 0x76,0x54,0x32,0x10
};

#pragma pack(push, 1)
struct TPackFileHeader
{
	uint64_t	entry_num;
	uint64_t	data_begin;
	uint8_t     iv[CryptoPP::Camellia::BLOCKSIZE];
};
struct TPackFileEntry
{
	char		file_name[FILENAME_MAX+1];
	uint64_t	offset;
	uint64_t	file_size;
	uint64_t	compressed_size;
	uint8_t		encryption;
	uint8_t     iv[CryptoPP::Camellia::BLOCKSIZE];
};
#pragma pack(pop)

class CPack;
using TPackFile = std::vector<uint8_t>;
using TPackFileMapEntry = std::pair<std::shared_ptr<CPack>, TPackFileEntry>;
using TPackFileMap = std::unordered_map<std::string, TPackFileMapEntry>;