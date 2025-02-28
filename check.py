import json
from collections import Counter

with open("evaluation_results_enhanced_ver2.json", "r", encoding="utf-8") as f:
    evaluation_results = json.load(f)

# 평가 항목별 점수 카운터 초기화
score_counters = {
    "지원 동기 및 진정성": Counter(),
    "논리적 표현력": Counter(),
    "활동경험": Counter(),
    "성실성(성의)": Counter(),
}

# 전체 점수 카운터
total_scores = Counter()

# 각 지원자의 평가 결과를 분석
for result in evaluation_results:
    if "evaluation_result" in result:
        for category, data in result["evaluation_result"].items():
            if "score" in data:
                score = data["score"]
                score_counters[category][score] += 1
                total_scores[score] += 1

# 결과 출력
print("=== 평가 항목별 점수 분포 ===")
for category, counter in score_counters.items():
    print(f"\n{category}:")
    for score in ["A", "B", "C", "G", "P", "NP"]:
        count = counter.get(score, 0)
        print(f"  {score}: {count}명")

print("\n=== 전체 점수 분포 ===")
for score in ["A", "B", "C", "G", "P", "NP"]:
    count = total_scores.get(score, 0)
    print(f"{score}: {count}개")

# 지원자 수 출력
print(f"\n총 지원자 수: {len(evaluation_results)}명")
