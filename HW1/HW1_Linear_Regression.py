
# coding: utf-8

# In[85]:


import tensorflow as tf
import numpy as np 
from sklearn import preprocessing
from sklearn.datasets import fetch_california_housing
from IPython.display import clear_output, Image, display, HTML

###### Do not modify here ###### 
def strip_consts(graph_def, max_const_size=32):
    """Strip large constant values from graph_def."""
    strip_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = strip_def.node.add() 
        n.MergeFrom(n0)
        if n.op == 'Const':
            tensor = n.attr['value'].tensor
            size = len(tensor.tensor_content)
            if size > max_const_size:
                tensor.tensor_content = "<stripped %d bytes>"%size
    return strip_def

def show_graph(graph_def, max_const_size=32):
    """Visualize TensorFlow graph."""
    if hasattr(graph_def, 'as_graph_def'):
        graph_def = graph_def.as_graph_def()
    strip_def = graph_def
    #strip_def = strip_consts(graph_def, max_const_size=max_const_size)
    code = """
        <script>
          function load() {{
            document.getElementById("{id}").pbtxt = {data};
          }}
        </script>
        <link rel="import" href="https://tensorboard.appspot.com/tf-graph-basic.build.html" onload=load()>
        <div style="height:600px">
          <tf-graph-basic id="{id}"></tf-graph-basic>
        </div>
    """.format(data=repr(str(strip_def)), id='graph'+str(np.random.rand()))

    iframe = """
        <iframe seamless style="width:1200px;height:620px;border:0" srcdoc="{}"></iframe>
    """.format(code.replace('"', '&quot;'))
    display(HTML(iframe))
###### Do not modify  here ######

###### Implement Data Preprocess here ######
housing = fetch_california_housing()
print("Shape of dataset:", housing.data.shape)
print("Shape of label:", housing.target.shape)

X = np.array(housing.data)
y = np.array(housing.target)
X = preprocessing.scale(X)
numData = len(housing.target)
trainRate = 0.9
numTrain = int(trainRate * numData)
numData = int(numData)
numTest = int(0.1*numData)

X_train = tf.constant(X[:numTrain, :], dtype='float32')
X_test = tf.constant(X[numTrain:, :], dtype='float32')
y_train = tf.constant(y[:numTrain], dtype='float32')
y_test = tf.constant(y[numTrain:], dtype='float32')
###### Implement Data Preprocess here ######

####creat tensorflow structure####
Weights = tf.Variable(tf.random_uniform([8,1],-1.0,1.0))
biases = tf.Variable(tf.zeros([1]))

y = tf.add(tf.matmul(X_train,Weights), biases*tf.ones([numTrain,1]))

loss = tf.reduce_mean(tf.square(y-y_train))

optimizer = tf.train.GradientDescentOptimizer(0.01)  #learning rate

train = optimizer.minimize(loss)
y_predict = tf.add(tf.matmul(X_test, Weights), biases*tf.ones([numTest,1]))
error=tf.reduce_mean((y_test-y_predict)/y_test)
init = tf.global_variables_initializer()


####creat tensorflow structure####

###### Start TF session ######
with tf.Session() as sess:
  sess.run(init)   
  #print(sess.run(y_data))
  print(sess.run(error))
  for step in range(201):
    sess.run(train)
    if step % 20 ==0:
      print(step,sess.run(Weights),sess.run(biases))
    print(sess.run(error))
    #show_graph(tf.get_default_graph().as_graph_def())
###### Start TF session ######

