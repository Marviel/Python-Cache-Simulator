# You will develop your cache simulator to operate as with the cache memory 
# we discussed in class and in your book. Your cache only needs to support reads. 
# We will test your code with the test cases you developed.

#TODO
# - Modes
# - Read from command line
# - Associative

import math
import pprint

PP = pprint.PrettyPrinter(indent=4)


#BLOCK_SIZE Only used by me to calculate tag_size
BLOCK_SIZE = 1 #In Words/Bytes (synonymous here) 
NUM_BLOCKS = 16 #In blocks :)
ADDR_SIZE = 20

# Returns cache address
def direct_mapped_hash_fnc(addr, num_blocks):
  return addr % num_blocks

def get_tag_size(offset,index):
  #return ADDR_SIZE - (offset + index) I used to do this, but it didn't work.
  return ADDR_SIZE - index

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


class Cache(object):
  #Contains array
  #[(index, v, tag, data)]
  def __init__(self, block_size, num_blocks, associativity, hit_time, 
                miss_time, replacement_policy):

    self.block_size = block_size
    self.num_blocks = num_blocks #cache size
    self.associativity = associativity
    self.hit_time = hit_time
    self.miss_time = miss_time
    self.replacement_policy = replacement_policy

    #Calculations
    self.m = int(math.log(self.block_size, 2)) #num Bits for offset
    self.n = int(math.log(self.num_blocks, 2)) #num Index Bits
    self.tag_size = get_tag_size(self.m, self.n) #num Tag bits

    # The data in different forms:
      # Direct Assoc: {(tag, data)}
    self._store = {}

  #tag is the unique identifier for each entry
  #TODO valid bit is set when we know the tag has good data (all false at startup, etc)

  # def read(self, addr):
    #Will choose which read function based on the current mode, then execute it


  # Given an address in memory, checks if the cache contains that data yet.
  # If it does not, stores the data in the cache.
  # Returns:
  #   If found, returns true
  #   If not, returns None
  def direct_mapped_read(self, addr):
    ret = self.direct_mapped_ping_cache(addr)

    return ret

  def direct_mapped_ping_cache(self, addr):
    cache_addr = direct_mapped_hash_fnc(addr, self.num_blocks)

    #Bit shift by (ADDR_SIZE - tag_size) bits to get tag
    shift = self.n
    tag = addr >> shift
    # print("addr: %d gives tag: %d (shift %d)"%(addr,tag, shift))

    if cache_addr in self._store and self._store[cache_addr][0] == tag: # If we have it in the cache...
      return True
    else: # If we don't...
      #Data in cache doesn't matter in this implementation, so store addr for debugging
      self._store[cache_addr] = (tag,addr) 
      return False

  def print_stats(self):
    print("block_size: %d"%(self.block_size))
    print("num_blocks: %d"%(self.num_blocks))
    print("m: %d"%(self.m))
    print("n: %d"%(self.n))
    print("tag_size: %d"%(self.tag_size))

  def print_contents(self):
    # PP.pprint(self._store)
    for k in self._store.keys():
      print("%d:%d"%(k,self._store[k][1]))


# READ PARAMS
#(you may include default values and make these optional parameters for your
# program):
# -Block size (number of words. Note that we don't differentiate in this project for
# words and bytes. You can assume all addresses are referring to words, and no
# further byte-word conversion is needed).
# -Number of lines/blocks in the cache.
# -Associativity (1 for direct, 2 for two-way set associative, etc.)
# -Hit time (in cycles)
# -Miss time (in cycles)
# -Replacement policy: Random and LRU



# Your program will be given a series of addresses (from an ASCII file that contains hex
# addresses with one address per line). One such file is provided to you, available in the
# assignment section of the blackboard system.

cache = Cache(BLOCK_SIZE,NUM_BLOCKS, None, None, None, None)
print("-------STARTING CACHE STATS-------")
cache.print_stats()
print("-------------------------")


print("--------HITS/MISS LOG--------")
# LOAD FILE
hit_cnt = 0
hit = False
instruction_cnt = 0
s = []
f = open("test_addresses.txt")
for line in f:
  addr = int(line, 0)
  s.append(addr)
  
  hit = cache.direct_mapped_read(addr)
  if hit:
    hit_cnt += 1 
    print("%d hit!"%(addr))
  else:
    print("%d miss"%(addr))

  # print(addr)
  # print("  " + str(hit))
  instruction_cnt += 1
  if instruction_cnt % 250 == 0: print("addresses loaded: %d"%(instruction_cnt))
print("------------------------------")

# print("BOOKKEEPING--------")
# print_bookkeeping(s)
# print("--------------------")

hit_rate = (1.0*hit_cnt)/(1.0*instruction_cnt)

print("--------CACHE CONTENTS------")
cache.print_contents()
print("----------------------------")

print("TOTAL HITS: %d, TOTAL INSTRUCTIONS: %d"%(hit_cnt,instruction_cnt))
print("HIT RATIO: %f"%(hit_rate))

print("-------ENDING CACHE STATS-------")
cache.print_stats()
print("-------------------------")


# Given this input and for the cache as
# parameterized at the command line, compute the hit/miss rate and the AMAT. 


# miss_rate = misses / instruction_cnt
# amat = hit_time + (miss_rate * miss_time)


