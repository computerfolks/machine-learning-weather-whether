import math
import random

#get training file path
training_file = 'hw1.train.col'
training_file_path = "/Users/jacobweissman/Desktop/381m project" + "/" + training_file

#get test file path
test_file = 'hw1.test.col'
test_file_path = "/Users/jacobweissman/Desktop/381m project" + "/" + test_file

#SELECT MAX DEPTH
max_depth = 3

#SELECT % OF TRAINING DATA TO USE
choose_trial_percentage = 100

#set global variable of list of weather-related words
weather_related_words = ['rain', 'sun', 'summer', 'season', 'winter', 'spring', 'forecast', 'storm', 'snow', 'temperature', 'forecast', 'flood', 'inches', 'extreme', 'climate', 'natural', 'cold', 'hot', 'moisture', 'humid']

#set global variable of list of words that commonly follow "whether" (based on most used words in English)
whether_followed_words = ['the', 'a', 'to', 'in', 'you', 'that', 'it', 'he', 'was', 'for', 'on', 'as', 'with', 'his', 'they', 'I', 'at', 'this', 'from', 'all', 'we', 'your']

#get all of the lines of the file into a list of strings
with open(training_file_path) as f:
  lines = f.readlines()

#set % of training data to be used
trial_size = int((choose_trial_percentage / 100) * len(lines))

#randomly shuffle the lines
random.shuffle(lines)

#set lines to only be viewed up to the trial size
lines = lines[:trial_size]


class Node:
  """
  Node class which will serve as a node on the decision tree
  """
  def __init__(self, basis, entropy, leftweather, leftwhether, rightweather, rightwhether, currentdepth, maxdepth):
    #left is negative/no
    #right is positive/yes
    
    #basis is the binary decision being made at the current node 
    #possible values for basis:  #weather_related, article_before, article_after, or_after, or_not_together, or_anywhere, whether_followed
    self.basis = basis
    
    #entropy at the current node
    self.entropy = entropy

    #number of words that are "weather" to the left / negative
    self.leftweather = leftweather
    self.leftwhether = leftwhether
    self.rightweather = rightweather
    self.rightwhether = rightwhether
    
    #keep track of current depth and maxdepth
    self.currentdepth = currentdepth
    self.maxdepth = maxdepth
  
  def decision(self, decision_dictionary):
    """
    call on this function when a test sentence is given and a prediction must be made
    """
    if self.basis is not None:
      #determine if tree should traverse to the left or the right based on if the property was found to be true in the test example
      direction_decision = decision_dictionary[self.basis]
      #print(f'current depth: {self.currentdepth} decision basis: {self.basis} decision: {direction_decision}')
    else:
      # irrelevant what I set this to, this will only occur when no basis was set because the data at the node was all weather or all whether. in this case, entropy will be = 0
      direction_decision = True
    #if we are at the bottom and a decision must be made, or entropy is 0 so the decision is obvious
    if self.currentdepth == self.maxdepth or self.entropy == 0:
      if direction_decision == True:
        #print(f'right weather: {self.rightweather} right whether: {self.rightwhether}')
        if self.rightweather > self.rightwhether:
          return "weather"
        else:
          return "whether"
      else:
        #print(f'left weather: {self.leftweather} left whether: {self.leftwhether}')
        if self.leftweather > self.leftwhether:
          return "weather"
        else:
          return "whether"
    #if not at max depth, call the correct subtree
    else:
      #if the property was found, traverse right / positive
      if direction_decision == True:
        return self.right.decision(decision_dictionary)
      else:
        return self.left.decision(decision_dictionary)

  def setleftnode(self, left):
    self.left = left

  def setrightnode(self, right):
    self.right = right

def check_for_list_of_words(line, check_words):
  """
  function to check if any word in a list of words is a substring of any word in a sentence
  """
  for word in line:
    for check_word in check_words:
      if check_word in word:
        return 1
  return 0

def check_for_two_consecutive_words(line, word1, word2):
  """
  check if two words appear consecutively in a sentence
  """
  for word_index in range(len(line)):
    if line[word_index] == word2 and line[word_index - 1] == word1:
      return 1
  return 0

def word_equal_check(word1, word2):
  """
  check if two words are the same
  """
  if word1 == word2:
    return 1
  else:
    return 0

def check_word_appear_in_sentence(line, word):
  """
  check if a word appears in a sentence
  """
  for check_word in line:
    if check_word == word:
      return 1
  return 0

