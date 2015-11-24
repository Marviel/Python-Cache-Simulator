# You will develop your cache simulator to operate as with the cache memory 
# we discussed in class and in your book. Your cache only needs to support reads. 
# We will test your code with the test cases you developed.

import math
import pprint
import sys
import random

args = ["[input_file]",
        "[block_size (int)]",
        "[num_blocks (int)]",
        "[associativity (0: direct, 1: set)]",
        "[hit_time (float)]",
        "[miss_time (float)]",
        "[replacement_policy (0: Random, 1: LRU)]"]

argstr = ""
for a in args:
  argstr += (" " + a)

if len(sys.argv) != len(args) + 1:
  print("USAGE: python3 cache_simulator.py" + argstr)
  sys.exit(0)

INPUT_FILE = sys.argv[1]
BLOCK_SIZE = int(sys.argv[2])
NUM_BLOCKS = int(sys.argv[3])
ASSOC = sys.argv[4] == "1"
HIT_TIME = float(sys.argv[5])
MISS_TIME = float(sys.argv[6])
REPLACEMENT = bool(sys.argv[7])
COLL_SIZE = 2 # set associativity number? N?
# -Block size (number of words. Note that we don't differentiate in this project for
# words and bytes. You can assume all addresses are referring to words, and no
# further byte-word conversion is needed).
# -Number of lines/blocks in the cache.
# -Associativity (1 for direct, 2 for two-way set associative, etc.)
# -Hit time (in cycles)
# -Miss time (in cycles)
# -Replacement policy: Random and LRU

PP = pprint.PrettyPrinter(indent=4)


#BLOCK_SIZE Only used by me to calculate tag_size
# BLOCK_SIZE = 16 #In Words/Bytes (synonymous here) 
# NUM_BLOCKS = 256 #In blocks :)
ADDR_SIZE = 20

# Returns cache address
def direct_mapped_hash_fnc(addr, num_blocks):
  return addr % num_blocks



#Prints out data about an array of numbers.
def print_bookkeeping(nums):
  #Bookkeeping Variables
  min_diff = 100000000
  max_diff = 0
  last = 0
  diff_cnt = 0
  cnt = 0
  min_addr = 1000000000
  max_addr = 0
  for a in sorted(nums):
    if(a < min_addr): min_addr = a
    if(a > max_addr): max_addr = a
    diff = a - last
    diff_cnt += diff
    if(diff < min_diff and diff != 0): min_diff = diff
    if(diff > max_diff): max_diff = diff
    last = a
    cnt += 1

  avg_diff = 1.0*diff_cnt/(1.0*cnt)

  print("min diff: %d"%(min_diff))
  print("max diff: %d"%(max_diff))
  print("avg diff: %f"%(avg_diff))
  print("min addr: %d"%(min_addr))
  print("max addr: %d"%(max_addr))


class DirectMappedCache(object):
  #Contains array
  #[(index, v, tag, data)]
  def __init__(self, block_size, num_blocks, hit_time, 
                miss_time, replacement_policy):

    # self.num_blocks = block_size * num_blocks #sorry. hackish...
    # self.block_size = 1
    self.block_size = block_size
    self.num_blocks = num_blocks #cache size
    self.hit_time = hit_time
    self.miss_time = miss_time
    self.replacement_policy = replacement_policy


    #Calculations
    self.m = int(math.log(self.block_size, 2)) #num Bits for offset
    self.n = int(math.log(self.num_blocks, 2)) #num Index Bits
    self.tag_size = self.get_tag_size() #num Tag bits

    
    self._blocks = {} # {block_index: [tag, data1, data2, ...]}

  def get_tag_size(self):
    #       ...........(offset bits + index bits)
    return ADDR_SIZE - (self.m + self.n) #I used to do this, but it didn't work.

  def get_tag_index(self, addr):
    mask_str = '1'*self.tag_size + '0'*self.n + '0'*self.m
    mask = int(mask_str,2)
    return mask & addr

  def get_block_index(self, addr):
    mask_str = '0'*self.tag_size + '1'*self.n + '0'*self.m
    mask = int(mask_str,2)
    #print("tag_size: %d, n: %d, m: %d ---> mask_str: %s"%(self.tag_size, self.n, self.m, mask_str))
    return mask & addr

  def get_offset_index(self, addr):
    mask_str = '0'*self.tag_size + '0'*self.n + '1'*self.m
    mask = int(mask_str,2)
    return mask & addr

  # Given an address in memory, checks if the cache contains that data yet.
  # If it does not, stores the data in the cache.
  # Returns:
  #   If found, returns true
  #   If not, returns None
  def read(self, addr):
    ret = self.ping_cache(addr)

    return ret

  def ping_cache(self, addr):
    block_index = self.get_block_index(addr)

    shift = self.n + self.m
    tag = addr >> shift

    if block_index in self._blocks and self._blocks[block_index][0] == tag: # If we have it in the cache...
      return True
    else: # If we don't...
      #Data in cache doesn't matter in this implementation, so store addr for debugging
      arr = []
      for i in range(self.block_size): #this part isn't perfect yet.
        arr = [addr + i*8]
      self._blocks[block_index] = [tag] + arr
      return False

  def print_stats(self):
    print("block_size: %d"%(self.block_size))
    print("num_blocks: %d"%(self.num_blocks))
    print("m: %d"%(self.m))
    print("n: %d"%(self.n))
    print("tag_size: %d"%(self.tag_size))

  def print_contents(self):
    # PP.pprint(self._store)
    for k in self._blocks.keys():
      print("%d:%d"%(k,self._blocks[k][1]))


