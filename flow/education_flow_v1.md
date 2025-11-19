# 教育フロー v2.0（teacher / mext / license）

このプロジェクトは、AIロールに対して「作業コンセプト」を教え、
それを文科省的に監査し、免許としてロールに付与するための仕組みを提供する。

## 対象となるエージェント

- teacher_agent
- mext_agent
- license_agent

## フロー概要

1. **Concept生成 (Stage 1)**
   - teacher_agent が、指定された作業コンセプト名（例: DocDD）について、
     Conceptテンプレート(YAML)を埋めたドラフトを生成する。

2. **制度監査 (Stage 2)**
   - mext_agent が Conceptドラフトを読み取り、
     8つの評価項目について0〜2点で採点。
   - 合計点とともに「approved / needs_revision / rejected」を返す。
   - needs_revision / rejected の場合は teacher_agent に差し戻し、
     teacher_agent が修正版Conceptを再生成する。
   - approved になるまで 1 ↔ 2 をループ。

3. **免許定義 (Stage 3)**
   - approved となったConceptに対し、license_agent が License定義を生成する。
   - Licenseには、免許ID、対応ドメイン、初期スコア、有効期限の目安、
     加点条件・減点条件・免停/剥奪条件などが含まれる。

4. **今後の拡張（v1では未実装）**
   - ロール(実働エージェント)に免許を紐づけ、
     実務ログからスコア更新を行う。
   - クライアントペルソナとの対話ログから作業コンセプトを改良する。
   - 書籍からの理論をぶつけて、ロールが理論を超えた場合は加点する。
   - MCPや外部ツールを接続して実プロジェクトに適用していく。
