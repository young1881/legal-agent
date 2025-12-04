from typing import List, Dict, Any
from app.services.vector_store import VectorStore

def load_sample_data(vector_store: VectorStore):
    """加载示例法律文档数据"""
    
    sample_documents: List[Dict[str, Any]] = [
        {
            "id": "xingfa-232",
            "content": "故意杀人的，处死刑、无期徒刑或者十年以上有期徒刑；情节较轻的，处三年以上十年以下有期徒刑。",
            "article_name": "中华人民共和国刑法",
            "section": "第二百三十二条",
            "doc_type": "statute",
            "source_id": "xingfa-232",
            "url": "https://example.com/xingfa#232",
            "metadata": {
                "chapter": "第四章 侵犯公民人身权利、民主权利罪",
                "effective_date": "2021-03-01"
            }
        },
        {
            "id": "xingfa-234",
            "content": "故意伤害他人身体的，处三年以下有期徒刑、拘役或者管制。犯前款罪，致人重伤的，处三年以上十年以下有期徒刑；致人死亡或者以特别残忍手段致人重伤造成严重残疾的，处十年以上有期徒刑、无期徒刑或者死刑。",
            "article_name": "中华人民共和国刑法",
            "section": "第二百三十四条",
            "doc_type": "statute",
            "source_id": "xingfa-234",
            "url": "https://example.com/xingfa#234",
            "metadata": {
                "chapter": "第四章 侵犯公民人身权利、民主权利罪",
                "effective_date": "2021-03-01"
            }
        },
        {
            "id": "xingfa-20",
            "content": "为了使国家、公共利益、本人或者他人的人身、财产和其他权利免受正在进行的不法侵害，而采取的制止不法侵害的行为，对不法侵害人造成损害的，属于正当防卫，不负刑事责任。正当防卫明显超过必要限度造成重大损害的，应当负刑事责任，但是应当减轻或者免除处罚。对正在进行行凶、杀人、抢劫、强奸、绑架以及其他严重危及人身安全的暴力犯罪，采取防卫行为，造成不法侵害人伤亡的，不属于防卫过当，不负刑事责任。",
            "article_name": "中华人民共和国刑法",
            "section": "第二十条",
            "doc_type": "statute",
            "source_id": "xingfa-20",
            "url": "https://example.com/xingfa#20",
            "metadata": {
                "chapter": "第二章 犯罪",
                "effective_date": "2021-03-01"
            }
        },
        {
            "id": "minshi-8",
            "content": "民事主体从事民事活动，不得违反法律，不得违背公序良俗。",
            "article_name": "中华人民共和国民法典",
            "section": "第八条",
            "doc_type": "statute",
            "source_id": "minshi-8",
            "url": "https://example.com/minshi#8",
            "metadata": {
                "chapter": "第一章 基本规定",
                "effective_date": "2021-01-01"
            }
        },
        {
            "id": "minshi-122",
            "content": "因他人没有法律根据，取得不当利益，受损失的人有权请求其返还不当利益。",
            "article_name": "中华人民共和国民法典",
            "section": "第一百二十二条",
            "doc_type": "statute",
            "source_id": "minshi-122",
            "url": "https://example.com/minshi#122",
            "metadata": {
                "chapter": "第三编 合同",
                "effective_date": "2021-01-01"
            }
        },
        {
            "id": "minshi-1179",
            "content": "侵害他人造成人身损害的，应当赔偿医疗费、护理费、交通费、营养费、住院伙食补助费等为治疗和康复支出的合理费用，以及因误工减少的收入。造成残疾的，还应当赔偿辅助器具费和残疾赔偿金；造成死亡的，还应当赔偿丧葬费和死亡赔偿金。",
            "article_name": "中华人民共和国民法典",
            "section": "第一千一百七十九条",
            "doc_type": "statute",
            "source_id": "minshi-1179",
            "url": "https://example.com/minshi#1179",
            "metadata": {
                "chapter": "第七编 侵权责任",
                "effective_date": "2021-01-01"
            }
        },
        {
            "id": "case-001",
            "content": "张三因与李四发生口角，持刀将李四刺伤，致李四重伤。法院认定张三构成故意伤害罪，判处有期徒刑五年。法院认为，张三主观上具有伤害他人的故意，客观上实施了伤害行为并造成重伤后果，符合故意伤害罪的构成要件。",
            "article_name": "典型案例",
            "section": "案例001",
            "doc_type": "case",
            "source_id": "case-001",
            "url": "https://example.com/cases#001",
            "metadata": {
                "case_type": "刑事",
                "court": "某市中级人民法院",
                "date": "2023-05-15"
            }
        },
        {
            "id": "case-002",
            "content": "王五在夜间回家途中，遭遇持刀抢劫。王五在反抗过程中，将抢劫犯打伤。法院认定王五的行为属于正当防卫，不负刑事责任。法院认为，王五面临正在进行的不法侵害，采取防卫行为是必要的，且未明显超过必要限度。",
            "article_name": "典型案例",
            "section": "案例002",
            "doc_type": "case",
            "source_id": "case-002",
            "url": "https://example.com/cases#002",
            "metadata": {
                "case_type": "刑事",
                "court": "某市人民法院",
                "date": "2023-08-20"
            }
        }
    ]
    
    vector_store.add_documents(sample_documents)