def get_sentence():
  """
  this function gets a sentence from the user and validates it before returning
  """
  sentence_accepted = False
  while (sentence_accepted == False):
    user_input = input("Enter a sentence which includes the word 'weather' or the word 'whether', but for one occurence of weather/whether, instead of the word weather/whether, type 'XXX'. The machine will predict which word is correct in context (for example: 'I don't know XXX or not to go to the party'): ").lower()
    sentence = user_input.split()
    #track the number of occurences of xxx
    occurences = 0
    for word_index in range(len(sentence)):
      if sentence[word_index] == "xxx":
        index = word_index
        insert_word = "xxx"
        occurences += 1
    if occurences != 1:
      print("The sentence must contain ONE AND ONLY ONE instance of XXX - try again.")
    else:
      sentence_accepted = True

  #format the sentence
  user_input = insert_word + " " + str(index) + " " + user_input
  return user_input

def line_filter(line, index, weather_related_filter, weather_related_return_including, article_before_filter, article_before_return_including, article_after_filter, article_after_return_including, or_after_filter, or_after_return_including, or_not_together_filter, or_not_together_return_including, or_anywhere_filter, or_anywhere_return_including, whether_followed_filter, whether_followed_return_including):
  """
  this function takes in a sentence and checks it against "filters"
  for example, if we are building a tree using training data, and we have already determined that the root node would be if "or not" appears in the sentence
  we now need to build the left side of the tree (the cases where the words "or not" do not appear), and the right side of the tree
  to build these sides, we must "filter" the data so we only view negative cases when building the left side, and positive cases when building the right side
  this function will filter out sentences based on whether the filter is toggled on and the sentence has the correct truth value for the given property that we are currently examining
  only if it passes all active filters will the sentence be returned
  at the start of the program, all filters are set to false/inactive
  the root node is built and toggles on the correct filter, etc
  note that the root node's left filter and right filter do NOT have to be the same
  """
  #weather words filter
  global weather_related_words
  weather_found = check_for_list_of_words(line, weather_related_words)
  #if the filter is on
  weather_related_approve = approve(weather_related_filter, weather_found, weather_related_return_including)
  if not weather_related_approve:
    return False

  #article_before filter
  try:
    prev_word = line[index + 1]
    prev_word_the = word_equal_check("the", prev_word)
    prev_word_a = word_equal_check("a", prev_word)
    prev_word_article = prev_word_the + prev_word_a
    article_before_approve = approve(article_before_filter, prev_word_article, article_before_return_including)
    if not article_before_approve:
      return False
  except:
    pass


  #article_after filter
  try:
    next_word = line[index + 3]
    next_word_the = word_equal_check("the", next_word)
    next_word_a = word_equal_check("a", next_word)
    next_word_article = next_word_the + next_word_a
    article_after_approve = approve(article_after_filter, next_word_article, article_after_return_including)
    if not article_after_approve:
      return False
  except:
    pass


  #or_after filter
  try:
    next_word = line[index + 3]
    next_word_or = word_equal_check("or", next_word)
    or_after_approve = approve(or_after_filter, next_word_or, or_after_return_including)
    if not or_after_approve:
      return False
  except:
    pass

  #or not together filter
  or_not_together = check_for_two_consecutive_words(line[2:], "or", "not")
  or_not_together_approve = approve(or_not_together_filter, or_not_together, or_not_together_return_including)
  if not or_not_together_approve:
    return False

  #or anywhere filter
  or_anywhere = check_word_appear_in_sentence(line, "or")
  or_anywhere_approve = approve(or_anywhere_filter, or_anywhere, or_anywhere_return_including)
  if not or_anywhere_approve:
    return False

  #whether followed
  global whether_followed_words
  try:
    next_word = line[index + 3]
    whether_followed = (next_word in whether_followed_words)
    whether_followed_approve = approve(whether_followed_filter, whether_followed, whether_followed_return_including)
    if not whether_followed_approve:
      return False
  except:
    pass
  #if the sentence passes all active filters
  return True

def approve(filter_bool, found_bool, return_bool):
  """
  this function takes in the boolean value of the filter being active/inactive,
  the actual result of if the property is positive/negative, 
  and the desired result of the property being positive/negative
  it returns True if the filter is inactive or the desired and actual properties have the same truth value
  otherwise, it returns False
  """
  if (filter_bool):
    if found_bool and (not return_bool):
      return False
    if (not found_bool) and return_bool:
      return False
  return True

