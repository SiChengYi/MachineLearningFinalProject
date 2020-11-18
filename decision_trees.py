import csv
import math
import matplotlib.pyplot as plt

class InternalNode(object):
    # An Internal Node class that has an associated feature and criteria for splitting.
    def __init__(self, feature, criteria):  # Constructor
        self.type = type
        self.feature = feature
        self.criteria = criteria
        self.left = None
        self.right = None

    def insert_left(self, child):
        if self.left is None:
            self.left = child
        else:
            child.left = self.left
            self.left = child

    def insert_right(self, child):
        if self.right is None:
            self.right = child
        else:
            child.right = self.right
            self.right = child

    def get_depth(self, iter):
        # Recursively return the depth of the node.
        l_depth = self.left.get_depth(iter + 1)
        r_depth = self.right.get_depth(iter + 1)

        # return the highest of the two
        return max([l_depth, r_depth])

    def is_leaf(self):
        return 0


class LeafNode(object):
    # A Leaf Node class that has an associated decision.
    def __init__(self, decision):  # Constructor
        self.decision = decision

    def retrieveDecision(self, child):
        return self.decision

    def get_depth(self, iter):
        return iter

    def is_leaf(self):
        return 1


def avg_calc(data):
    avg = []
    for j in range(1, 7):
        num_ben = 0
        num_mal = 0
        avg_p = 0
        avg_n = 0
        for i in range(1, len(data)):
            if data[i][7] == '0':
                if data[i][j] != '':
                    num_ben += 1
                    avg_p += int(data[i][j])
            else:
                if data[i][j] != '':
                    num_mal += 1
                    avg_n += int(data[i][j])

        avg_p /= num_ben
        if num_mal != 0:
            avg_n /= num_mal
        avg.append((avg_p + avg_n) / 2)
    return avg


def find_num_ben(data):
    num_ben = 0
    for i in range(0, len(data)):
        if data[i][7] == '0':
            num_ben += 1
    return num_ben


def find_num_mal(data):
    num_mal = 0
    for i in range(0, len(data)):
        if data[i][7] == '1':
            num_mal += 1
    return num_mal


def info_gain_calc(data, avg, total_entropy):
    info_gain = []
    for i in range(0, len(avg)):
        num_pos_t = 0
        num_pos_f = 0
        num_true = 0
        num_neg_t = 0
        num_neg_f = 0
        num_false = 0
        total_cases = 0
        for j in range(1, len(data)):
            if data[j][i + 1] != '':
                total_cases += 1
                if int(data[j][i + 1]) < avg[i]:
                    num_true += 1
                    if data[j][7] == '0':
                        num_pos_t += 1
                    else:
                        num_neg_t += 1
                else:
                    num_false += 1
                    if data[j][7] == '0':
                        num_pos_f += 1
                    else:
                        num_neg_f += 1
        num_pos_ta = 0
        num_neg_ta = 0
        num_pos_fa = 0
        num_neg_fa = 0
        if num_true != 0:
            if num_pos_t / num_true != 0:
                num_pos_ta = (-num_pos_t / num_true) * math.log(num_pos_t / num_true, 2)
            if num_neg_t / num_true != 0:
                num_neg_ta = (-num_neg_t / num_true) * math.log(num_neg_t / num_true, 2)
        if num_false != 0:
            if num_pos_f / num_false != 0:
                num_pos_fa = (-num_pos_f / num_false) * math.log(num_pos_f / num_false, 2)
            if num_neg_f / num_false != 0:
                num_neg_fa = (-num_neg_f / num_false) * math.log(num_neg_f / num_false, 2)
        true_answer = num_true / total_cases * (num_pos_ta + num_neg_ta)
        false_answer = num_false / total_cases * (num_pos_fa + num_neg_fa)
        condition = true_answer + false_answer
        info_gain.append(total_entropy - condition)

    return info_gain


