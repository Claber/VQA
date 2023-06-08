import json, sys, os
from itertools import groupby
from operator import itemgetter

data_home = "/home/wolfe/code/nlvr/vqa/"
annotation_path = data_home + "Annotations/mscoco_all_annotations.json"
qestion_path = data_home + "Questions/OpenEnded_mscoco_all_questions.json"
ofa_vani_result = data_home + "Results/ofa_vannila/OpenEnded_mscoco_all__results.json"
ofa_plus_retrieval_result = data_home + "Results/ofa_plus_retrieval/OpenEnded_mscoco_all__results.json"
image_dirs = ["/home/wolfe/data_sets/ok_vqa/train2014", "/home/wolfe/data_sets/ok_vqa/val2014"]
test_picture_file_name_pattern = "COCO_val2014_{pic_name}"
train_picture_file_name_pattern = "COCO_train2014_{pic_name}"
pic_file_patterns = [train_picture_file_name_pattern, test_picture_file_name_pattern]

def pic_path_pattern(pat_str):
    def p(image_id, image_dir):
        # "COCO_val2014_000000000164.jpg"
        id = ["0"] * len("000000000164")
        image_id = str(image_id)
        l = len(image_id)
        l0 = len(id)
        assert l  < l0, "image id > max"
        for i,c in enumerate(image_id):
            id[l0 - l + i] = str(c)
        image_id = "".join(id) + ".jpg"
        return os.path.join(image_dir, pat_str.format(pic_name = image_id))
    
    return p

formatters = [pic_path_pattern(p) for p in pic_file_patterns]

def question_infor_formatter(tup):
    ann, d1, d2, question, id, is_t_f, s, s2 = tup
    img_dir_index = 1 if id >=9009 else 0
    image_abs_path = formatters[img_dir_index](question[0]["image_id"], image_dirs[img_dir_index])
    subset_label = "train2014" if img_dir_index == 0 else "eval2014"
    return f'question_id={ann["question_id"]}, subset={subset_label}, t_f={1 if is_t_f else 0}{1 if d1[0]["answer"].lower() in ("yes", "no") else 0}, {question[0]["question"]}, image @:{image_abs_path} -> score={s},{s2}, ans1_ofa={d1[0]["answer"]}, ans2_ofa_retrieval={d2[0]["answer"]}, ans_ref={str([a["answer"] for a in ann["answers"]])}'

def similarity(str1, str2, strict = False):
    ta = str1.split()
    tb = str2.split()
    all_t = ta + tb
    all_t = set(all_t)
    t1 = set(ta)
    t2 = set(tb)
    inter = t1.intersection(t2)
    second_score = 0.
   
    if not strict and len(inter) == 0:
        for t in t1:
            for t_ in t2:
                current_score = 0
                c1 = set([str(c) for c in t])
                c2 = set([str(c) for c in t_])
                c_all = c1.union(c2)
                c_inter = c1.intersection(c2)
                current_score = float(len(c_inter))/float(len(c_all))
                if current_score > second_score:
                    second_score = current_score

    return float(len(inter))/float(len(all_t)) + second_score

def score(e):
    return similarity(e[1][0]["answer"], e[2][0]["answer"])

def score_1(e):
    return max([similarity(e[1][0]["answer"], a["answer"], True) for a in e[0]["answers"]])


with open(annotation_path,'r') as af, open(ofa_vani_result,'r') as f1, open(ofa_plus_retrieval_result,'r') as f2, open(qestion_path,'r') as f3:
    ann_js = json.load(af)["annotations"]
    r1_js = json.load(f1)
    r2_js = json.load(f2)
    q_js = json.load(f3)["questions"]
    d1 = {}
    d2 = {}
    d3 = {}
    for qid, item in groupby(r1_js, key = itemgetter("question_id")):
        d1[qid] = list(item)
        assert len(d1[qid]) == 1
    for qid, item in groupby(r2_js, key = itemgetter("question_id")):
        d2[qid] = list(item)
        assert len(d2[qid]) == 1

    for qid, item in groupby(q_js, key = itemgetter("question_id")):
        d3[qid] = list(item)
        assert len(d3[qid]) == 1
        



    tuples  = [(ann, d1[ann["question_id"]], d2[ann["question_id"]], d3[ann["question_id"]], i) for i, ann in enumerate(ann_js)]
    _tuples_sorted = [ tuple(list(a) + [a[2][0]["answer"].lower() in ('yes', 'no')] + [score(a), score_1(a)])  for a in tuples]
    tuples_sorted = sorted(_tuples_sorted, key = lambda a: a[-2])
    c = 0
    for t in tuples_sorted:
        if c > 200: 
            break
        else:
            if t[-1] > 0:
                c = c + 1
                print(question_infor_formatter(t))
    print (c)
    print(float(c)/float(len(tuples)))