class SetAssociativeCache(object):
  #Contains array
  #[(index, v, tag, data)]
  def __init__(self, block_size, num_blocks, hit_time, 
                miss_time, replacement_policy):

    # self.num_blocks = block_size * num_blocks #sorry. hackish...
    # self.block_size = 1
    self.block_size = block_size
    self.num_blocks = num_blocks #cache size
    self.hit_time = hit_time
    self.miss_time = miss_time
    self.replacement_policy = replacement_policy


    #Calculations
    self.m = int(math.log(self.block_size, 2)) #num Bits for offset
    self.n = int(math.log(self.num_blocks, 2)) #num Index Bits
    self.tag_size = self.get_tag_size() #num Tag bits

    
    self._blocks = {} # {block_index: [[tag, data1, data2, ...]]}

  #tag is the unique identifier for each entry
  #TODO valid bit is set when we know the tag has good data (all false at startup, etc)

  # def read(self, addr):
    #Will choose which read function based on the current mode, then execute it

  def get_tag_size(self):
    #       ...........(offset bits + index bits)
    return ADDR_SIZE - (self.m + self.n) #I used to do this, but it didn't work.

  def get_tag_index(self, addr):
    mask_str = '1'*self.tag_size + '0'*self.n + '0'*self.m
    mask = int(mask_str,2)
    return mask & addr

  def get_block_index(self, addr):
    mask_str = '0'*self.tag_size + '1'*self.n + '0'*self.m
    mask = int(mask_str,2)
    return mask & addr

  def get_offset_index(self, addr):
    mask_str = '0'*self.tag_size + '0'*self.n + '1'*self.m
    mask = int(mask_str,2)
    return mask & addr

  # Given an address in memory, checks if the cache contains that data yet.
  # If it does not, stores the data in the cache.
  # Returns:
  #   If found, returns true
  #   If not, returns None
  def read(self, addr):
    ret = self.ping_cache(addr)
    return ret

  def ping_cache(self, addr):
    block_index = self.get_block_index(addr)

    shift = self.n + self.m
    tag = addr >> shift

    if block_index in self._blocks:
      for slot in self._blocks[block_index]:
        if slot[0] == tag:
          # If we have it in the cache...
          return True

      # If we got here, we don't have this entry. So, we add it.
      self.write_slot(block_index, tag, addr)
      return False # We don't have it, then.

    else: # If we don't have anything....
      #Data in cache doesn't matter in this implementation, so store addr for debugging
      arr = []

      for i in range(COLL_SIZE):
        slot = []
        slot = [-1 for x in range(self.block_size + 1)]
        arr.append(slot)

      #print(arr)
      
      self._blocks[block_index] = arr
      self.write_slot(block_index,tag,addr)
      return False

  def write_slot(self, block_index, tag, addr):
    slot_to_overwrite = random.randint(0,COLL_SIZE - 1)
    arr = []
    for i in range(self.block_size):
      arr = [addr + i*8]
    self._blocks[block_index][slot_to_overwrite] = [tag] + arr

  def print_stats(self):
    print("block_size: %d"%(self.block_size))
    print("num_blocks: %d"%(self.num_blocks))
    print("m: %d"%(self.m))
    print("n: %d"%(self.n))
    print("tag_size: %d"%(self.tag_size))

  def print_contents(self):
    # PP.pprint(self._store)
    for k in self._blocks.keys():
      print("%d:%d"%(k,self._blocks[k][1]))




#-----------BEGIN SCRIPT----------------------------------------
#---------------------------------------------------------------
if ASSOC:
  print("Associative")
  cache = SetAssociativeCache(BLOCK_SIZE,NUM_BLOCKS, None, None, None)
else:
  print("Direct")
  cache = DirectMappedCache(BLOCK_SIZE,NUM_BLOCKS, None, None, None)


print("-------STARTING CACHE STATS-------")
cache.print_stats()
print("Associative: %d"%(ASSOC))
print("-------------------------")


print("--------HITS/MISS LOG--------")
# LOAD FILE
hit_cnt = 0
hit = False
instruction_cnt = 0
s = []
f = open(INPUT_FILE)
for line in f:
  addr = int(line, 0)
  s.append(addr)
  
  hit = cache.read(addr)
  if hit:
    hit_cnt += 1 
    print("%d hit!"%(addr))
  else:
    print("%d miss"%(addr))

  instruction_cnt += 1
  if instruction_cnt % 250 == 0: print("addresses loaded: %d"%(instruction_cnt))
print("------------------------------")




if not ASSOC:
  print("--------CACHE CONTENTS------")
  cache.print_contents()
  print("----------------------------")


# Calculate statistics and exit.
hit_rate = (1.0*hit_cnt)/(1.0*instruction_cnt)
miss_cnt = instruction_cnt - hit_cnt
miss_rate = (1.0*miss_cnt)/(1.0*instruction_cnt)
amat = HIT_TIME + (miss_rate * MISS_TIME)
print("TOTAL HITS: %d, TOTAL INSTRUCTIONS: %d"%(hit_cnt,instruction_cnt))
print("HIT RATIO: %f"%(hit_rate))
print("AMAT: %f"%(amat))

# print("-------ENDING CACHE STATS-------")
# cache.print_stats()
# print("-------------------------")



