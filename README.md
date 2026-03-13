# Computer Vision Dataset Automation Toolkit

컴퓨터 비전 데이터셋 준비 과정에서 자주 발생하는 작업들을 자동화하기 위한 CLI 기반 Python 유틸리티 모음입니다.

이 프로젝트는 이미지 데이터셋 검증, 손상되거나 중복된 파일 정리, 메타데이터 생성, 통계 분석 및 시각화까지의 과정을 자동화하는 모듈형 도구들을 제공합니다.

실제 머신러닝 및 컴퓨터 비전 데이터 파이프라인에서 사용되는 데이터 엔지니어링 워크플로우를 구현하는 것을 목표로 합니다.

---

# 주요 기능

- 이미지 데이터셋 검증
- 손상된 파일 및 중복 파일 자동 정리
- SHA256 해시 기반 정확한 중복 이미지 탐지
- 이미지 데이터셋 메타데이터 자동 생성
- 데이터셋 통계 및 시각화 생성
- 모듈형 CLI 기반 유틸리티 구조
- 재현 가능한 워크플로우를 위한 구조화된 출력 디렉토리

---

# 프로젝트 구조

```
cv-dataset-automation-toolkit
│
├── image_validator.py
├── dataset_cleaner.py
├── metadata_generator.py
├── dataset_stats.py
│
├── utils
│   ├── file_utils.py
│   ├── image_utils.py
│   ├── logging_utils.py
│   └── path_utils.py
│
├── sample_dataset
│   ├── images
│   └── annotations
│
├── outputs
│   ├── logs
│   ├── reports
│   ├── metadata
│   └── stats
│
├── quarantine
│
├── requirements.txt
└── README.md
```

---

# 데이터 처리 파이프라인

이 툴킷은 모듈형 데이터 파이프라인 구조로 설계되었습니다.

```
Raw Dataset
     │
     ▼
image_validator.py
     │
     ▼
validation_report.csv
     │
     ▼
dataset_cleaner.py
     │
     ▼
Clean Dataset
     │
     ▼
metadata_generator.py
     │
     ▼
metadata.csv
     │
     ▼
dataset_stats.py
     │
     ▼
Statistics + Visualizations
```

각 단계는 필요에 따라 독립적으로 실행할 수 있습니다.

---

# 설치 방법

저장소를 클론합니다.

```bash
git clone <repository-url>
cd cv-dataset-automation-toolkit
```

가상 환경을 생성합니다.

```bash
python -m venv venv
source venv/bin/activate
```

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

---

# 사용 방법

데이터셋 이미지를 다음 디렉토리에 배치합니다.

```
sample_dataset/images
```

---

# 1. 이미지 데이터셋 검증

이미지 파일의 무결성과 지원되는 형식을 검사합니다.

```bash
python image_validator.py --input sample_dataset/images
```

출력 결과

```
outputs/reports/validation_report.csv
outputs/logs/validation.log
```

검증 리포트에는 다음 정보가 포함됩니다.

- 파일 경로
- 검증 상태
- 이미지 해상도
- 오류 유형

---

# 2. 데이터셋 정리

손상된 파일, 지원되지 않는 파일, 중복 파일을 quarantine 디렉토리로 이동합니다.

예시 실행:

```bash
python dataset_cleaner.py \
  --input sample_dataset/images \
  --remove-unsupported \
  --remove-corrupted \
  --deduplicate
```

출력 결과

```
quarantine/invalid/
quarantine/duplicates/
outputs/logs/dataset_cleaner.log
```

중복 파일 탐지는 **SHA256 파일 해시 기반으로 동일한 파일을 정확히 탐지**합니다.

---

# 3. 메타데이터 생성

유효한 이미지로부터 메타데이터를 추출합니다.

```bash
python metadata_generator.py \
  --input sample_dataset/images \
  --output-json outputs/metadata/metadata.json
```

출력 결과

```
outputs/metadata/metadata.csv
outputs/metadata/metadata.json
outputs/logs/metadata_generator.log
```

생성되는 메타데이터에는 다음 정보가 포함됩니다.

- 이미지 너비
- 이미지 높이
- 채널 수
- 파일 크기
- 종횡비
- 이미지 읽기 가능 여부

---

# 4. 데이터셋 통계 생성

데이터셋 메타데이터를 기반으로 통계 분석과 시각화를 생성합니다.

```bash
python dataset_stats.py \
  --input-csv outputs/metadata/metadata.csv
```

출력 결과

```
outputs/stats/dataset_summary.json

outputs/stats/width_distribution.png
outputs/stats/height_distribution.png
outputs/stats/aspect_ratio_distribution.png
outputs/stats/file_size_distribution.png
outputs/stats/channel_distribution.png
```

이 시각화들은 데이터셋의 분포와 특성을 이해하는 데 도움이 됩니다.

---

# 출력 디렉토리 구조

모든 결과물은 구조화된 출력 디렉토리에 저장됩니다.

```
outputs
├── logs
├── reports
├── metadata
└── stats
```

이 구조는 데이터 처리 워크플로우를 재현 가능하게 유지하는 데 도움을 줍니다.

---

# 사용 기술

이 프로젝트에서 사용된 주요 기술은 다음과 같습니다.

- Python 3
- OpenCV
- pandas
- numpy
- matplotlib
- tqdm

사용된 Python 표준 라이브러리:

- argparse
- pathlib
- shutil
- hashlib
- logging

---

# 활용 사례

이 툴킷은 다음과 같은 작업에 활용할 수 있습니다.

- 컴퓨터 비전 학습용 데이터셋 준비
- 대규모 이미지 컬렉션 정리
- 데이터셋 메타데이터 생성 및 분석
- 중복 이미지 탐지
- 데이터셋 분포 분석 및 시각화

---

# 향후 개선 방향

향후 다음과 같은 기능을 추가할 수 있습니다.

- perceptual hashing 기반 유사 이미지 탐지
- annotation 파일 검증 도구
- 학습 / 검증 / 테스트 데이터 자동 분할
- 병렬 이미지 처리
- COCO, YOLO 등 데이터셋 포맷 지원

---

# License

이 프로젝트는 교육 및 포트폴리오 목적을 위해 제작되었습니다.

---

# Author

Computer Vision Dataset Automation Toolkit  
Machine Learning 워크플로우를 위한 Python 기반 데이터셋 엔지니어링 도구
