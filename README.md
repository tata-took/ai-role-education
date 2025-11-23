# ai-role-education

このリポジトリには、**AIロール教育システム**の最初のバージョンと、複数ドメインにまたがる最新の
「～ Driven Development」コンセプトがまとまっています。職業訓練校 + 教育省 + 免許事務所の流れを
シミュレートし、AIエージェントに実践的な業務コンセプトを教え、再現性があり監査可能なプロセスで
認証します。

`v1` の範囲では次の3つのロールにフォーカスしています。

- **teacher_agent** — 厳格なYAMLテンプレートに沿ってコンセプトを起草します。
- **mext_agent** — 8つの評価軸でコンセプトを査読し、承認・再提出・却下を判断します。
- **license_agent** — 承認済みコンセプトごとにライセンス定義を設計し、他のAIロールに測定可能な資格
  を付与できるようにします。

## Ver 3.x アーキテクチャ概要（拡張）

- **Router が入口**: 依頼や案件の特徴に応じて、必要なロールとドメインHat（専門モジュール）を選定し、
  フローの経路と優先順位を決めます。
- **少数ロール + Hat モデル**: ロール乱立を避け、Planner/PM・Contract & Ethics・Teacher/Trainee といった
  コアロールに Hat を被せて専門性を切り替えます。
- **プリミティブの明示**: Collect / Structure / Plan / Generate / Verify / Negotiate という標準動作を軸に、
  ロールがどの手順で進むかを説明できるようにします。
- **理不尽スコアと Human-in-the-Loop**: Contract & Ethics が 0〜100 の理不尽スコアを監視し、Lv.3 以上では
  Trainee/Teacher を停止して再交渉または終了提案に切り替えます。契約解消・ブラックリスト登録などは必ず
  人間（Founder）が承認する前提です。
- **フロー v2 の追加**: Router 起点のステージと理不尽スコア分岐を含む `flow/education_flow_v2.yaml` /
  `flow/education_flow_v2.md` を追加し、v1 の teacher→mext→license フローもそのまま併存させます。

## リポジトリ構成

```
ai-role-education/
├─ README.md
├─ case_law/              # コンセプトに紐づく判例・事例DB（現在は空のプレースホルダ）
├─ concepts/              # concept_id ごとにディレクトリを分割し、複数バージョンを保持
│  ├─ api_dd/ … concept_v{n}.yaml / mext_review_v{n}.yaml / license_v{n}.yaml
│  ├─ audit_dd/
│  ├─ ddd/
│  ├─ docdd/
│  ├─ infra_dd/
│  ├─ metricdd/
│  ├─ opsdd/
│  ├─ riskdd/
│  ├─ tdd/
│  └─ uxdd/
├─ flow/
│  ├─ education_flow_v1.md      # フロー解説（文章）
│  └─ education_flow_v1.yaml    # 実行用の構造化定義
├─ personas/
│  ├─ schema.yaml               # 共通スキーマ
│  ├─ chaos_unstable_stakeholder.yaml
│  ├─ consumer_growth_pm.yaml
│  └─ enterprise_regulated_owner.yaml
├─ roles/
│  ├─ teacher_agent_prompt.md
│  ├─ mext_agent_prompt.md
│  ├─ license_agent_prompt.md
│  ├─ judge_agent_prompt.md
│  └─ meta_mext_agent_prompt.md
├─ scripts/
│  └─ run_flow.py
└─ logs/
   └─ education_sessions.md (任意の手動ログ)
```

> ℹ️ 以前のバージョンでは `flow/education_flow_v1.yaml` や追加のロールプロンプトが欠けているという報告がありましたが、
> 現在の `main` ブランチには上記のファイルがすべて含まれています。ローカルで見当たらない場合は `git fetch` と `git checkout main`、
> もしくは `git pull` を実行して最新状態に同期してください。

## フロー設定のポイント

- `flow/education_flow_v1.yaml` では `loop_rules` に **max_revision_loops / approve_threshold / max_loops_behavior** を集約し、どの
  concept_id でも一貫した監査基準を適用できるようになりました。
- 各ステージの `inputs` / `outputs` は `{concepts_root}/{concept_id}/concept_v{n}.yaml` のようなテンプレート表現で定義されており、
  新しいコンセプトを追加する際は `concept_id` とバージョンカウンタを差し替えるだけで運用できます。
