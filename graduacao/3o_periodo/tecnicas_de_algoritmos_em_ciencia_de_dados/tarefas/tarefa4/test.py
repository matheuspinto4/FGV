import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# --- Spliting the Data --- #

ads_df = pd.read_csv("adult_census_subset.csv")
X1 = ads_df[['age', 'workclass', 'fnlwgt', 'education', 'education.num', 'marital.status', 'occupation', 'relationship', 'race', 'sex', 'capital.gain', 'capital.loss', 'hours.per.week', 'native.country']]
Y1 = ads_df[['income']]
random_state = 9
X_train1, X_vt1, Y_train1, Y_vt1 = train_test_split(X1, Y1, test_size=0.3, random_state=random_state)
X_test1, X_validation1, Y_test1, Y_validation1 = train_test_split(X_vt1, Y_vt1, test_size=0.5, random_state=random_state)

X_train_set1 = pd.concat([X_train1, X_validation1])
Y_train_set1 = pd.concat([Y_train1, Y_validation1])



class Node:
    def __init__(self, set_index, depth):
        self.set_index = set_index 
        self.question = None
        self.left_child = None
        self.right_child = None
        self.gini = 0
        self.depth = depth
        self.label = None
        self.prob_classes = {}



class Question:
    def __init__(self, feature: str, operator: str, value: str or int):  # type: ignore
        """Inicia a o objeto
        Args:
            feature (str): Feature que participará da pergunta
            operator (str): Operador de comparação, ie. ">=", "==", ...
            value (str or int): Valor a ser comparado
        """
        self.feature = feature
        self.operator = operator
        self.value = value
    
    def __repr__(self):
        return f"{self.feature} {self.operator} {self.value}"
    


class RandomTree:
    def __init__(self, max_depth, min_node_instances):
        self.max_depth = max_depth
        self.min_node_instances = min_node_instances
        self.root = Node([], 0)

    def match(self, question, sample):
        if question.operator == "==":
            return sample[question.feature] == question.value
        elif question.operator == "<=":
            return sample[question.feature] <= question.value

    def gini_coeficient(self, set_index):
        if len(set_index) == 0:
            return 0
        
        counts = self.Y_train.loc[set_index].value_counts()
        proportions = counts / len(set_index)
        gini = 1 - np.sum(proportions ** 2)
        return gini

    def do_split(self, node, question):
        all_indices = node.set_index
        features_values = self.X_train.loc[all_indices, question.feature]

        if question.operator == "==":
            mask = (features_values == question.value)
        elif question.operator == "<=":
            mask = (features_values <= question.value)

        left_index = node.set_index[mask]
        right_index = node.set_index[~mask]
        
        gain = node.gini - len(left_index) * self.gini_coeficient(left_index) / len(node.set_index) - len(right_index) * self.gini_coeficient(right_index) / len(node.set_index)

        return gain, np.array(left_index), np.array(right_index)

    def select_question(self, node):
        best_gain = 0
        best_question = None
        best_left_index = None
        best_right_index = None
        
        # Get the target variable for the current node once
        y_node = self.Y_train.loc[node.set_index].squeeze()

        # Iterate through features to find the best split
        random_features = np.random.choice(self.columns_labels, size=self.num_features, replace=False)
        for feature in random_features:
            x_node_feature = self.X_train.loc[node.set_index, feature]
            
            if x_node_feature.dtype == object: # Categorical feature (logic remains the same)
                for value in x_node_feature.unique():
                    question = Question(feature=feature, operator="==", value=value)
                    gain_new, left_index, right_index = self.do_split(node, question)
                    if gain_new > best_gain:
                        best_gain, best_question, best_left_index, best_right_index = gain_new, question, left_index, right_index
            
            else: # <-- OPTIMIZED LOGIC FOR NUMERICAL FEATURES
                # 1. Sort data by feature value
                # Combine feature values and targets, then sort
                df_temp = pd.DataFrame({'feature': x_node_feature, 'label': y_node}).sort_values('feature')
                sorted_labels = df_temp['label'].values
                sorted_indices = df_temp.index.values

                # 2. Initialize class counts for the two potential children
                # Left child starts empty, right child has all samples
                right_counts = y_node.value_counts().to_dict()
                left_counts = {k: 0 for k in right_counts.keys()}
                
                n_right = len(sorted_labels)
                n_left = 0

                # 3. Iterate through sorted samples, updating counts incrementally
                for i in range(len(sorted_labels) - 1):
                    # Move one sample from right to left
                    label = sorted_labels[i]
                    n_left += 1
                    n_right -= 1
                    left_counts[label] += 1
                    right_counts[label] -= 1

                    # To avoid splitting on identical feature values, only check for a split
                    # when the feature value changes.
                    current_val = sorted_labels[i]
                    next_val = sorted_labels[i+1]
                    if current_val == next_val:
                        continue

                    # 4. Calculate Gini gain with the updated counts
                    # This is much faster as it doesn't re-calculate value_counts()
                    p_left = np.array(list(left_counts.values())) / n_left
                    gini_left = 1 - np.sum(p_left**2)

                    p_right = np.array(list(right_counts.values())) / n_right if n_right > 0 else 0
                    gini_right = 1 - np.sum(p_right**2)
                    
                    gain_new = node.gini - (n_left / len(node.set_index)) * gini_left - (n_right / len(node.set_index)) * gini_right
                    
                    if gain_new > best_gain:
                        best_gain = gain_new
                        # The threshold is the midpoint between the two differing values
                        threshold = (df_temp['feature'].iloc[i] + df_temp['feature'].iloc[i+1]) / 2
                        best_question = Question(feature=feature, operator="<=", value=threshold)
                        
                        # The split indices can be taken directly from the sorted array
                        best_left_index = sorted_indices[:i+1]
                        best_right_index = sorted_indices[i+1:]

        return best_gain, best_question, best_left_index, best_right_index         

    def recursive_growth(self, node):
        if node.gini == 0 or node.depth >= self.max_depth or len(node.set_index) <= self.min_node_instances:
            counts = self.Y_train.loc[node.set_index].value_counts()
            if not counts.empty:
                node.label = counts.idxmax()
                node.prob_classes = (counts / len(node.set_index)).to_dict()
            return
         
        best_gain, best_question, left_index, right_index = self.select_question(node)

        if best_gain == 0: # Criou um filho igual ao pai, Se entrar na recursão ela fica infinita
            counts = self.Y_train.loc[node.set_index].value_counts()
            if not counts.empty:
                node.label = counts.idxmax() 
                node.prob_classes = (counts / len(node.set_index)).to_dict()
            return
        
        node.question = best_question
        # print(node.question, node.depth)

        node.left_child = Node(left_index, node.depth + 1)
        node.left_child.gini = self.gini_coeficient(left_index)

        node.right_child = Node(right_index, node.depth + 1)
        node.right_child.gini = self.gini_coeficient(right_index)
        
        self.recursive_growth(node.left_child)
        self.recursive_growth(node.right_child)    

    def fit(self, X_train, Y_train, num_features=None):
        self.columns_labels = X_train.columns
        self.num_features = num_features
        self.X_train = X_train
        self.Y_train = Y_train

        self.root.set_index = self.X_train.index.to_numpy()
        self.root.gini = self.gini_coeficient(self.root.set_index)
        
        self.recursive_growth(self.root)

    def prediction_recursion(self, x, node):
        if node.label != None:
            return node
        if self.match(node.question, x):
            return self.prediction_recursion(x, node.left_child)
        else:
            return self.prediction_recursion(x, node.right_child)
        
    def predic_probabilities(self, X_test, true_label=(1,)):
        prob_classes = []
        for index in range(len(X_test)):
            leaft_node = self.prediction_recursion(X_test.iloc[index], self.root)
            probability = leaft_node.prob_classes.get(true_label, 0.0)
            prob_classes.append(probability)
        return prob_classes
        
    def predict(self, X_test):
        predictions = []
        for index in range(len(X_test)):
            leaf_node = self.prediction_recursion(X_test.iloc[index], self.root)
            predictions.append(leaf_node.label) 
        return predictions


