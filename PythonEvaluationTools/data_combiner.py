import json
import os

anns_files = ["nlvr/vqa/Annotations/" + i for i in 
              ["mscoco_train2014_annotations.json", "mscoco_val2014_annotations.json"]]
question_files = ["nlvr/vqa/Questions/" + i for i in 
              ["OpenEnded_mscoco_train2014_questions.json", "OpenEnded_mscoco_val2014_questions.json"]]
answer_files = ["nlvr/vqa/Results/OpenEnded_mscoco_train2014__results.json", 
                "nlvr/vqa/Results/OpenEnded_mscoco_val2014__results.json"]


with open(anns_files[0],'r') as f:
    anns_js = json.load(f)
    anns_js["data_subtype"] = "all"
    print("ann_num1=", len(anns_js["annotations"]))

with open(anns_files[1],'r') as f:
    anns_js["annotations"] = anns_js["annotations"] + (json.load(f)["annotations"])
    print("ann_num2=", len(anns_js["annotations"]))

with open(question_files[0],'r') as f:
    q_js = json.load(f)
    q_js["data_subtype"] = "all"
    print("q_num1=", len(q_js["questions"]))

with open(question_files[1],'r') as f:
    q_js["questions"] = q_js["questions"] + (json.load(f)["questions"])
    print("q_num2=", len(q_js["questions"]))

with open(answer_files[0],'r') as f:
    a_js = json.load(f)
    print("answer num1=", len(a_js))

with open(answer_files[1],'r') as f:
    a_js = a_js + json.load(f)
    print("answer num1=", len(a_js))



with open("nlvr/vqa/Annotations/mscoco_all_annotations.json", 'w') as f:
    json.dump(anns_js, f)

with open("nlvr/vqa/Questions/OpenEnded_mscoco_all_questions.json", 'w') as f:
    json.dump(q_js, f)

with open("nlvr/vqa/Results/OpenEnded_mscoco_all__results.json", 'w') as f:
    json.dump(a_js, f)

