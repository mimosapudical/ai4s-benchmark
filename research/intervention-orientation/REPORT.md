# 因果结构任务：提案准备交付报告

当前结论：已完成一个科学任务的规格、数据、oracle/verifier 原型和作者侧校准；**未开 PR，也未提交或声称获批提案**。本次没有找到该任务的人工批准记录。剩余门槛见末尾清单，不能称为 upstream review ready。

## 1. 仓库与版本

- Upstream：`AI4S-Bench/ai4s-benchmark`。
- 精确 upstream main：`909274d50e91360991b5cc8c60edc3696de37f40`，收尾再次 fetch 后未变化。
- Fork：`mimosapudical/ai4s-benchmark`。
- 分支：`proposal/interventional-essential-graph-20261017`。
- 已校准的实现提交：`5539af71fdd37fefa087a33e88bd08cd5203029c`。
- 后续提交只加入最终证据与本报告。最终交付 SHA 在交付消息中给出；五个任务文件和校准器的精确哈希另见 `computation_manifest_r5_20261017.json`。

审查读取了 README、CONTRIBUTING、bench README/manifest/runner、PR 模板、五个 workflow、任务示例、validator 及其 tests、贡献文档和科学 rubric。GitHub connector 拉取全部 26 条 PR、issues 集合中的 11 条独立 issue，结合近期 git log；Discussions 的两个列表页、关闭/作者过滤页也已检查。主分支唯一任务为贡献示例；未合并任务为其他领域。两个名称含 Causal 的现有提案做文献证据整理，并非本任务的干预图定向。此检索未发现重复实现；这不是对全世界 benchmark 的新颖性证明。

## 2. 选择与科学价值

已比较 A 完整干预 DAG 恢复、B 观测等价类加干预定向、C 异质环境不变结构；只实现 B，比较表在 `PROPOSAL.md`。

像用几张不同角度的照片重建物体：有些棱角照片足以确定，有些背面仍看不到。要求把看不到的部分也画死，会奖励猜测。本任务要求输出干预 essential graph，把“有限样本选错等价类”和“即使无限样本也不能定向”区分开。

8 个系统，各 9 节点、12 条骨架边；观测 MEC 各有 144 个 DAG。每个系统提供 1500 观测样本、两种干预各 500 样本的高斯充分统计量。固定数据共 52 条可定向边、44 条仍模糊边。生成器先确定观测协方差，再独立均匀抽取真实 DAG 并重参数化，避免观测方差顺序替代真正的干预识别。

这是统计方法研究的受控合成任务；不伪装成真实实验数据，也不声称新因果发现算法。它尚未证明 frontier 难度足以达到研究级 benchmark 的收录标准。

## 3. 精确文件与函数

任务根目录：`tasks/applied-mathematics/causal-discovery/finite-sample-intervention-orientation/`。恰好新增五个文件，没有修改原有实现。

| 文件 | 内容/函数 | 当前行范围 |
|---|---|---|
| `task.toml` | 正确 domain/field、包名、作者与资源 | 1–32 |
| `instruction.md` | 完整假设、输入、输出、公开评分 | 1–74 |
| `environment/Dockerfile` | Python/NumPy；仅嵌入合法 evidence | 1–9 |
| `solution/solve.sh` | `enumerate_dags`、`local_score`、`infer` | 13–32、35–46、49–70 |
| `tests/test.sh` | `equivalence_signature`、`acyclic`、`essential_states`、`grade`、`read_answer` | 18–27、30–37、40–58、61–89、92–106 |

作者侧 `research/intervention-orientation/` 另含生成器 `generate.py`、校准器 `calibrate.py`、配对扫描 `sensitivity.py`、7 项科学单测 `test_science.py`，以及提案、文献核查、每轮结果和 PR 草稿。它们不是第二个任务或第二套通用运行框架，不进入 agent 镜像。

编辑前已用 `nl -ba` 阅读最近参照：贡献示例 TOML 1–13、solve 1–5、test 1–11；validator `task_toml_errors` 54–77、`main` 80–120（其中审批链接检查 93–104）。现有 validator、CI、bench manifest 和示例均保持原样。

## 4. 方法与定理