def entropy(positive_values, negative_values):
  """
  this function calculates the total entropy given a number of positive and number of negative values
  """
  total_values = positive_values + negative_values
  if positive_values == 0:
    piece1 = 0
  else:
    piece1= -(positive_values / total_values) * math.log2(positive_values/total_values)
  if negative_values == 0:
    piece2 = 0
  else:
    piece2= -(negative_values / total_values) * math.log2(negative_values/total_values)
  return piece1 + piece2

def weighted_entropy(positive_values_one, positive_values_two, negative_values_one, negative_values_two):
  """
  this function computes the entropy of positive/negative values split across an additional function
  """
  positive_count = positive_values_one + positive_values_two
  negative_count = negative_values_one + negative_values_two
  total_count = positive_count + negative_count
  entropy_positive = entropy(positive_values_one, positive_values_two) * (positive_count / total_count)
  entropy_negative = entropy(negative_values_one, negative_values_two) * (negative_count / total_count)
  return entropy_positive + entropy_negative

def tree_builder(weather_related_filter, weather_related_return_including, article_before_filter, article_before_return_including, article_after_filter, article_after_return_including, or_after_filter, or_after_return_including, or_not_together_filter, or_not_together_return_including, or_anywhere_filter, or_anywhere_return_including, whether_followed_filter, whether_followed_return_including, current_depth, max_depth):
  """
  this function takes in the filter property (active/inactive) for each attribute, and the desired return value for the attribute (relevant only if the filter is active)
  it is called recursively and also takes in the current depth and maximum depth
  it's job is to build the next node in the tree
  """
  #counting stats, split across how many times each occurs for sentences with the word "weather", and how many times each occurs for sentences with the word "whether"
  #total number of how many times each word appears
  whether = 0
  weather = 0

  #how many times an article (the/a) appears immediately before the target word
  article_before_whether = 0
  #same for weather
  article_before_weather = 0

  #how many times an article (the/a) appears immediately after the target word
  article_after_whether = 0
  article_after_weather = 0

  #how many times the word "or" appears immediately after the target word
  or_after_whether = 0
  or_after_weather = 0

  #if the phrase "or not" is found in the sentence
  or_not_whether = 0
  or_not_weather = 0

  #if a weather related word is found anywhere in the sentence
  weather_related_weather = 0
  weather_related_whether = 0

  #if the word "or" is found anywhere in the sentence
  or_anywhere_weather = 0
  or_anywhere_whether = 0

  #if the target word is followed by a common English word which grammatically fits for the word "whether"
  whether_followed_weather = 0
  whether_followed_whether = 0

  #set the left and right branch to the current return values
  #the only set of right/lefts that will change will be the ones corresponding to the new basis,
  #in which case we will toggle right to positive and left to negative
  #this will ensure that the line_filter function properly filters and only allows to pass through the positive examples for the right side of the tree, and negative for the left
  weather_related_return_including_right = weather_related_return_including
  weather_related_return_including_left = weather_related_return_including
  
  article_before_return_including_right = article_before_return_including
  article_before_return_including_left = article_before_return_including

  article_after_return_including_right = article_after_return_including
  article_after_return_including_left = article_after_return_including

  or_after_return_including_right = or_after_return_including
  or_after_return_including_left = or_after_return_including

  or_not_together_return_including_right = or_not_together_return_including
  or_not_together_return_including_left = or_not_together_return_including

  or_anywhere_return_including_right = or_anywhere_return_including
  or_anywhere_return_including_left = or_anywhere_return_including

  whether_followed_return_including_right = whether_followed_return_including
  whether_followed_return_including_left = whether_followed_return_including


  for line in lines:
    current_line = line.split()
    #the first item in the list will be the target word
    current_word = current_line[0]
    #the second item will be the index of the target word
    current_index = int(current_line[1])
    examine = line_filter(current_line, current_index, weather_related_filter, weather_related_return_including, article_before_filter, article_before_return_including, article_after_filter, article_after_return_including, or_after_filter, or_after_return_including, or_not_together_filter, or_not_together_return_including, or_anywhere_filter, or_anywhere_return_including, whether_followed_filter, whether_followed_return_including)
    if not examine:
      #if it does not pass the filter, skip it
      continue
    if current_word == "weather":
      weather += 1
    else:
      whether += 1

    #only run this if the weather_related_filter is not toggled on
    #if it is, there is no point in running it: we are either looking at
    #all positive cases or all negative cases
    #either way, the information is useless so we should save the runtime
    if not weather_related_filter:
      #check for weather related words
      weather_found = check_for_list_of_words(current_line, weather_related_words)
      if current_word == "weather":
        weather_related_weather += weather_found
      else:
        weather_related_whether += weather_found

    #check previous word
    try:
      prev_word = current_line[current_index + 1]
      if not article_before_filter:
        prev_word_the = word_equal_check("the", prev_word)
        prev_word_a = word_equal_check("a", prev_word)
        prev_word_article = prev_word_the + prev_word_a
        if current_word == "weather":
          article_before_weather += prev_word_article
        else:
          article_before_whether += prev_word_article

    except:
      # print(line)
      pass

    #check next word
    try:
      next_word = current_line[current_index + 3]

      if not article_after_filter:
        next_word_the = word_equal_check("the", next_word)
        next_word_a = word_equal_check("a", next_word)
        next_word_article = next_word_the + next_word_a
        if current_word == "weather":
          article_after_weather += next_word_article
        else:
          article_after_whether += next_word_article

      if not or_after_filter: 
        next_word_or = word_equal_check("or", next_word)
        if current_word == "weather":
          or_after_weather += next_word_or
        else:
          or_after_whether += next_word_or
      
      if not whether_followed_filter:
        whether_followed = (next_word in whether_followed_words)
        if current_word == "weather":
          whether_followed_weather += whether_followed
        else:
          whether_followed_whether += whether_followed

    except:
      # print(line)
      pass
      
    #check for the phrase "or not"
    if not or_not_together_filter:
      or_not_together = check_for_two_consecutive_words(current_line[2:], "or", "not")
      if current_word == "weather":
        or_not_weather += or_not_together
      else:
        or_not_whether += or_not_together

    if not or_anywhere_filter:
      or_anywhere = check_word_appear_in_sentence(current_line, "or")
      if current_word == "weather":
        or_anywhere_weather += or_anywhere
      else:
        or_anywhere_whether += or_anywhere

  # print(f'Weather total: {weather}\nWhether total: {whether}\n')
  system_entropy = entropy(weather, whether)
  # print(f'total entropy: {system_entropy}\n\n')
  # the keys to these dictionaries will be the possible bases for the new decision node
  information_gain_dictionary = {}
  entropy_dictionary = {}

  #how many times was a property positive for each target word
  yes_weather_dictionary = {}
  yes_whether_dictionary = {}
  
  #how many times was a property negative for each target word
  no_weather_dictionary = {}
  no_whether_dictionary = {}

  if not weather_related_filter:
    no_weather_related_weather = weather - weather_related_weather
    no_weather_related_whether = whether - weather_related_whether
    weather_related_entropy_total = weighted_entropy(weather_related_weather, weather_related_whether, no_weather_related_weather, no_weather_related_whether)
    weather_related_information_gain = system_entropy - weather_related_entropy_total
    information_gain_dictionary['weather_related'] = weather_related_information_gain
    entropy_dictionary['weather_related'] = weather_related_entropy_total
    yes_weather_dictionary['weather_related'] = weather_related_weather
    yes_whether_dictionary['weather_related'] = weather_related_whether
    no_weather_dictionary['weather_related'] = no_weather_related_weather
    no_whether_dictionary['weather_related'] = no_weather_related_whether

    # print("IS THERE A WEATHER RELATED WORD?")
    # print(f'No Weather: {no_weather_related_weather}\nYes Weather: {weather_related_weather}\nNo Whether: {no_weather_related_whether}\nYes Whether: {weather_related_whether}\n')
    # print(f'total entropy:  {weather_related_entropy_total}')
    # print(f'information gain: {weather_related_information_gain}\n\n\n')

  if not article_before_filter:
    
    no_article_before_weather = weather - article_before_weather
    no_article_before_whether = whether - article_before_whether
    article_before_entropy_total = weighted_entropy(article_before_weather, article_before_whether, no_article_before_weather, no_article_before_whether)
    article_before_information_gain = system_entropy - article_before_entropy_total
    information_gain_dictionary['article_before'] = article_before_information_gain
    entropy_dictionary['article_before'] = article_before_entropy_total
    yes_weather_dictionary['article_before'] = article_before_weather
    yes_whether_dictionary['article_before'] = article_before_whether
    no_weather_dictionary['article_before'] = no_article_before_weather
    no_whether_dictionary['article_before'] = no_article_before_whether
    
    # print("IS THERE AN ARTICLE (THE/A) IMMEDIATELY BEFORE?")
    # print(f'No Weather: {no_article_before_weather}\nYes Weather: {article_before_weather}\nNo Whether: {no_article_before_whether}\nYes Whether: {article_before_whether}\n')
    # print(f'total entropy:  {article_before_entropy_total}')
    # print(f'information gain: {article_before_information_gain}\n\n\n')


  if not article_after_filter:
    no_article_after_weather = weather - article_after_weather
    no_article_after_whether = whether - article_after_whether
    article_after_entropy_total = weighted_entropy(article_after_weather, article_after_whether, no_article_after_weather, no_article_after_whether)
    article_after_information_gain = system_entropy - article_after_entropy_total
    information_gain_dictionary['article_after'] = article_after_information_gain
    entropy_dictionary['article_after'] = article_after_entropy_total
    yes_weather_dictionary['article_after'] = article_after_weather
    yes_whether_dictionary['article_after'] = article_after_whether
    no_weather_dictionary['article_after'] = no_article_after_weather
    no_whether_dictionary['article_after'] = no_article_after_whether

    # print("IS THERE AN ARTICLE (THE/A) IMMEDIATELY AFTER?")
    # print(f'No Weather: {no_article_after_weather}\nYes Weather: {article_after_weather}\nNo Whether: {no_article_after_whether}\nYes Whether: {article_after_whether}\n')
    # print(f'total entropy:  {article_after_entropy_total}')
    # print(f'information gain: {article_after_information_gain}\n\n\n')

  if not or_after_filter:
    no_or_after_weather = weather - or_after_weather
    no_or_after_whether = whether - or_after_whether
    or_after_entropy_total = weighted_entropy(or_after_weather, or_after_whether, no_or_after_weather, no_or_after_whether)
    or_after_information_gain = system_entropy - or_after_entropy_total
    information_gain_dictionary['or_after'] = or_after_information_gain
    entropy_dictionary['or_after'] = or_after_entropy_total
    yes_weather_dictionary['or_after'] = or_after_weather
    yes_whether_dictionary['or_after'] = or_after_whether
    no_weather_dictionary['or_after'] = no_or_after_weather
    no_whether_dictionary['or_after'] = no_or_after_whether

    # print("IS THERE THE WORD 'OR' IMMEDIATELY AFTER?")
    # print(f'No Weather: {no_or_after_weather}\nYes Weather: {or_after_weather}\nNo Whether: {no_or_after_whether}\nYes Whether: {or_after_whether}\n')
    # print(f'total entropy:  {or_after_entropy_total}')
    # print(f'information gain: {or_after_information_gain}\n\n\n')


  if not or_not_together_filter:
    no_or_not_weather = weather - or_not_weather
    no_or_not_whether = whether - or_not_whether
    or_not_entropy_total = weighted_entropy(or_not_weather, or_not_whether, no_or_not_weather, no_or_not_whether)
    or_not_information_gain = system_entropy - or_not_entropy_total
    information_gain_dictionary['or_not_together'] = or_not_information_gain
    entropy_dictionary['or_not_together'] = or_not_entropy_total
    yes_weather_dictionary['or_not_together'] = or_not_weather
    yes_whether_dictionary['or_not_together'] = or_not_whether
    no_weather_dictionary['or_not_together'] = no_or_not_weather
    no_whether_dictionary['or_not_together'] = no_or_not_whether

    # print("IS THERE THE PHRASE 'OR NOT' ANYWHERE IN THE SENTENCE?")
    # print(f'No Weather: {no_or_not_weather}\nYes Weather: {or_not_weather}\nNo Whether: {no_or_not_whether}\nYes Whether: {or_not_whether}\n')
    # print(f'total entropy:  {or_not_entropy_total}')
    # print(f'information gain: {or_not_information_gain}\n\n\n')

  if not or_anywhere_filter:
    no_or_anywhere_weather = weather - or_anywhere_weather
    no_or_anywhere_whether = whether - or_anywhere_whether
    or_anywhere_entropy_total = weighted_entropy(or_anywhere_weather, or_anywhere_whether, no_or_anywhere_weather, no_or_anywhere_whether)
    or_anywhere_information_gain = system_entropy - or_anywhere_entropy_total
    information_gain_dictionary['or_anywhere'] = or_anywhere_information_gain
    entropy_dictionary['or_anywhere'] = or_anywhere_entropy_total
    yes_weather_dictionary['or_anywhere'] = or_anywhere_weather
    yes_whether_dictionary['or_anywhere'] = or_anywhere_whether
    no_weather_dictionary['or_anywhere'] = no_or_anywhere_weather
    no_whether_dictionary['or_anywhere'] = no_or_anywhere_whether

    # print("IS THERE THE WORD 'OR' ANYWHERE?")
    # print(f'No Weather: {no_or_anywhere_weather}\nYes Weather: {or_anywhere_weather}\nNo Whether: {no_or_anywhere_whether}\nYes Whether: {or_anywhere_whether}\n')
    # print(f'total entropy:  {or_anywhere_entropy_total}')
    # print(f'information gain: {or_anywhere_information_gain}\n\n\n')

  if not whether_followed_filter:
    no_whether_followed_weather = weather - whether_followed_weather
    no_whether_followed_whether = whether - whether_followed_whether
    whether_followed_entropy_total = weighted_entropy(whether_followed_weather, whether_followed_whether, no_whether_followed_weather, no_whether_followed_whether)
    whether_followed_information_gain = system_entropy - whether_followed_entropy_total
    information_gain_dictionary['whether_followed'] =  whether_followed_information_gain
    entropy_dictionary['whether_followed'] = whether_followed_entropy_total
    yes_weather_dictionary['whether_followed'] = whether_followed_weather
    yes_whether_dictionary['whether_followed'] = whether_followed_whether
    no_weather_dictionary['whether_followed'] = no_whether_followed_weather
    no_whether_dictionary['whether_followed'] = no_whether_followed_whether

    # print("IS THE WORD FOLLOWED BY A COMMON WORD THAT USUALLY FOLLOWS WHETHER?")
    # print(f'No Weather: {no_whether_followed_weather}\nYes Weather: {whether_followed_weather}\nNo Whether: {no_whether_followed_whether}\nYes Whether: {whether_followed_whether}\n')
    # print(f'total entropy:  {whether_followed_entropy_total}')
    # print(f'information gain: {whether_followed_information_gain}\n\n\n')




  #find the new decision basis, based on which has maximum information gain (greedy algorithm)
  maxkey = None
  maxvalue = 0
  for x in information_gain_dictionary.keys():
    if information_gain_dictionary[x] > maxvalue:
      maxvalue = information_gain_dictionary[x]
      maxkey = x
  if maxkey is None:
    #if all examples seen were only "weather" or were only "whether", so there is no information gain possible
    return Node(None, 0, weather, whether, weather, whether, current_depth, max_depth)
  #otherwise, make a new node
  new_node = Node(maxkey, entropy_dictionary[maxkey], no_weather_dictionary[maxkey], no_whether_dictionary[maxkey], yes_weather_dictionary[maxkey], yes_whether_dictionary[maxkey], current_depth, max_depth)
  
  #toggle maxkey to true for filtering each side of the tree
  if maxkey == 'weather_related':
    weather_related_filter = True
    weather_related_return_including_right = True
    weather_related_return_including_left = False

  if maxkey == 'article_before':
    article_before_filter = True
    article_before_return_including_right = True
    article_before_return_including_left = False

  if maxkey == 'article_after':
    article_after_filter = True
    article_after_return_including_right = True
    article_after_return_including_left = False
  
  if maxkey == 'or_after':
    or_after_filter = True
    or_after_return_including_right = True
    or_after_return_including_left = False

  if maxkey == 'or_not_together':
    or_not_together_filter = True
    or_not_together_return_including_right = True
    or_not_together_return_including_left = False

  if maxkey == 'or_anywhere':
    or_anywhere_filter = True
    or_anywhere_return_including_right = True
    or_anywhere_return_including_left = False

  if maxkey == 'whether_followed':
    whether_followed_filter = True
    whether_followed_return_including_right = True
    whether_followed_return_including_left = False
  
  

  if current_depth != max_depth:
    new_node.setleftnode(tree_builder(weather_related_filter, weather_related_return_including_left, article_before_filter, article_before_return_including_left, article_after_filter, article_after_return_including_left, or_after_filter, or_after_return_including_left, or_not_together_filter, or_not_together_return_including_left, or_anywhere_filter, or_anywhere_return_including_left, whether_followed_filter, whether_followed_return_including_left, current_depth + 1, max_depth))
    new_node.setrightnode(tree_builder(weather_related_filter, weather_related_return_including_right, article_before_filter, article_before_return_including_right, article_after_filter, article_after_return_including_right, or_after_filter, or_after_return_including_right, or_not_together_filter, or_not_together_return_including_right, or_anywhere_filter, or_anywhere_return_including_right, whether_followed_filter, whether_followed_return_including_right, current_depth + 1, max_depth))
  return new_node


