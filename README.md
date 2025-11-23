# ai-role-education

AI ロール教育のためのプロンプト、フロー定義、サンプルデータをまとめたリポジトリです。LLM 呼び出しや外部サービス連携は含まれていないため、あくまで資料・テンプレート集としてそのまま利用できます。

## 含まれているもの（現状）
- **ロールプロンプト**: Router / Planner(PM) / Contract & Ethics / Teacher / Trainee / MEXT / License / Judge などの v3 世代ドキュメントが `roles/` 配下にあります。
- **教育フロー定義**: 直列の v1 と、Router を入り口にした v2 をそれぞれ Markdown と YAML で収録しています (`flow/education_flow_v1.*`, `flow/education_flow_v2.*`)。
- **コンセプトデータ**: `concepts/<concept_id>/` に concept・mext_review・license の各 YAML をバージョン付きで保存しています（api_dd / audit_dd / ddd / docdd / infra_dd / metricdd / opsdd / riskdd / tdd / uxdd）。
- **設定ファイル**: クレジット配分 (`config/credit_policy.yaml`) と天候パターン (`config/weather_config.yaml`) を用意しています。
- **簡易ヘルパー**: 天候の可否判定クラス（`environment.py`）、再教育キューのスタブ（`judge_system.py`）、ロールバージョン管理のパス生成ヘルパー（`role_paths.py`）。
- **動作サンプルスクリプト**: `scripts/run_flow.py` でフローとコンセプトの読み書きだけを試せます（LLM 生成は未実装）。
- **その他**: `case_law/` は判例データのプレースホルダ、`logs/` はローカル実行時のログ出力先です。

## リポジトリ構成
```
ai-role-education/
├─ roles/              # 各ロールのプロンプト (v3 世代の md ファイル)
├─ flow/               # education_flow_v1/v2 の説明と YAML 定義
├─ concepts/           # コンセプトごとの versioned YAML（concept / mext_review / license）
├─ config/             # クレジット・天候設定
├─ scripts/            # 簡易実行スクリプト（LLM 呼び出しは未実装）
├─ environment.py      # 天候クラスと参加可否判定
├─ judge_system.py     # 再教育キューのスタブ実装
├─ role_paths.py       # ロールのバージョンディレクトリ補助
├─ logs/               # ローカル実行ログ（存在しない場合は自動生成）
└─ case_law/           # 判例データの空ディレクトリ
```

## フロー定義の概要
- **education_flow_v1**: teacher → mext → license の直列フロー。`flow/education_flow_v1.md` と `flow/education_flow_v1.yaml` に詳細があります。
- **education_flow_v2**: Router を入口とし、Planner/Contract & Ethics/Teacher/Trainee を経由する発展版。`flow/education_flow_v2.md` と `flow/education_flow_v2.yaml` にステージと入出力の対応をまとめています。

## サンプルスクリプトの使い方
`python scripts/run_flow.py --concept-id <id>` で指定コンセプトの最新バージョンを読み、次バージョンの concept/mext_review/license を作成して `logs/education_sessions.md` に履歴を追記します。

- LLM 生成部分 (`call_teacher_agent` / `call_mext_agent` / `call_license_agent`) は `NotImplementedError` なので、実際には既存 YAML を複製し、レビューとライセンスは最小のプレースホルダを出力します。
- 事前に `concepts/<id>/concept_v*.yaml` が存在しない場合は失敗します。

```bash
python scripts/run_flow.py --concept-id docdd --flow flow/education_flow_v2.yaml
```

## 設定・ヘルパーの利用イメージ
- `config/credit_policy.yaml`: 初期クレジット、進化コスト、成功報酬やペナルティ係数を管理するためのサンプルデータ。
- `config/weather_config.yaml` + `environment.py`: 天候ごとに強度・混沌度・報酬補正と参加必要クレジットを持ち、`WeatherSystem.can_join()` で参加可否を判定します。
- `judge_system.py`: 再教育キューの同時処理上限やタイムアウト（48 時間）をスタブ実装しています。
- `role_paths.py`: `roles/active` と `roles/archive` をまたぐロールバージョンディレクトリの生成に使うユーティリティです。

## 現時点の前提と制約
- このリポジトリはドキュメントとテンプレート集であり、エージェント実行環境や API は含まれていません。
- `case_law/` や `logs/` はプレースホルダ扱いで、必要に応じてローカルで追加します。
- ライセンス表記は特に設けていません（プロンプトや YAML を自分の実験用途で自由に拡張する想定）。