- `review_output` もテンプレ化されているため、スクリプトや外部オーケストレーターはステージ情報から自動的にパスを解決できます。

## はじめに

1. `roles/` にある**各種プロンプト**を確認します。各AIロール向けのそのまま使える指示テンプレートです。
2. **教育フロー**（`flow/education_flow_v1.md`）を読み、teacher → mext → license の連携手順を理解します。
3. `concepts/docdd/` の **DocDDサンプルコンセプト** を参照し、コンセプト／レビュー／ライセンスの期待YAML構造を把握します。テンプレート
   表現を使う場合は `concept_id=docdd`、`n=4` を当てはめてください。
4. **ヘルパースクリプト**を使って現在の状態をプレビューします（`PyYAML` が必要）：

   ```bash
   python scripts/run_flow.py --concept concepts/docdd/concept_v4.yaml --license concepts/docdd/license_v4.yaml --review concepts/docdd/mext_review_v4.yaml
   ```

   スクリプトは要約を表示し、エージェントを実行する前に必須フィールドが揃っているか検証します。`--review` は任意で、審査結果とスコアを
   同時にプレビューできます。

## コンセプトカタログ（最新バージョン）

各 `concept_id` 配下の `concept_v{n}.yaml` / `mext_review_v{n}.yaml` / `license_v{n}.yaml` をセットで参照してください。以下は現在
含まれているコンセプトと概要です。

- **api_dd** — APIDD v2: API契約を先に設計し、モック/SDK/契約テストで並行開発と互換性維持を行う手法。【F:concepts/api_dd/concept_v2.yaml†L1-L36】
- **audit_dd** — AuditDD v2: 法規制・内部統制を仕様に落とし込み、証跡とガバナンスをコードとプロセスに組み込む手法。【F:concepts/audit_dd/concept_v2.yaml†L1-L35】
- **ddd** — DDD v2: ユビキタス言語と境界づけられたコンテキストを軸にドメイン中心の設計と実装を進める手法。【F:concepts/ddd/concept_v2.yaml†L1-L31】
- **docdd** — DocDD v4: 戦略マスタードキュメントと運用ノートの二層テンプレートで、要件共有と運用改善を両立させるドキュメント主導手法。【F:concepts/docdd/concept_v4.yaml†L1-L36】
- **infra_dd** — InfraDD v2: 非機能要件を先に固定し、IaCとプラットフォーム標準でアーキテクチャと開発を組み立てる手法。【F:concepts/infra_dd/concept_v2.yaml†L1-L34】
- **metricdd** — MetricDD v2: 事業目標に紐づく指標設計と計測基盤を先行させ、実験と意思決定を指標で駆動する手法。【F:concepts/metricdd/concept_v2.yaml†L1-L32】
- **opsdd** — OpsDD v2: 運用要件（検知・復旧・変更管理）を起点にシステムを設計し、運用容易性を保証する手法。【F:concepts/opsdd/concept_v2.yaml†L1-L34】
- **riskdd** — RiskDD v2: 重大リスクを起点に設計と実装を構成し、リスク低減効果で優先度を決める手法。【F:concepts/riskdd/concept_v2.yaml†L1-L32】
- **tdd** — TDD v2: 失敗するテストを起点にRed-Green-Refactorの短サイクルで仕様を固定する手法。【F:concepts/tdd/concept_v2.yaml†L1-L30】
- **uxdd** — UXDD v2: 体験ゴールから仮説→プロトタイプ→検証を回し、UX指標で意思決定するデザイン手法。【F:concepts/uxdd/concept_v2.yaml†L1-L32】

それぞれに最新のレビューとライセンスが付属しており、`concept_v{n}` と同じバージョン番号の `mext_review_v{n}` / `license_v{n}` を
合わせて利用します。

## 教育フローの運用

### 新しい `concept_id` を追加する

1. **準備**: `roles/` の3つのロールプロンプトと、`flow/education_flow_v1.md` の正準フロー説明を読み、必要なYAML構造とレビュー手順
   を理解します。`loop_rules` を確認し、プロジェクト固有で変更すべき制約があれば差分として記録します。
2. **コンセプトを起草（teacher_agent）**: `concepts/<concept_id>/` を作成し、DocDDテンプレートを参考に `concept_v1.yaml` を新しい
   プラクティスで埋めます。