#if you want a category to be filtered for, set to true
#if you want positive values on that category used (and not negative values), set return_including to True
weather_related_filter = False
weather_related_return_including = False

article_before_filter = False
article_before_return_including = False

article_after_filter = False
article_after_return_including = False

or_after_filter = False
or_after_return_including = False

or_not_together_filter = False
or_not_together_return_including = False

or_anywhere_filter = False
or_anywhere_return_including = False

whether_followed_filter = False
whether_followed_return_including = False

current_depth = 0

#build the tree
print("Building the tree. This may take a moment.")
root_node = tree_builder(weather_related_filter, weather_related_return_including, article_before_filter, article_before_return_including, article_after_filter, article_after_return_including, or_after_filter, or_after_return_including, or_not_together_filter, or_not_together_return_including, or_anywhere_filter, or_anywhere_return_including, whether_followed_filter, whether_followed_return_including, current_depth, max_depth)

#once the tree is built, test it using test data, or allow the user to pick their own sentence
use_custom = input("would you like to use a custom sentence (type '0') or run against 1000 test sentences (type any other key)?: ")
if use_custom == "0":
  lines = [get_sentence()]
    
else:

  #get all of the lines of the test file into a list of strings
  with open(test_file_path) as f:
    lines = f.readlines()

#track whether to repeat or not (if user selected custom)
repeat_again = True

