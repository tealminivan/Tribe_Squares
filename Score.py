class Score:

  def __init__(self, player_name):
    self.__name=player_name
    self.__score=0
    self.__multiplier=1
    self.__level=0
    self.__lives=3

  def add_points(self, amount):
    self.__score=self.__score+amount*self.__multiplier
    i=0
    loop=True
    if(0<=self.__score<=9999):
      self.__level=0
    else:
      while(loop):
        start=(2**i)*(10000)
        i=i+1
        bound=(2**i)*(10000)-1
        if(start<=self.__score<=bound):
          self.__level=2**(i-1)
          loop=False
   
  def subtract_points(self, amount):
    self.__multiplier=1
    self.__score=self.__score-amount
    i=0
    loop=True
    if(0<=self.__score<=9999):
      self.__level=0
    else:
      while(loop):
        start=(2**i)*(10000)
        i=i+1
        bound=(2**i)*(10000)-1
        if(start<=self.__score<=bound):
          self.__level=2**(i-1)
          loop=False

  def get_multiplier(self):
    return self.__multiplier

  def increment_multiplier(self):
    self.__multiplier=self.__multiplier+1

  def get_score(self):
    return self.__score

  def get_level(self):
    return self.__level
    

  def get_lives(self):
    return self.__lives

  def lose_life(self):
    self.__lives=self.__lives-1
    if(self.__lives<=0):
      self.__lives=0
      return False
    else:
      return True

  def gain_life(self):
    self.__lives=self.__lives+1

  def __str__(self):
    return "Player: "+self.__name+", Score: "+str(self.__score)+", Level: "+str(self.__level)+", Multiplier: "+str(self.__multiplier)+", Lives: "+str(self.__lives)
    

if __name__ == '__main__':
  bob=Score("BOB")  
  number=bob.get_score()
  print(number)
  print(bob.get_level())
  bob.add_points(10000)
  print(bob.get_score())
  print(bob.get_level())
  bob.subtract_points(1)
  print(bob.get_level())
  bob.increment_multiplier()
  print(bob.get_multiplier())
  bob.add_points(5000)
  print(bob.get_score())
  print(bob.get_level())
  bob.subtract_points(1)
  print(bob.get_score())
  print(bob.get_level())
  print(bob.get_multiplier())
  print(bob.__str__())
 
 
  