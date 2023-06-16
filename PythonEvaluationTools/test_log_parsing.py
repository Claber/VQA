import re
rationals_log_path = "/home/wolfe/Downloads/ok_vqa_rational_retrieval_log"
image_pattern = "/home/taoli1/\.conda/envs/lavis/lib/python3\.8/site-packages/lavis/datasets/data/coco/images/[a-z,0-9]{7,10}/COCO_[a-z,0-9_]{20,100}.jpg"
text_pattern = "'text': '\[.*\},\), 'newidx2sim"
id_order = "'newidx2sim: ', .*newidx2sim after:  .*"
rationals_dict = {}
rationals_dict_1 = {}
with open(rationals_log_path, 'r') as f:
    
    for l in f:
       
        m1 = re.search(image_pattern, l)
        m2 = re.search(text_pattern, l)
        m3 = re.search(id_order, l)
        image_file_name = m1.group(0).split('/')[-1]
        image_id = image_file_name.split("_")[-1].split(".")[0]
        text = m2.group(0).split(']')[-2].split('[')[1]
        question = text.split("\\', \"")[0].split("\\'")[-1]
        order1 = m3.group(0).split("])newidx2sim after: ")[-2].split("[")[-1].split(",")
        top2 = order1[0:2]
        # print(['a'] *  30)
        # print(int(image_id))
        # print(question)
        # print(image_file_name)
        # print(text)
        # print(question)
        # print(order1, top2)
        # print (l)

        rationals_dict[(question, int(image_id))] = (image_file_name, text, order1, top2)
        rationals_dict_1[int(image_id)] =  (question, image_file_name, text, order1, top2)
        # print((question, int(image_id)), (image_file_name, text, order1, top2))
print(len(rationals_dict_1), len(rationals_dict))
        