- Hauser & Bühlmann，JMLR 2012，Theorem 10：保守干预族下，各 mutilated DAG 的骨架和 v-structures 一致是干预等价判据。这里包含观测环境，噪声为正方差高斯，符合条件。verifier 直接枚举此判据；oracle 使用其单点干预推论，不共享实现代码。
- Hauser & Bühlmann，arXiv:1303.3216v1：联合高斯机制似然的相关方法来源。本实现的目标函数在 `METHODOLOGY.md` 独立推导；不把渐近一致性当有限样本保证。
- Yan 等，ICML 2024：有限样本定向是统计检验问题。这里没有实现该论文的 anytime-valid 检验，评分的 0.95 也不是置信水平。
- Herman 等，CLeaR 2025：提醒合成数据中的方差/R² 排序捷径；本任务使用协方差匹配，而非声称实现其 UUMC 方法。
- Lungu 等，2026 预印本：研究观测/干预样本比例，但其二变量、固定干预值、贝叶斯定理不直接适用本任务，仅作为最新相邻工作。

数学原则：高斯充分统计量及 Wishart 波动、共享非目标机制的 profile likelihood、essential graph 状态 Hamming loss；若两种参数化在所有可用环境分布相同，Le Cam 二点下界说明不能统一可靠区分。这解释了为何不可强制给所有边定向，不能证明本任务跨类的有限样本恢复率。

所有来源链接、查到的版本、具体假设和适用边界见 `METHODOLOGY.md`，未以论文题目代替定理核查。

## 5. 校准结果

| 检查 | 精确结果 |
|---|---|
| 最终固定数据 Oracle | 5/5 reward=1；每次 96/96，四项 accuracy 全部 1 |
| 无输出/空文件/坏 JSON/布尔值/重复键/额外键/符号链接 | 全部 reward=0，输出格式错误 |
| 全部不定向 | 44/96=45.8333%，reward=0 |
| 全部正向 | 25/96=26.0417%，reward=0 |
| 每系统破坏 4 条的真值样式答案 | 64/96=66.6667%，reward=0 |
| 观测数据方法 | 44/96=45.8333%，reward=0 |
| 分环境拟合、忽略机制共享 | 55/96=57.2917%，reward=0 |
| 预先伪造 reward.json/reward.txt | 每轮被清除，不改变失败判定 |

每轮记录保留，不覆盖：r1 是作者侧 heredoc 解析错误；r2 固定数据通过；r3 未配对探索保留其失败与混杂限制；r4 修正为固定结构参数、样本嵌套的配对扫描；r5 在已提交实现上重跑最终控制。

配对新数据（每档 5 个固定 seed，每组 8 系统）：干预样本 25/75/200/500 时分别 2/5、4/5、5/5、5/5 组通过。200 和 500 档平均正确率均 99.5833%，并非每组 exact recovery。未配对 r3 在 500 档仍有 1/5 组因局部错误失败；这条证据没有删除。有限采样检查不能变成普适成功保证。

## 6. 命令与结果

以下均从仓库根运行；原始命令、stdout/stderr、退出码见 `validation_r5_20261017.json` 和各 audit summary。