class RandomForest:
    def __init__(self, B=20, max_depth=8, min_node_instances=10, min_depth=3, max_instances=50):
        self.B = B
        self.bag = []
        self.max_depth = max_depth
        self.min_node_instances = min_node_instances
        # self.min_depth = min_depth
        # self.max_instances = max_instances

    def fit(self, X_train, Y_train, num_features=None):
        if num_features == None:
            self.num_features = int(np.sqrt(X_train.shape[1]))
        else:
            self.num_features = num_features
        n_samples = X_train.shape[0]

        for _ in range(self.B):
            indices = np.random.choice(n_samples, size=n_samples, replace=True)
            X_bootstrap, Y_bootstrap = X_train.iloc[indices], Y_train.iloc[indices]
            X_bootstrap = X_bootstrap.reset_index(drop=True)
            Y_bootstrap = Y_bootstrap.reset_index(drop=True)
            
            randomTree = RandomTree(max_depth=self.max_depth, min_node_instances=self.min_node_instances)
            randomTree.fit(X_bootstrap, Y_bootstrap, num_features=self.num_features)
            self.bag.append(randomTree)

    def predict_probabilities(self, X_test, B=None):
        if B == None:
            B = self.B
            
        mean_prediction = np.zeros(X_test.shape[0]).reshape((X_test.shape[0],1))
        for index in list(np.random.choice(range(self.B), replace=False,size=B)):
            tree = self.bag[index]
            pred = np.array(tree.predict(X_test))
            mean_prediction += pred
        
        return mean_prediction / B
    

    def predict(self, X_test,B=None):
        if B == None:
            B = self.B
        
        probabilities = self.predict_probabilities(X_test=X_test, B=B)

        prediction = (probabilities > 0.5).astype(int)

        return prediction
    

best_min_node_instances_rf = 0
best_num_features_rf = 0
best_score_rf = 0
best_max_depth = 0
best_B_rf = 0
for max_depth in [3,4,5,6,7]:
    print(max_depth)
    for num_features in [3]: # ~sqrt(X_train.shape[1])
        for min_node_instances in [10,20,30,40]:
            for B in [10,20]:
                rf = RandomForest(B=B, max_depth=max_depth, min_node_instances=min_node_instances)
                rf.fit(X_train=X_train1, Y_train=Y_train1, num_features=num_features)
                prob = rf.predict_probabilities(X_test=X_test1, B=B)
                score = roc_auc_score(Y_test1, prob)
                if score > best_score_rf:
                    best_max_depth = max_depth
                    best_num_features_rf = num_features
                    best_min_node_instances_rf = min_node_instances
                    best_B_rf = B
                    best_score_rf = score



best_rf = RandomForest(B=best_B_rf, max_depth=best_max_depth, min_instances=best_min_node_instances_rf)
best_rf.fit(X_train=X_train_set1, Y_train=Y_train_set1, num_features=best_num_features_rf)

prob = best_rf.predict_probabilities(X_test=X_test1, B=best_B_rf)
score = roc_auc_score(Y_test1, prob)


print(f"Test Score: {score}")