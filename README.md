# Paper Reading Tools

两个独立的论文阅读辅助脚本：按公开链接清单下载 PDF，并渲染可能含图 1/图 2 的页面。附带十篇公开论文的标题、年份和来源链接；不包含论文文件、翻译全文、私人笔记或数模研究代码。

## 使用

需要 Python 3.10+。页面渲染另需将 Poppler 的 `pdftoppm` 安装到 PATH，也可传入完整路径。

```sh
python -m pip install -r requirements.txt
python download_papers.py --output downloads
python extract_paper_figures.py --root downloads --output figures
```

两者均支持 `--manifest other.json`；运行 `--help` 可查看参数。清单字段为 `n`（1–10）、`short`、`year`、`pdf`，可另附标题和来源页。输出按“第几篇-简称-年份/简称-原论文.pdf”整理。

图表识别仅用 PDF 文本关键词定位并渲染整页，不会智能裁图；扫描件及不同排版可能识别失败。下载源可能改变或限制访问；已有 PDF 会跳过下载并读取页数。请依据各文献来源的使用条件访问，脚本的 MIT 许可证不覆盖论文内容。

[MIT](LICENSE)
