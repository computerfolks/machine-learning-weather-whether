﻿This repo contains the machine-learning "whether/weather" selector (an extension of the first project for my Machine Learning class).

**What The Program Does:**

 This is a machine-learning program designed using a simple ID3-like decision tree learning algorithm which, when given a sentence containing either the word “whether” or the word “weather,” predicts which word is correct in the given context. The program builds the decision tree by examining the value of 7 boolean attributes across 15,000 training sentences.
 
The user can then test the program by giving a custom sentence, or by directing the program to automatically test itself on 1,000 test sentences. When the tree is set to a maximum depth of 3, the model is able to achieve ~90% accuracy.

**How To Run The Program**

First, at the top of the program file, the user must enter the correct filepaths (for training_file_path and test_file_path) to access the training data and the test data. The user can then set what % of the training data they would like to use, as well as the max depth to use when building the tree.

During runtime, the program will prompt the user to decide whether to use a custom sentence to test the model or to use default test data. If the custom sentence option is selected, the model will prompt the user for a sentence, with the target word (“weather”/”whether”) replaced by the string “XXX”. The model will predict which word is correct, and then prompt the user for either an additional sentence, or to exit the program.

If the user selects to test using default test data, the program tests itself on the test data by making a prediction and evaluating if the prediction was correct. The program displays the final tally to the user and exits.

**How The Program Works**

There are three key pieces which work together to build the decision tree: the filter function, the tree_builder function, and the Node class. The filter function takes in which filters are “active”; in other words, which attributes have already been selected by a higher decision node. For the active filters, there will also be a desired return value. For example, when the program builds the tree using training data, and we have already determined that the root node would be if "or not" appears in the sentence, then we want future decision nodes to either be seeing only positive examples (sentences in which “or not” appears) or only negative examples.

Before using a sentence to build a given node, the tree_builder function will pass the sentence through the filter function. If it passes the filter, it is used as part of the next decision. The tree_builder function is built for recursion. Once a node is created, if max_depth has not been reached, the function calls on itself to create the left and right node of the current node. For example, to create the left node and right node for the “or not” node, simply call the function again, but toggle the “or not” filter to true, set the return_including values to negative for the left node (so the filter function returns desired sentences only), and set the return_including values to positive for the right node.

As discussed the program builds a tree using the tree_builder function. This function takes in what filters should be applied, and what decision to make on active filters. The function tracks the following attributes: an article occurring immediately before the target word, an article occurring immediately after, the word “or” appearing immediately after, the phrase “or not” appearing anywhere in the sentence, a “weather-related” word (based on a list of weather-related words) appearing anywhere in the sentence, the word “or” appearing anywhere in the sentence, and a common English word (based on a list of common English words) that grammatically fits with the word “whether” immediately following the target word.

The function calculates the entropy (calling other functions) for each attribute, and uses this to calculate the information gain. It chooses the maximum information gain, sets the filter for that attribute to be true, creates the decision node, and splits the data across two recursive calls to set the left and right node. For example, if the attribute “or not” is chosen to be the basis of a given decision node, the filter for “or not” is set to true, and the left node is given all the input that does not have an article before (using the return_included variable), while the right node is given all the input that has an article before. The function recursively builds nodes until maximum depth is hit, or the entropy is zero (all words fall into either “weather” or “whether”).

The program then tests itself, using either a custom sentence written by the user, or the test data in the test data file. To test a given input, it determines the sentence’s truth value for all the attributes, then calls the decision function for the root node. The node recursively calls down the proper branch (right or left, based on the attribute value for the basis of the decision at that node), and the decision is returned when maximum depth is reached. The program reports either a prediction (if given custom input) or the score report of correct answers vs. wrong answers on the test data.
