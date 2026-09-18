"""K8T M2.3 external bus/address decoder oracle."""

LOW_BASE,LOW_END=0x000000,0x00FFFF
SRAM_BASE,SRAM_END=0x010000,0x20FFFF
SRAM_EXP_BASE,SRAM_EXP_END=0x210000,0x40FFFF
VIDEO_BASE,VIDEO_END=0x800000,0x8FFFFF
ETH_BASE,ETH_END=0x900000,0x9FFFFF
STORAGE_BASE,STORAGE_END=0xA00000,0xAFFFFF
EXP_BASE,EXP_END=0xB00000,0xBFFFFF
IO_BASE,IO_END=0xE00000,0xEFFFFF
FLASH_BASE,FLASH_END=0xF80000,0xFFFFFF

STANDARD_SRAM_BYTES=2*1024*1024
MAX_ONBOARD_SRAM_BYTES=4*1024*1024
FLASH_BYTES=512*1024

REGIONS=(
 ("low",LOW_BASE,LOW_END),("sram",SRAM_BASE,SRAM_END),
 ("sram_expansion",SRAM_EXP_BASE,SRAM_EXP_END),("video",VIDEO_BASE,VIDEO_END),
 ("ethernet",ETH_BASE,ETH_END),("storage",STORAGE_BASE,STORAGE_END),
 ("expansion",EXP_BASE,EXP_END),("io",IO_BASE,IO_END),("flash",FLASH_BASE,FLASH_END),
)

def decode(addr):
    addr &= 0xffffff
    hits=[name for name,start,end in REGIONS if start <= addr <= end]
    if len(hits)>1:
        raise AssertionError("overlapping address decode")
    return hits[0] if hits else "open_bus"

def validate_map():
    previous_end=-1
    for _,start,end in sorted(REGIONS,key=lambda r:r[1]):
        if start <= previous_end: return False
        previous_end=end
    return True
