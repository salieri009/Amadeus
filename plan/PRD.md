# 📝 Project Amadeus: Product Requirements Document (PRD)

| 항목 | 내용 |
| :--- | :--- |
| **프로젝트명** | Amadeus (아마데우스) |
| **버전** | v1.0 (MVP: Minimum Viable Product) |
| **작성자** | Jungwook (DevOps Engineer) |
| **상태** | 기획 단계 (Planning) |
| **목표** | "Reactive(반응형)에서 **Predictive(예측형)**로, Manual(수동)에서 **Autonomous(자율)**로 진화하는 인프라 시스템 구축" |

## 1. 배경 및 목적 (Background & Goals)

### 1.1 문제 정의 (The Pain)
- 기존의 Kubernetes HPA(Horizontal Pod Autoscaler)는 CPU가 80%를 넘어야만 반응함. 즉, 스케일링이 완료될 때까지 사용자는 느린 속도를 견뎌야 함 (Latency Spike).
- 새벽에 장애가 발생하면 엔지니어가 직접 일어나서 로그를 보고 서버를 재시작해야 함.

### 1.2 솔루션 (The Solution)
- **Deep Learning(LSTM)**이 **공개 데이터셋(Public Dataset, 예: NASA/Google Trace)**으로 일반적인 부하 패턴을 사전 학습(Pre-train)하고, 실제 환경의 실시간 트래픽으로 **미세 조정(Fine-tuning)**하여 예측 정확도를 확보.
- 부하가 오기 10분 전에 미리 서버를 확장하여 Latency Spike를 원천 차단.
- 장애 로그 패턴을 감지하여 사람의 개입 없이 즉시 자율 복구(Self-Healing)를 수행함.

## 2. 사용자 페르소나 (Target Persona)
- **Primary**: 정욱 (주니어 DevOps 엔지니어)
- **니즈**: 반복적인 장애 대응 업무를 줄이고, "AI를 활용한 인프라 운영 경험"을 포트폴리오에 넣고 싶음.
- **목표**: 밤에 알람 소리에 깨지 않고 숙면을 취하는 것.

## 3. 핵심 기능 명세 (Functional Requirements)
이 프로젝트는 크게 **두 가지 뇌(Brain)**와 **하나의 손(Hand)**으로 구성됩니다.

### 3.1 기능 A: Predictive Scaling (예언가)
- **Input**: Prometheus에서 수집한 최근 60분간의 CPU, Memory, Request Count 시계열 데이터.
- **Model**: LSTM (Long Short-Term Memory) 기반의 시계열 예측 모델.
- **Action**: 향후 10분 뒤 예상 부하량을 계산 → 필요 Pod 개수 산출 → `kubectl scale` 미리 실행.
- **성공 기준**: 트래픽 스파이크 발생 시 응답 지연(Latency) 증가율 10% 미만 유지.

### 3.2 기능 B: Self-Healing (의사)
- **Input**: 실시간 애플리케이션 Error Log 및 Pod 상태(Status).
- **Logic**:
    - **Case 1**: OOMKilled (메모리 부족) 감지 → 해당 Pod의 메모리 Limit을 20% 상향 조정하여 재배포.
    - **Case 2**: CrashLoopBackOff 감지 → 이전 버전 이미지로 자동 롤백(Rollback).
- **Action**: Kubernetes API를 통해 설정 변경(Patch) 및 재배포.

### 3.3 기능 C: Intelligent Dashboard & Alert (인터페이스)
- **Visual**: Grafana 대시보드에 **[실제 트래픽]**과 **[AI 예측 트래픽]**을 겹쳐서 표시.
- **Notify**: Slack으로 "Amadeus: 미래 부하 감지됨. 서버 3대 증설 완료." 메시지 전송.

## 4. 시스템 아키텍처 (System Architecture)
전체 시스템은 Kubernetes 클러스터 내부에서 Loop(순환) 구조로 작동합니다.
1. **Observe (관찰)**: Prometheus가 Pod의 상태를 계속 수집.
2. **Think (판단)**: Python으로 작성된 Amadeus Operator가 데이터를 가져와 LSTM 모델에 넣고 추론.
3. **Act (실행)**: 결정된 사항(Scale Out 또는 Restart)을 K8s API Server에 명령.

## 5. 기술 스택 (Tech Stack)

| 구분 | 기술 | 선정 이유 |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | AI 라이브러리(PyTorch)와 K8s 제어(Client) 모두 최적화. |
| **AI Core** | PyTorch | UTS 수업 연계. LSTM 모델 구현 용이. |
| **Infra** | Kubernetes | CKA 자격증 연계. 컨테이너 오케스트레이션 표준. |
| **Data** | Prometheus | 시계열 데이터 수집 표준 도구. |
| **Target App** | Google Online Boutique | 구글의 마이크로서비스 표준 데모. 실제 이커머스 로직(결제, 장바구니 등) 기반 트래픽 생성. |
| **Load Test** | Locust | 단순 랜덤 요청이 아닌 **실제 사용자 행동 시나리오(User Journey)** 기반의 부하 생성. |
| **Interface** | Slack API | 운영 알림 발송용. |

## 6. 개발 로드맵 (Milestones)
정욱님의 학기 일정에 맞춘 단계별 계획입니다.

- **Phase 1 (Real-World 데이터 환경 구축)**: `Online Boutique` 데모 앱 배포 및 `Locust`로 실제 사용자 패턴(Daily Cycle, Flash Sale 등) 스크립팅 & 데이터 수집. (1주 차)
- **Phase 2 (하이브리드 두뇌 만들기)**: 공개 데이터셋으로 기본 패턴을 사전 학습(Pre-train) 시키고, Phase 1 데이터로 Fine-tuning 하여 실무 적용성 강화. (2~3주 차)
- **Phase 3 (손과 발 연결)**: Python 코드로 K8s Pod 개수 조절하는 로직(Controller) 개발. (4주 차)
- **Phase 4 (통합 및 시각화)**: 전체 시스템 합체 & Grafana/Slack 연동. (5주 차~)