def determine_feature(avg, category):
    root = InternalNode('failed', 0)
    if category == 0:
        root = InternalNode('subscribers', avg[category])
    elif category == 1:
        root = InternalNode('submission_titles_containing_toxic_words', avg[category])
    elif category == 2:
        root = InternalNode('submissions_containing_toxic_words', avg[category])
    elif category == 3:
        root = InternalNode('total_submissions_score', avg[category])
    elif category == 4:
        root = InternalNode('comments_containing_toxic_words', avg[category])
    elif category == 5:
        root = InternalNode('total_comments_score', avg[category])
    print(root.feature)
    return root


def read_feature(node):
    feature = node.feature
    if feature == "subscribers":
        return 1
    elif feature == "submission_titles_containing_toxic_words":
        return 2
    elif feature == "submissions_containing_toxic_words":
        return 3
    elif feature == "total_submissions_score":
        return 4
    elif feature == "comments_containing_toxic_words":
        return 5
    elif feature == "total_comments_score":
        return 6
    return 0


def construction_recurse(data, threshold, curr_level, kind):
    avg = avg_calc(data)

    num_ben = find_num_ben(data)
    num_mal = find_num_mal(data)

    total_cases = num_ben + num_mal
    total_entropy = -(num_ben / total_cases * math.log(num_ben / total_cases, 2)) - (num_mal / total_cases * math.log(num_mal / total_cases, 2))
    info_gain = info_gain_calc(data, avg, total_entropy)

    category = 0
    max = 0
    for i in range(0, len(info_gain)):
        if info_gain[i] > max:
            max = info_gain[i]
            category = i

    root = determine_feature(avg, category)
    true_data = []
    false_data = []
    for i in range(1, len(data)):
        if data[i][category + 1] != '':
            if int(data[i][category + 1]) < root.criteria:
                true_data.append(data[i])
            else:
                false_data.append(data[i])
    num_different_p = 0
    num_different_f = 0
    for i in range(0, len(true_data)):
        if true_data[i][7] != true_data[0][7]:
            num_different_p += 1
    for i in range(0, len(false_data)):
        if false_data[i][7] != false_data[0][7]:
            num_different_f += 1

    if kind == 0:
        if num_different_p == 0 or threshold == curr_level:
            child1 = LeafNode(0)
        else:
            child1 = construction_recurse(true_data, threshold, curr_level + 1, kind)
        if num_different_f == 0 or threshold == curr_level:
            child2 = LeafNode(1)
        else:
            child2 = construction_recurse(false_data, threshold, curr_level + 1, kind)
        root.insert_right(child2)
        root.insert_left(child1)
    if kind == 1:
        if num_different_p == 0 or threshold > max:
            child1 = LeafNode(0)
        else:
            child1 = construction_recurse(true_data, threshold, curr_level + 1, kind)
        if num_different_f == 0 or threshold > max:
            child2 = LeafNode(1)
        else:
            child2 = construction_recurse(false_data, threshold, curr_level + 1, kind)
        root.insert_right(child2)
        root.insert_left(child1)
    return root


class DecisionTreeBuilder:
    '''This is a Python class named DecisionTreeBuilder.'''

    def __init__(self):  # Constructor
        self.tree = None  # Define a ``tree'' instance variable.

    def construct(self, data, threshold, kind):
        # kind = kind of threshold,0 for depth, 1 for info gain
        '''
           This function constructs your tree with a default threshold of None.
           The depth of the constructed tree is returned.
        '''
        self.tree = construction_recurse(data, threshold, 1, kind)
        return self.tree.get_depth(0)  # Return the depth of your constructed tree.

    def classify(self, data):
        '''
           This function classifies data with your tree.
           The predictions for the given data are returned.
        '''
        # Use the constructed tree here., e.g. self.tree

        predicts = []

        for i in range(0, len(data)):
            node = self.tree
            flag = 0
            for j in range(1, 7):
                if data[i][j] == '':
                    flag = 1
            if flag == 1:
                continue
            while node.is_leaf() == 0:
                category = read_feature(node)
                if int(data[i][category]) < node.criteria:
                    node = node.left
                else:
                    node = node.right
            predicts.append(node.decision)
        # Return a list of predictions.
        pain = 0
        tn = 0
        fn = 0
        tp = 0
        fp = 0
        for i in range(0, len(predicts)):
            for j in range(1, 7):
                if data[i][j] == '':
                    i+=1
                    break

            if int(predicts[pain]) == int(data[i][7]):
                if data[i][7] == '0':
                    tn += 1
                elif data[i][7] == '1':
                    tp += 1
            else:
                if data[i][7] == '0':
                    fp += 1
                elif data[i][7] == '1':
                    fn += 1
            pain+=1
        print("{:>25}".format("PREDICTED CLASS"))
        print("{:>15}".format("non toxic"),"toxic")
        print("TRUE CLASS")
        print("{:<10}".format("non toxic"),tn,"{:>7}".format(fp))
        print("{:<10}".format("toxic"),fn,"{:>7}".format(tp))
        global accuracy
        global recall
        global precision
        global F1
        accuracy = (tn + tp) / (tn + tp + fn + fp)
        print("\nAccuracy:", accuracy)
        recall = 0
        if tp + fn != 0:
            recall = tp / (tp + fn)
        else:
            recall = 0
        print("recall:", recall)
        precision = tp / (tp + fp)
        print("Precision:", precision)
        if precision + recall != 0:
            F1 = 2 * precision * recall / (precision + recall)
        else:
            F1 = 0
        print("F1:", F1)
        return predicts







