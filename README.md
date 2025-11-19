# ai-role-education

このリポジトリには、**AIロール教育システム**の最初のバージョンが含まれています。
職業訓練校 + 教育省 + 免許事務所の流れをシミュレートし、AIエージェントに
実践的な業務コンセプトを教え、再現性があり監査可能なプロセスで認証します。

`v1` の範囲では次の3つのロールにフォーカスしています。

- **teacher_agent** — 厳格なYAMLテンプレートに沿ってコンセプトを起草します。
- **mext_agent** — 8つの評価軸でコンセプトを査読し、承認・再提出・却下を判断します。
- **license_agent** — 承認済みコンセプトごとにライセンス定義を設計し、他のAIロールに
  測定可能な資格を付与できるようにします。

## リポジトリ構成

```
ai-role-education/
├─ README.md
├─ concepts/
│  └─ docdd/
│     ├─ concept_v1.yaml
│     ├─ mext_review_v1.yaml
│     └─ license_v1.yaml
├─ flow/
│  ├─ education_flow_v1.md  # フロー解説（文章）
│  └─ education_flow_v1.yaml  # 実行用の構造化定義
├─ personas/
│  └─ schema.yaml
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

## はじめに

1. `roles/` にある**各種プロンプト**を確認します。各AIロール向けのそのまま使える指示テンプレートです。
2. **教育フロー**（`flow/education_flow_v1.md`）を読み、teacher → mext → license の連携手順を理解します。
3. `concepts/docdd/` の **DocDDサンプルコンセプト** を参照し、コンセプト／レビュー／ライセンスの期待YAML構造を把握します。
4. **ヘルパースクリプト**を使って現在の状態をプレビューします（`PyYAML` が必要）：

   ```bash
   python scripts/run_flow.py --concept concepts/docdd/concept_v1.yaml --license concepts/docdd/license_v1.yaml
   ```

   スクリプトは要約を表示し、エージェントを実行する前に必須フィールドが揃っているか検証します。

## 現在のコンセプト一覧

- **DocDD（Document Driven Development）** — `concepts/docdd/`
  - `concept_v1.yaml`: 実装開始前に要件を文書化し、関係者が同じ参照情報を共有するプラクティスを定義しています。
  - `mext_review_v1.yaml`: 合計スコア14/16で**承認**、次版ではアンチパターン対策と失敗ケースの根本原因をより詳しく求めています。
  - `license_v1.yaml`: DocDDライセンスを定義し、ソフトウェア開発チーム向けに50ポイント開始・90日ごとのレビュー・詳細な評価/停止/失効ルールを示します。

## 教育フローの運用

### 新しい `concept_id` を追加する

1. **準備**: `roles/` の3つのロールプロンプトと、`flow/education_flow_v1.md` の正準フロー説明を読み、必要なYAML構造とレビュー手順を理解します。
2. **コンセプトを起草（teacher_agent）**: `concepts/<concept_id>/` を作成し、DocDDテンプレートを参考に `concept_v1.yaml` を新しいプラクティスで埋めます。
3. **コンセプトを監査（mext_agent）**: 下書きを8つの評価軸で審査し、`mext_review_v1.yaml` を作成して承認・要修正・却下を判断します。承認されない場合は、コメントが解決されるまでteacherと反復します。
4. **ライセンスを発行（license_agent）**: 承認後、同じコンセプト用の `license_v1.yaml` を作成し、対象領域・スコアリングルール・有効期間・執行条件を定義します。

### 既存の `concept_id` を更新する

1. **最新ファイルを確認**（`concept_vN.yaml`、`mext_review_vN.yaml`、`license_vN.yaml`）し、これまでの指摘とライセンス制約を把握します。
2. **改訂案を作成**（`concept_vN+1.yaml`）し、レビューでの指摘や新たに得た運用知見を反映します。
3. **再監査**: `mext_review_vN+1.yaml` を作成し、teacherフェーズと数回ループして最終的に**承認**されるまで繰り返します。
4. **ライセンス更新**（`license_vN+1.yaml`）は、コンセプト変更が認証要件に影響する場合のみ行い、コミット前にスクリプトや手動チェックを再実行します。

## システム拡張のアイデア

- DocDD構造を複製し、IDを更新して新たなコンセプトを追加します。
- teacher ↔ mext ループを自動化するCLIツール（OpenAI APIや他のオーケストレーターなど）を構築し、出力を `logs/` に保存します。
- ライセンスに高度なスコアリングや実運用テレメトリを組み込みます。
- v2に向けて、クライアントペルソナ、自動カリキュラムビルダー、MCP連携などのアクターを追加します。

## ライセンス

このリポジトリはドキュメントとサンプルデータに特化しています。AI実験プロジェクト内で自由に利用・拡張してください。
