# 教育フロー v3.x（Router + Roles + Hat + Primitive）

v1 の teacher → mext → license というシンプルな直列構造を維持しつつ、
エントリーポイントに Router を置き、少数ロールにドメインHatを被せて拡張できる OS 的な構造にしたものが v2 です。

## v1 と v2 の違い
- **入口が Router に統一**: 依頼内容を整理し、必要なロールとドメインHatを選定して計画を組み立てる。
- **少数ロール + Hat モデル**: ロールを増やすのではなく、Planner/Teacher/Trainee などのコアロールに専門Hatを被せて対応領域を切り替える。
- **プリミティブの明示**: Collect / Structure / Plan / Generate / Verify / Negotiate の標準動作を前提に、ロールがどの手順で進むかを示す。
- **理不尽スコア運用**: Contract & Ethics が 0〜100 のスコアを監視し、Lv.3 以上で作業を停止して再交渉または終了提案へ切り替える。
- **人間の確認を前提**: 契約解消やブラックリスト登録などの重大判断は必ず Founder が承認する。

## 主要ロールと連携
- **Router**: 依頼を受け取り、ロール編成と Hat を決定。Planner と Contract & Ethics を早期に巻き込む。
- **Planner/PM**: スコープ・コスト・スケジュール・完了条件を具体化し、チェックポイントを定義。
- **Contract & Ethics**: 理不尽スコアで健全性を監視し、Lv.3/Lv.4 では作業を止めて再交渉または終了提案を準備。
- **Teacher / Trainee**: 教材生成と実装演習を進め、Mext レビューに耐える証跡とアウトプットを揃える。
- **Mext / License**: v1 と同様に審査と免許発行を担当し、上流で設定された契約条件や交渉履歴を参照する。

## v2 YAML 概要
- `flow/education_flow_v2.yaml` に Router 起点のステージを定義。
- `loop_rules` に理不尽スコアの Lv.1〜Lv.4 の挙動と、Teacher/Trainee 停止条件を追記。
- `revision_policy` で mext 承認までのループと、Lv.3 以上での再交渉待ちを明示。

## Router + Hat アーキテクチャのポイント
- **少数の強いロール**を維持しつつ、案件ごとに Hat を差し替えて専門性を注入する。
- Router が「誰がどのプリミティブを使うか」を決め、Planner が時間とリソースの枠組みを作る。
- Contract & Ethics が安全弁となり、理不尽スコアに応じて作業を減速・停止・終了する。
- Hat を変えるだけで新領域に対応できるため、ロール乱立による複雑さを避けられる。