| 命令 | 结果 |
|---|---|
| `python research/intervention-orientation/test_science.py -v` | 7 tests，OK，exit 0 |
| `python -m pytest -q` | 11 passed，exit 0 |
| `env -u ALL_PROXY -u all_proxy -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy python -m unittest discover -s ci_checks -p 'test_*.py'` | 21 tests，OK，exit 0；离线 localhost 测试不需要代理 |
| `uv run --locked --script ci_checks/rubric_review.py --help` | exit 0，无模型调用 |
| `sh -n tasks/applied-mathematics/causal-discovery/finite-sample-intervention-orientation/solution/solve.sh` | exit 0 |
| 同一路径的 `sh -n .../tests/test.sh` | exit 0 |
| `git diff upstream/main --check` | exit 0 |
| `python research/intervention-orientation/calibrate.py --output research/intervention-orientation/audit_r5_20261017`，BLAS/OMP=1 | exit 0，17 条记录，wrapper 17.13 秒 |
| `env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/intervention-orientation/sensitivity.py --output research/intervention-orientation/audit_r4_20261017` | exit 0，20 个 bank，23.70 秒 |
| `python research/intervention-orientation/generate.py --output /tmp/ai4s_assets_r2_20261017` | 默认 evidence/truth/generation 哈希与第一轮完全一致 |
| `task_toml_errors(..., new_task=True)` + 五文件/LF/镜像源检查 | 无错误，全部通过 |
| Harbor 0.20.0 `Task(path)` 加载 | 通过；四 CPU、零 GPU、正确作者、no-network |
| 实际 `harbor run -p tasks/applied-mathematics/causal-discovery/finite-sample-intervention-orientation -a oracle -e docker` | exit 1，Docker 未安装；没有开始求解或评分 |
| `python scripts/validate_task.py --base upstream/main --head HEAD`，无提案链接 | exit 1，按预期阻止无批准提案的新任务贡献 |
| computation-audit `validate_manifest.py ... --root .` | version-2 evidence record 有效，源文件前后哈希一致；不等于定理证明 |

初次完整 SDK 测试失败原因是继承的 SOCKS 代理需要缺失的 socksio；已在独立 upstream worktree 复现同一失败，日志 `upstream_ci_r1_20261017.log`。只在离线测试进程去掉代理后 21 项全过，没有改 upstream 测试或依赖锁，也没有隐瞒原始失败。

仓库 `bench/run_matrix.py preflight` 还指向既有外部 AMR pin，当前没有该子模块内容，且 Docker 缺失；没有擅自把 manifest 切到新任务来获得表面通过。新任务自己的 Harbor 运行已单独确认是 Docker setup failure。

## 7. 初始清单复核及限制

- [x] 科学问题与 A/B/C 比较完成，只实现 B。
- [x] 精确 upstream SHA、参考行号、文件/函数清单已记录。
- [x] 未发现仓库内同功能任务；无原有代码改动、无无关重构。
- [x] 一个任务、五个文件，作者和目录一致；4 CPU/0 GPU。
- [x] 合法信息 oracle；verifier 不调用 oracle/generator/agent 代码。
- [x] 固定 oracle 5 次通过；负对照、格式控制、合理不完整方法均有结果。
- [x] 全部可执行本地 focused/smoke/仓库检查通过；完整 diff 和邻近逻辑已复读。
- [x] 结果逐轮独立文件；保留设置失败、科学失败和不利证据。
- [ ] 人工批准提案：尚无。不能用其他项目或其他任务的批准代替。
- [ ] Docker 构建、实际 Harbor Oracle/no-op、资源/隔离验证：环境缺 Docker。
- [ ] Frontier-agent 尝试与真实科学难度：未运行，不能声称模型稳定失败。
- [ ] 独立人工科学审查及最终收录/署名：尚无。

公开仓库会暴露 solution/tests 源文件；要求 harness 在 agent 阶段不挂载这些路径，并隔离外网。镜像构建内容没有答案和生成 seed，但这不防公开源码记忆、全仓库挂载或被篡改的可信运行器。Python `-I` 和奖励文件控制不是容器安全证明。此处不宣称已解决持久后台进程篡改等攻击。

已识别的不可运行/外部审批项目不能靠重复本地测试变绿。因此本次按指令交付 proposal-ready 包，**不开放任务 PR**，也不把所有门槛标为完成。

## 8. PR 标题与正文

标题：`Add finite-sample interventional essential-graph recovery task`。

完整待提交正文见 `PR_DRAFT.md`。其中明确列出待批准状态，没有插入伪造的 Discussion，也没有在未完成的工作中添加 upstream issue 引用。审批与运行门槛完成后才更新并提交。

## 9. 是否足以谈作者署名

这已经超出维护性工程补丁：贡献者拥有一个有可识别性边界、独立评分、生成控制和校准证据的科学资产。**但目前不能称为已验证的 authorship-grade 成果**：候选只有 144 个 DAG，强模型可能轻易写出穷举求解；还没有 frontier 实测或人工科学认可。当前适合用具体资产发起提案评审，最终是否足以支持作者讨论，取决于这些未完成证据和项目署名政策，而不是一次 merge。
