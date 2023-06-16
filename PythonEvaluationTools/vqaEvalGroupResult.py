# coding: utf-8

import sys
dataDir = '../../vqa'
sys.path.insert(0, '%s/PythonHelperTools/vqaTools' %(dataDir))
from vqa import VQA
from vqaEvaluation.vqaEval import VQAEval
import matplotlib.pyplot as plt
import skimage.io as io
import json
import random
import os

# set up file names and paths
versionType ='' # this should be '' when using VQA v2.0 dataset
taskType    ='OpenEnded' # 'OpenEnded' only for v2.0. 'OpenEnded' or 'MultipleChoice' for v1.0
dataType    ='mscoco'  # 'mscoco' only for v1.0. 'mscoco' for real and 'abstract_v002' for abstract for v1.0. 
dataSubType ='all'
annFile    ='%s/Annotations/%s%s_%s_annotations.json'%(dataDir, versionType, dataType, dataSubType)
quesFile    ='%s/Questions/%s%s_%s_%s_questions.json'%(dataDir, versionType, taskType, dataType, dataSubType)
print(annFile, quesFile)
imgDir      = '/home/wolfe/data_sets/ok_vqa/{}'.format(dataSubType)
resultType  =''
fileTypes   = ['results', 'accuracy', 'evalQA', 'evalQuesType', 'evalAnsType'] 

def new_func(dataDir, versionType, taskType, dataType, dataSubType, annFile, quesFile, resultType, fileTypes, gp_num):
    group_result_dir = "single_rationals/" + gp_num

# An example result json file has been provided in './Results' folder.  
# reFile = nlvr/vqa/Results/OpenEnded_mscoco_train2014_fake_results.json
    [resFile, accuracyFile, evalQAFile, evalQuesTypeFile, evalAnsTypeFile] = ['%s/Results/%s/%s%s_%s_%s_%s_%s.json'%(dataDir,group_result_dir , versionType, taskType, dataType, dataSubType, \
resultType, fileType) for fileType in fileTypes]  

# create vqa object and vqaRes object
    vqa = VQA(annFile, quesFile)
    vqaRes = vqa.loadRes(resFile, quesFile)

# create vqaEval object by taking vqa and vqaRes
    vqaEval = VQAEval(vqa, vqaRes, n=2)   #n is precision of accuracy (number of places after decimal), default is 2

# evaluate results
    """
If you have a list of question ids on which you would like to evaluate your results, pass it as a list to below function
By default it uses all the question ids in annotation file
"""
    vqaEval.evaluate() 

# print accuracies
    
    print ("Group %d, Overall Accuracy is: %.02f\n" %(i, vqaEval.accuracy['overall']))
    return vqaEval.accuracy['overall']

res = {}
for i in range(0, 9):
	res[i] = new_func(dataDir, versionType, taskType, dataType, dataSubType, annFile, quesFile, resultType, fileTypes, str(i))

res_sorted = sorted (res.items(), key=lambda a: a[1])
for rs in res_sorted:
      print(rs)