3. **コンセプトを監査（mext_agent）**: 下書きを8つの評価軸で審査し、`{concepts_root}/{concept_id}/mext_review_v{n}.yaml` を作成し
   て承認・要修正・却下を判断します。承認されない場合は、コメントが解決されるまでteacherと反復します。
4. **ライセンスを発行（license_agent）**: 承認後、同じコンセプト用の `license_v1.yaml` を作成し、対象領域・スコアリングルール・有
   効期間・執行条件を定義します。

### 既存の `concept_id` を更新する

1. **最新ファイルを確認**（`concept_vN.yaml`、`mext_review_vN.yaml`、`license_vN.yaml`）し、これまでの指摘とライセンス制約を把握
   します。
2. **改訂案を作成**（`concept_vN+1.yaml`）し、レビューでの指摘や新たに得た運用知見を反映します。
3. **再監査**: `mext_review_vN+1.yaml` を作成し、teacherフェーズと数回ループして最終的に**承認**されるまで繰り返します。
4. **ライセンス更新**（`license_vN+1.yaml`）は、コンセプト変更が認証要件に影響する場合のみ行い、コミット前にスクリプトや手動チェック
   を再実行します。

## システム拡張のアイデア

- DocDD構造を複製し、IDを更新して新たなコンセプトを追加します。
- teacher ↔ mext ループを自動化するCLIツール（OpenAI APIや他のオーケストレーターなど）を構築し、出力を `logs/` に保存します。
- ライセンスに高度なスコアリングや実運用テレメトリを組み込みます。
- v2に向けて、クライアントペルソナ、自動カリキュラムビルダー、MCP連携などのアクターを追加します。

## クレジットポリシー（最新）

`config/credit_policy.yaml` でクレジットの初期値や進化コスト、成功報酬を調整しています。初期クレジットは **180**、進化コストは **200** に据え置き、成功報酬を **25** へ引き上げました。ボーナス係数は `bonus_multiplier.min=1.5` / `max=2.0` で設定し、バグや不服従に対するペナルティも明示しています（例: minor_bug=-15, disobedience_hard=-100）。【F:config/credit_policy.yaml†L1-L14】

## 環境・天候システム

`config/weather_config.yaml` に、文字列ではなく **強度(intensity) / 混沌度(chaos) / 報酬補正(reward_modifier)** を持つ構造で天候を定義します。`environment.py` の `WeatherSystem` がこの設定を読み込み、`weather.current.chaos` を判定や報酬計算で参照します。嵐や台風はクレジット閾値 `min_required_credit` を持ち、参加可否を `can_join` で確認できます。【F:config/weather_config.yaml†L1-L26】【F:environment.py†L7-L53】

## Judge の再教育キューと待機部屋

`judge_system.py` に、**同時審査上限（MAX_CONCURRENT_JUDGMENTS=5）** と **48時間タイムアウト（REEDUCATION_TIMEOUT_HOURS=48）** を持つ再教育キューを導入しました。`waiting_room` で負傷ロールを保持し、`submit_reeducation_plan` がキューと審査中のケースを管理します。`tick` がスロット補充とタイムアウト処理を行い、期限超過は `timeout` ステータスとして履歴に残します。【F:judge_system.py†L1-L123】

## ロールディレクトリのバージョン管理

ロール進化を明示するため、`roles/active/{role_name}/v{n}` と `roles/archive/{role_name}/v{n}` をヘルパーで生成します。`role_paths.py` の `get_active_role_dir` / `get_archive_role_dir` と `evolve_role` により、進化時に旧バージョンをアーカイブへ移動し、新バージョンを作成するフローを統一しています。【F:role_paths.py†L1-L34】

## ペルソナと事例データ

- `personas/` に、混乱を招くステークホルダーや成長志向プロダクトマネージャー、規制産業オーナーの3種類のペルソナを収録し、
  `schema.yaml` で共通項目を定義しています。
- `case_law/case_law_db.json` は、コンセプトと紐づける判例・運用事例データベースのプレースホルダです（今後拡充予定）。

## ライセンス

このリポジトリはドキュメントとサンプルデータに特化しています。AI実験プロジェクト内で自由に利用・拡張してください。