#track correct answers
correct_answers = 0
wrong_answers = 0

while(repeat_again):
  for line in lines:
    test_line = line.split()
    testdictionary = {}
    test_word = test_line[0]
    test_index = int(test_line[1])

    #test the test_line against all the properties, to find out all the truth values
    test_weather_found = check_for_list_of_words(test_line, weather_related_words)
    #weather_related, article_before, article_after, or_after, or_not_together, or_anywhere, whether_followed
    testdictionary['weather_related'] = test_weather_found
    try:
      test_prev_word = test_line[test_index + 1]
      test_prev_word_the = word_equal_check("the", test_prev_word)
      test_prev_word_a = word_equal_check("a", test_prev_word)
      test_prev_word_article = test_prev_word_the + test_prev_word_a
      testdictionary['article_before'] = test_prev_word_article
    except:
      #set to a default
      testdictionary['article_before'] = 0

    try:
      test_next_word = test_line[test_index + 3]
      test_next_word_the = word_equal_check("the", test_next_word)
      test_next_word_a = word_equal_check("a", test_next_word)
      test_next_word_article = test_next_word_the + test_next_word_a
      testdictionary['article_after'] = test_next_word_article
      test_next_word_or = word_equal_check("or", test_next_word)
      testdictionary['or_after'] = test_next_word_or
      test_whether_followed = (test_next_word in whether_followed_words)
      testdictionary['whether_followed'] = test_whether_followed
    except:
      testdictionary['article_after'] = False
      testdictionary['or_after'] = False
      testdictionary['whether_followed'] = False

    test_or_not_together = check_for_two_consecutive_words(test_line[2:], "or", "not")
    testdictionary['or_not_together'] = test_or_not_together
    test_or_anywhere = check_word_appear_in_sentence(test_line, "or")
    testdictionary['or_anywhere'] = test_or_anywhere

    #make a prediction
    decision_word = root_node.decision(testdictionary)

    if use_custom == "0":
      print(f'predicted word: {decision_word}')
    else:
      #evaluate it against the actual correct word
      if test_word == decision_word:
        correct_answers += 1
      else:
        wrong_answers += 1

  if use_custom != "0":
    #print test data
    print(f'correct answers: {correct_answers}')
    print(f'wrong answers: {wrong_answers}')

  if use_custom == "0":
    user_repeat = input("Would you like to try another sentence (type '0' for yes, any other key for no)?: ")
    if user_repeat == "0":
      lines = [get_sentence()]
    else:
      repeat_again = False
  else:
    repeat_again = False