print("1. Reading File")
with open("data.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # Uncomment the following line if the first line in your CSV is column names
    # next(reader, None)  # skip the headers

    # create a list (i.e. array) where each index is a row of the CSV file.
    all_data = [row for row in reader]
print()

# 2. Split the data into training and test sets.
#   Note: This is an example split that simply takes the first 90% of the
#    data read in as training data and uses the remaining 10% as test data.
print("2. Separating Data")
number_of_rows = len(all_data)  # Get the length of our list.
training_data = all_data[0:int((len(all_data)-1)*.8)]
test_data = all_data[int((len(all_data)-1)*.8): len(all_data)-1]


print()
# 3. Create an instance of the DecisionTreeBuilder class.
accuracies = [0]
recalls = [0]
precisions = [0]
F1s = [0]
for i in range(1, 9):
    print("3. Instantiating DecisionTreeBuilder")
    dtb = DecisionTreeBuilder()
    print()

    # 4. Construct the Tree.
    print("4. Constructing the Tree with Training Data")
    tree_length = dtb.construct(training_data, i, 0)
    print("Tree Length: " + str(tree_length))
    print()

    # 5. Classify Test Data using the Tree.
    print("5. Classifying Test Data with the Constructed Tree")
    predictions = dtb.classify(test_data)
    accuracies.append(accuracy)
    recalls.append(recall)
    precisions.append(precision)
    F1s.append(F1)

plt.plot(accuracies, label='accuracy')
plt.plot(recalls, label = 'recall')
plt.plot(precisions,label = 'precision')
plt.plot(F1s,label = 'F1 score')
plt.title('Accuracy VS recall VS precision VS F1')
plt.ylabel('Y Axis')
plt.xlabel("Max Tree Length")
plt.yticks([.25,0.5,.75,1])
plt.legend(loc = 'best')
plt.show()



accuracies = [0]
recalls = [0]
precisions = [0]
F1s = [0]
list = []
i = 0
while i < 1:
    list.append(i)
    print("3. Instantiating DecisionTreeBuilder")
    dtb = DecisionTreeBuilder()
    print()

    # 4. Construct the Tree.
    print("4. Constructing the Tree with Training Data")
    tree_length = dtb.construct(training_data, i, 1)
    print("Tree Length: " + str(tree_length))
    print()

    # 5. Classify Test Data using the Tree.
    print("5. Classifying Test Data with the Constructed Tree")
    predictions = dtb.classify(test_data)
    accuracies.append(accuracy)
    recalls.append(recall)
    precisions.append(precision)
    F1s.append(F1)
    i+=.01

plt.plot(accuracies, label='accuracy')
plt.plot(recalls, label = 'recall')
plt.plot(precisions,label = 'precision')
plt.plot(F1s,label = 'F1 score')
plt.title('Accuracy VS recall VS precision VS F1')
plt.ylabel('Y Axis')
plt.xlabel("Runs")
plt.yticks([.25,.5,.75,1])
plt.legend(loc = 'best')
plt.show()