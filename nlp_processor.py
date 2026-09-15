# nlp_processor.py
import json
import re
from typing import List, Tuple
import config
from logger import logger

llm = None
chain = None

def _init_llm():
    global llm, chain
    if config.USE_MOCK_LLM:
        logger.info("Mock LLM mode")
        return False
    try:
        from langchain_core.prompts import PromptTemplate
        from langchain_community.llms import Tongyi
        llm = Tongyi(model=config.LLM_MODEL, temperature=config.TEMPERATURE, api_key=config.DASHSCOPE_API_KEY)
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""你是一个专业的知识图谱抽取引擎。请从以下文本中抽取实体和关系。
要求：
1. 实体类型：人名、地名、组织名、时间、产品名等
2. 关系类型：任职、位于、产出、研发、收购、创始人、成立时间、总部地点等
3. 输出严格的JSON数组格式：[["实体1", "关系", "实体2"], ...]
4. 如果没有明确关系，返回空数组[]

示例：
文本："苹果公司CEO蒂姆·库克宣布在加州发布iPhone15"
输出：[["蒂姆·库克", "任职于", "苹果公司"], ["苹果公司", "位于", "加州"], ["苹果公司", "发布", "iPhone15"]]

文本：{text}
输出（仅输出JSON数组）："""
        )
        chain = prompt | llm
        logger.info("LLM initialized")
        return True
    except Exception as e:
        logger.error(f"LLM init failed: {e}")
        return False

_HAS_REAL_LLM = _init_llm()

def _extract_json_array(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        return text
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(pattern, text)
    if matches:
        return matches[-1].strip()
    start = text.find("[")
    if start == -1:
        return ""
    stack = []
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "[" and (i == 0 or text[i-1] != "\\"):
            stack.append(i)
        elif ch == "]" and (i == 0 or text[i-1] != "\\"):
            if stack:
                stack.pop()
                if not stack:
                    return text[start:i+1]
    return ""

def extract_triples(text: str) -> List[Tuple[str, str, str]]:
    if not text:
        return []
    if len(text) > config.MAX_TEXT_LENGTH:
        text = text[:config.MAX_TEXT_LENGTH]
    if config.USE_MOCK_LLM or not _HAS_REAL_LLM:
        # mock logic
        text_lower = text.lower()
        if "苹果" in text_lower:
            return [["苹果公司", "发布", "iPhone"], ["蒂姆·库克", "任职于", "苹果公司"]]
        if "阿里" in text_lower:
            return [["阿里巴巴", "创始人", "马云"], ["阿里巴巴", "总部", "杭州"]]
        return [["人工智能", "研究领域", "机器学习"], ["深度学习", "子领域", "神经网络"]]
    try:
        response = chain.invoke({"text": text})
        json_str = _extract_json_array(response)
        if not json_str:
            return []
        triples = json.loads(json_str)
        valid = []
        for item in triples:
            if isinstance(item, list) and len(item) == 3:
                e1, r, e2 = str(item[0]).strip(), str(item[1]).strip(), str(item[2]).strip()
                if e1 and r and e2:
                    valid.append([e1, r, e2])
        return valid
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        return []