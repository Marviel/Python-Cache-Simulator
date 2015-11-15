# You will develop your cache simulator to operate as with the cache memory 
# we discussed in class and in your book. Your cache only needs to support reads. 
# We will test your code with the test cases you developed.
import math

# 1) What is block size in cache

# Returns cache address
def direct_mapped_hash_fnc(addr, num_blocks):
  return addr % num_blocks


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
    self.m = int(math.log(self.block_size, 2))
    self.n = int(math.log(self.num_blocks, 2)) #log base 2..
    self.tag_size = int(20 - (self.n + self.m))

    # The data in different forms:
      # Direct Assoc: {(tag, data)}
    self._store = {}

  #tag is the unique identifier for each entry
  #valid bit is set when we know the tag has good data (all false at startup, etc)


  # def read(self, addr):
    #Will choose which read function based on the current mode, then execute it


  # Given an address in memory, checks if the cache contains that data yet.
  # If it does not, stores the data in the cache.
  # Returns:
  #   If found, returns true
  #   If not, returns None
  def direct_mapped_read(self, addr):
    ret = self.direct_mapped_ping_cache(addr)

    #Add everything else in the block to the cache
    for i in range(self.block_size):
      self.direct_mapped_ping_cache(addr)

    return ret

  def direct_mapped_ping_cache(self, addr):
    cache_addr = direct_mapped_hash_fnc(addr, self.num_blocks)

    #Bit shift by tag_size bits to get tag
    tag = addr >> self.tag_size

    if cache_addr in self._store and self._store[cache_addr][0] == tag: # If we have it in the cache...
      return True
    else: # If we don't...
      #Data in cache doesn't matter in this implementation, so store addr for debugging
      self._store[cache_addr] = (tag,addr) 
      return False


  def print_data(self):
    print("block_size: %d"%(self.block_size))
    print("num_blocks: %d"%(self.num_blocks))
    print("m: %d"%(self.m))
    print("n: %d"%(self.n))
    print("tag_size: %d"%(self.tag_size))


# READ PARAMS
#(you may include default values and make these optional parameters for your
# program):
# -Block size (number of words. Note that we don’t differentiate in this project for
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

cache = Cache(1048,1, None, None, None, None)
print("-------CACHE DATA-------")
cache.print_data()
print("-------------------------")


# LOAD FILE
hit_cnt = 0
hit = False
instruction_cnt = 0
s = []
f = open("addresses.txt")
for line in f:
  addr = int(line, 0)
  s.append(addr)
  
  hit = cache.direct_mapped_read(addr)
  if hit:
    hit_cnt += 1 
    #print("dupe found at line: %d"%(instruction_cnt))

  # print(addr)
  # print("  " + str(hit))
  instruction_cnt += 1
  if instruction_cnt % 250 == 0: print("addresses loaded: %d"%(instruction_cnt))

min_diff = 100000000
max_diff = 0
last = 0
diff_cnt = 0
cnt = 0
for a in sorted(s):
  cnt += 1
  diff = a - last
  diff_cnt += diff
  if(diff < min_diff and diff != 0): min_diff = diff
  if(diff > max_diff): max_diff = diff
  last = a

avg_diff = 1.0*diff_cnt/(1.0*cnt)

print("min diff: %d"%(min_diff))
print("max diff: %d"%(max_diff))
print("avg diff: %f"%(avg_diff))
#print("testcount: %d"%(cache.testcount))

hit_rate = (1.0*hit_cnt)/(1.0*instruction_cnt)

print("TOTAL HITS: %d, TOTAL INSTRUCTIONS: %d"%(hit_cnt,instruction_cnt))
print("HIT RATIO: %f"%(hit_rate))


# Given this input and for the cache as
# parameterized at the command line, compute the hit/miss rate and the AMAT. 


# miss_rate = misses / instruction_cnt
# amat = hit_time + (miss_rate * miss_time)









