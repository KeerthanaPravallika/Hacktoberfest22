#!/usr/bin/env python
# coding: utf-8

# # Goals

# In this lab you will :
#   Learn to implement the model fw,b for linear regression with one variable

# # Tools

# In this lab we will make use of 

#     Numpy - a popular library for scientific computing
#     Matplotlib - a popular library for plotting data

# In[2]:


import numpy as np
import matplotlib.pyplot as plt


# # Problem statement

# In[3]:


x_train = np.array([1.0,2.0])
y_train = np.array([300 , 500])


# In[5]:


m=len(x_train)
print(f'number of training examples - {m}')


# In[7]:


i=0
x_i=x_train[i]
y_i=y_train[i]
print(f'ith training example - ({x_i},{y_i})')


# In[10]:


plt.scatter(x_train,y_train,marker='x',c='r')


# In[19]:


w=200
b=100


# In[20]:


def calc(x,y,w,b):
    m=x.shape
    f=np.zeros(m)
    for i in range(len(x)):
        f[i]=w*x[i]+b
    return f


# In[21]:


y_hat=calc(x_train,y_train,w,b)


# In[22]:


plt.plot(x_train,y_hat,c='b')
plt.scatter(x_train,y_train,c='r')


# In[23]:


cost= w*1.2 +b


# In[24]:


print(f'predicted price - {cost}')


# In[ ]:




