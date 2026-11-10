# MTH028 / MTH026 刷题站 · 技术说明

> 给接手这个仓库的 AI agent / 开发者看的：**代码怎么跑、数据长什么样、接口有哪些、改哪里安全、哪些坑已经踩过**。
> 先读第 0 节和第 11 节，能省掉 80% 的返工。最后更新：2026-11-09。

---

## 0. 一分钟上手

```bash
cd <repo>                                   # 仓库根目录就是线上站点的真身
MTH026_ROOT=$PWD MTH026_DB=/tmp/dev.db MTH026_PORT=8088 python3 server/server.py
# 浏览器打开 http://localhost:8088/          → MTH028（默认）
#          http://localhost:8088/mth026.html → MTH026
#          http://localhost:8088/admin       → 后台（需要 MTH026_ADMIN_PW）
```

只改题库、不动后端时，可以不启服务：直接改 `bank.js`，刷新页面即可（`bank.js` 是 `no-cache`）。

重建题库（数据驱动，一条链）：

```bash
cd mth028
python3 build/extract_v2.py          # 60 份 PDF（Q/B/H 三批）→ data/extract_v2.json（900 条原始记录）
python3 build/select_items.py        # 定答案、去重  → data/selection.json / duplicates.json（900 → 285）
python3 build/render_crops.py        # 出图          → out/img/{q,a}/<qid>.png + data/crops.json
python3 build/map_topics_v2.py       # 归考点        → data/topic_map.json
python3 build/merge_bank.py          # 落成 4 个文件  → data/quiz_{index,structured}.json
python3 build/assemble_bank.py       # 合 bank.js    → out/bank.js
python3 build/export_bank_index.py   # 后台用索引    → out/bank_index28.json
```

---

## 1. 仓库结构：哪份文件是真身

| 路径 | 角色 | 说明 |
|---|---|---|
| `index.html` | **MTH028 前端（真身）** | 单文件 SPA，含全部逻辑；线上就是这份 |
| `mth026.html` | MTH026 前端（真身） | 旧的单文件站，不与 028 共享 JS |
| `bank.js` | **MTH028 题库（真身）** | `window.MTH028_BANK = {...}`，285 题，来自 Q/B/H 三批导出 |
| `app.css` / `katex/` | 样式与公式 | 028 与 026 共用 |
| `img/q/<qid>.png` `img/a/<qid>.png` | 028 题图 / 答案图 | 每个 item 两张 |
| `q/` `pq/` | 026 的题图（351 + 323） | 命名与 028 无关 |
| `admin.html` | 后台控制台 | 同时管 026 和 028（`bank28` 系列接口） |
| `server/server.py` | **后端（真身，约 1600 行）** | 标准库 `http.server`，无第三方依赖 |
| `mth028/build/*.py` | 题库管线 | 不在运行路径上，只产出数据 |
| `mth028/data/*.json` | 管线的中间与最终数据 | 见第 6 节字典 |
| `mth028/out/` | 构建工作区（`bank.js`/`img`/`index.html` 的暂存） | 同步进仓库根后才上线 |
| `mth026/…`、`tools/` | MTH026 的生成脚本与素材 | 028 不依赖 |

> **别搞错**：仓库根的 `index.html`、`bank.js`、`img/`、`server/server.py` 才是线上运行的；`mth028/out/` 只是我构建时的暂存目录。改前端要在 `index.html` 上改，不要只改 `mth028/out/index.html`。

---

## 2. 运行时架构

```
浏览器 ──GET 静态──> server.py ──> ROOT 目录（/var/www/mth026）
   │                    │
   │                    └──> SQLite（/opt/mth026/data/app.db，WAL）
   └──JSON API──────────> /api/*（账号、进度、后台）
```

- 单进程 `ThreadingHTTPServer`，`systemd` 托管（`mth026.service`）。
- 静态与 API 同一个端口（8088），由 `App.do_GET/do_POST` 先看路径前缀：`/api/` 走 `_api`，其余走 `_static`。
- 没有模板引擎、没有构建步骤：改完文件刷新浏览器即生效（`bank.js`/`index.html`/`img/` 都是 `no-cache`）。

---

## 3. MTH028 前端（`index.html`）

### 3.1 结构

整个脚本是一个 IIFE：

- 内部所有函数、`ITEMS`/`TOPICS`/`BYTOPIC` 都在闭包里；
- 结尾 `G.MTH028_APP = API` 把**只读数据 + 纯函数**暴露给外部（`window.MTH028_APP`）；
- `GLOBAL_HANDLERS` 里的函数被挂到 `window`，因为 HTML 里用的是内联 `onclick="..."`。

```js
// 想在外面跑断言（Node 或浏览器控制台）：
const A = window.MTH028_APP;
A.ITEMS.length; A.BYTOPIC['2.1']; A.gradeChoice(A.ITEMS[0], 'B');
```

> 新增一个按钮/交互：若用内联 `onclick`，函数必须进 `GLOBAL_HANDLERS`，否则 `ReferenceError`（历史上踩过，整页按钮全废）。

### 3.2 视图与路由

纯 hash 路由，无 History API 兜底：

| hash | 视图函数 | 作用 |
|---|---|---|
| `#home` | `viewHome()` | 首页：考点掌握度、开始智能轮次 |
| `#ref` | `viewRef()` | 考点梳理（方法卡、公式、易错点） |
| `#bank` | `viewBank()` | 题库索引（按类型/章/搜索） |
| `#preview` | `viewPreview()` | 预览板：题目 + 答案直接展示，不计分 |
| `#fav` | `viewFav()` | 收藏 |
| `#mistakes` | `viewMistakes()` | 错题本（双层：latest + archive） |
| `#glossary` | `viewGlossary()` | 术语表 |
| `#quiz` | `viewQuiz()` | 答题卡（不写 hash，刷新回首页） |
| `#res` | `viewRes()` | 一轮结束的结果页 |

`route(v)` 是唯一入口；`HASHV`/`HASHROUTE` 两个表在文件中部。

### 3.3 item 数据模型（`normItem` 输出）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | **进度主键**。规则见 7.1，改动会让学生进度错位 |
| `qid` | str | 内部标签 `p3-13` / `b8-07`，只用于图片与数据 join |
| `label` | str | 显示用 `Q3-13` / `B8-07` |
| `quiz`,`qno` | int | 来源文件与题号（`quiz` 21–35 表示题库2） |
| `type` | `choice`\|`fill`\|`cloze` | 决定判分与输入框数量 |
| `blanks` | int | choice 为 0，fill 为 1，cloze 为 2/4 |
| `key` | str\|null | choice 的正确答案字母 |
| `answers` | str[]\|null | fill/cloze 的逐空答案 |
| `answerText` | str | 展示用参考答案（可能来自 AI） |
| `answerSource` | `pdf`\|`ai`\|`pdf-crop`\|`none` | 答案出处 |
| `aiGenerated` | bool | true → 页面显示「答案由 AI 生成」横幅 |
| `answerImg` | str\|null | 原卷反馈卡截图 |
| `img` | str | 题目截图（**唯一可靠题面**） |
| `topic` | str | 考点 id，如 `2.3` |
| `chapter` | int | 0/1，由 `topic` 推导 |
| `stem` | str | OCR 文本，**无空格、顺序会乱**，只用于搜索 |
| `options` | str[] | `["A","B","C","D"]`，只给按钮用 |
| `notes` | str | 备注（复杂答案/自评等） |

### 3.4 两层存储

```js
localStorage['mth028.en.v1']          // 游客桶
localStorage['mth028.en.v1@<name>']   // 登录后的账号桶
```

```js
store = {
  h:    { "<id>": {ok:bool, t:ms, a?:答案, resp?:string|string[], self?:1} },  // 最近一次作答
  fav:  { "<id>": 毫秒时间戳 },        // 收藏；负数=取消收藏的墓碑，绝对值大者胜
  miss: { "<id>": {n,first,last,rep,repAt} }, // 追加式错题档案，答对只置 rep=true，不删行
  streak: int, best: int
}
```

关键规则：

- **切换账号只换桶，不合并**：`switchOwner(name)` 重新 `loadBucket`；所以 A 的记录不会流进 B。
- 游客首次登录时，游客桶**折叠**进账号桶（`mergeInto`），这是唯一一次跨桶合并。
- `fav` 用带符号时间戳做「最后一次操作胜出」，离线/多设备也不会把取消收藏又翻回来。
- 服务端 401 时走同一条换桶路径，然后降级为游客。

同步：`save()` 防抖 → `schedulePush()` → `PUT api/progress28`（全量 `{h,fav,miss,streak,best}`），响应是整个合并后的 store，前端再 `mergeInto` 覆盖本地。**后端永远做合并，不做覆盖**（见 5.7）。

### 3.5 判分

```js
autoGradeable(it)   // choice: !!key；fill/cloze: answers 长度 == blanks
gradeChoice(it, L)  // 字母比较
gradeFill(it, v)    // ansEqual(v, answers[0])
gradeCloze(it, vs)  // 逐空 ansEqual，per[] 给出每空对错
ansEqual(a, b)      // 归一后比较：全角→半角、−/–/— → '-'、去空格与尾部标点
                    // 数值走容差（相对 1e-4）；"1/2" 与 0.5 互认（fracVal）
```

判不了分的题（`answers=null` 且没有 key）会走 `revealSelf()`：显示原卷答案图 + 「我答对了 / 我答错了」自评按钮，记 `self:1`。

### 3.6 智能轮次（`pickSmart`）

1. **阶段 1 覆盖**：`untouchedGroups()` = 该考点 `done===0`，按考点顺序优先出一个没做过的题；
2. **阶段 2 弱点**：全部考点都碰过后，按 `weakness(diag(sec))` 打分取最高（错得多、久未练的优先）；
3. `skips()` 记录「跳过这题 / 跳过这类」，本次会话内不再出；
4. 同一考点内 `pickFrom()` 先出没做过、再出错题、最后出最久未见的。

### 3.7 后台改答案的即时生效路径

```
后台 POST /api/admin/bank28/ans  →  bank_overrides28 表  →  GET /api/overrides28
   →  页面 boot 时 applyOverrides28(ov)：按 item.id 覆盖 it.key / it.answers
```

所以**后台改答案不需要重建 bank.js**，也不需要重启服务；代价是覆盖只存在数据库里，重建 `bank.js` 不会丢它（这是有意的）。

---

## 4. MTH026 一侧（改动前必读）

- `mth026.html` 是独立单页，进度走 `api/progress` + `progress` 表；028 走 `api/progress28` + `progress28` 表。
- 后端里有 `clean_progress`/`merge`（026）与 `clean_progress28`/`merge28`（028）两套。**不要把 028 的字段塞进 026 的清洗函数**：026 的白名单会把 `h[].a` 截成单个字母、丢掉未知字段，028 的填空答案（如 `-13`、`["4","2"]`）会被静默抹掉。
- 两侧共享 `users`、`sessions`、`audit` 与后台账号，但答案/收藏/错题互不可见。

---

## 5. 后端（`server/server.py`）

### 5.1 启动参数（环境变量）

| 变量 | 默认 | 作用 |
|---|---|---|
| `MTH026_ROOT` | 脚本上一级 | 静态根目录（线上 `/var/www/mth026`） |
| `MTH026_DB` | `<root>/data/app.db` | SQLite 路径（线上 `/opt/mth026/data/app.db`） |
| `MTH026_PORT` | `8088` | 监听端口 |
| `MTH026_ADMIN_PW` | 空 | 为空则后台关闭；线上从 `/opt/mth026/admin.env` 读 |
| `MTH026_BANK_INDEX` | `/opt/mth026/bank_index.json` | 026 的题号索引（后台用） |
| `MTH028_BANK_INDEX` | `/opt/mth026/bank_index28.json` | **028 的答案索引（后台用）**，由 `build/export_bank_index.py` 生成 |

### 5.2 用户接口

所有请求/响应都是 JSON；cookie 名 `mth026_sid`（HttpOnly，SameSite=Lax）。非 GET 请求会校验 `Origin`，跨站直接 403。

| 方法 | 路径 | 请求体 | 响应 |
|---|---|---|---|
| GET | `/api/health` | — | `{ok,port}` |
| GET | `/api/me` | — | `{user:{name,display,created}}` 或 `{user:null}` |
| POST | `/api/register` | `{u,p}` | `{ok:true}` + 设 cookie；重名 409，限速 429 |
| POST | `/api/login` | `{u,p}` | 同上；密码错 401 |
| POST | `/api/logout` | — | `{ok:true}`，清 cookie |
| GET | `/api/progress` | — | 026 的 store（未登录 401） |
| PUT | `/api/progress` | store | 合并后的 store |
| DELETE | `/api/progress` | — | 清空 026 进度 |
| GET/PUT/DELETE | `/api/progress28` | 同上 | 028 的 store，PUT 用 `clean_progress28`+`merge28` |
| GET | `/api/overrides` | — | 026 的后台覆盖 `{overrides:{id:{key,answers}}}` |
| GET | `/api/overrides28` | — | 028 的后台覆盖 `{updated,count,overrides:{id:{key}|{answers}}}` |

store 形状与前端一致：`{h,fav,miss,streak,best}`，GET 额外带 `updated`（秒）。

### 5.3 管理接口（cookie `mth026_admin`）

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/admin/login` / `logout` | `{p}`；密码在 `MTH026_ADMIN_PW`，不是用户表里的账号 |
| GET | `/api/admin/state` | `{enabled,signed_in}`，不需要登录 |
| GET | `/api/admin/stats` | 用户数、答题量等 |
| GET | `/api/admin/users` | 用户列表 |
| GET | `/api/admin/audit` | 审计流水（最近 2000 条） |
| GET | `/api/admin/bank` | 026 题库分页 |
| POST | `/api/admin/bank/ans` | `{id,a}` 改 026 答案 |
| POST | `/api/admin/bank/note` | `{id,note}` 加备注 |
| GET | `/api/admin/bank28?q=&type=&filter=&limit=&offset=` | 028 题库分页 → `{total, rows:[{id,qid,label,type,topic,base,current,changed,note,img,answerImg,blanks}]}` |
| POST | `/api/admin/bank28/ans` | `{id,a}`；choice 只收 A–D，填空按 `blanks` 逗号分隔，空串=删除覆盖 |
| POST | `/api/admin/bank28/note` | `{id,note}` |
| GET | `/api/admin/export.csv` | 导出用户/进度 |
| POST | `/api/admin/user/{pw,reset,kick,ban,unban,del}` | 改密 / 清进度 / 踢下线 / 封禁 / 解封 / 删号 |

`bank28` 系列以 **item.id** 为键查 `/opt/mth026/bank_index28.json`；文件缺失或过期会导致「no such item」——见第 9 节。

### 5.4 数据库

```sql
users(id PK, name UNIQUE, display, salt BLOB, hash BLOB, created, banned)
sessions(token PK, uid, created, seen, ip)          -- token 存的是 sha256，不是明文
progress(uid PK, blob TEXT, updated)                 -- 026 进度（JSON 文本）
progress28(uid PK, blob TEXT, updated)               -- 028 进度
admin_sessions(token PK, created, seen, ip)
audit(id PK, ts, ip, action, target, detail)
bank_overrides(item_id PK, ans, note, updated)       -- 026 后台改答案
bank_overrides28(item_id PK, ans, note, updated)     -- 028 后台改答案
```

- WAL 模式；连接用 `sqlite3.Row`。
- 密码 `PBKDF2-HMAC-SHA256`，20 万轮，随机 16B salt；会话 token 随机、库里只存 `sha256(token)`。
- 会话有效期：用户 30 天（`SESSION_SECS`，滑动续期 `seen`），后台 12 小时（`ADMIN_SESSION_SECS`）。
- 注册/登录有按 IP 的失败限速（`FAIL_LIMIT`/`FAIL_WINDOW`）。

### 5.5 静态服务

| 路径 | Cache-Control | 说明 |
|---|---|---|
| `/`、`/index.html`、`/mth026.html`、`/bank.js`、`/app.css` | `no-cache` | 改完刷新即生效 |
| `/img/**`（028 题图/答案图） | `no-cache` | 图会随重建覆写，禁止强缓存 |
| `/q/**`、`/pq/**`、`/katex/**` | `public, max-age=2592000, immutable` | 026 题图与字体，内容不变 |
| 其他静态 | `public, max-age=86400` | 默认 |

- 所有响应带 `ETag`（mtime-size），命中 `If-None-Match` 返回 304。
- 文本类 >1KB 且客户端支持时 gzip（压缩率 >8% 才用）。
- 路径做了 realpath 越界检查，`/admin` 映射到 `admin.html`。

### 5.6 进度的清洗与合并（028）

```python
clean_progress28(payload)   # 白名单：h[id]={a,ok,t,self?,resp?}；fav→带符号 int；miss→{n,first,last,rep,repAt}
merge28(old, new)           # h 按 t 取新（整条替换，避免旧 resp 残留）
                            # fav 绝对值大者胜；miss 只增不减；streak/best 取 max
```

`a` 允许 8 字符（字母或短答案），`resp` 允许 str(≤200) 或 list(≤8)。

---

## 6. 数据文件字典（`mth028/data/`）

| 文件 | 谁写 | 内容 |
|---|---|---|
| `extract_v2.json` | `extract_v2.py` | 900 条原始记录：每题一页卡片的精确矩形、选项、印刷答案、学生填值、是否作答 |
| `selection.json` | `select_items.py` | **最终 285 条**：定好的 key/answers/blanks、去重后的代表、`aiGenerated` |
| `duplicates.json` | `select_items.py` | 被合并掉的题号 → 保留题号（追溯用；修正项靠它跟随） |
| `answer_fixes.json` | **人工** | 唯一的人工修正入口：`{"fill":{qid:{answers,blanks}}, "choice":{qid:"B"}}` |
| `crops.json` | `render_crops.py` | qid → `img/q/x.png`、`img/a/x.png` |
| `topic_map.json` | `map_topics_v2.py` | qid → 考点；`topic_map_overrides.json` 里的人工标注优先 |
| `quiz_index.json` / `quiz_structured.json` | `merge_bank.py` | 装配器的输入（旧格式，保持兼容） |
| `topics.json` | 人工/生成 | 17 个考点 + 2 章；`has_slides:false` 的会显示「课件暂缺」 |
| `glossary.json` | 人工 | 33 组 / 212 术语 |
| `bank_index.json` | 旧产物 | 仅 026 后台用，028 不用 |

`out/bank.js` 与 `out/bank_index28.json` 是最终产物：`bank.js` 上站点，`bank_index28.json` 上服务器 `/opt/mth026/`。

---

## 7. 命名与编号约定

### 7.1 item.id（= 进度主键）

```
MTH028-Quizzes/N.pdf  → quiz = N     (1..15)  → id = N*1000 + qno        (1001..15015)
题库2/2-N.pdf          → quiz = 20+N  (21..35) → id = quiz*1000 + qno     (21001..35015)
HJT/3-N.pdf            → quiz = 60+N  (61..75) → id = quiz*1000 + qno     (61001..75015)
```

- `id` 必须**稳定**：换代表、重新去重都不应改变已上线题目的 id，否则学生进度对不上。
  去重打分里 `rank()` 给「已上线的 qid（`p1-01`…`p10-15`）」加一分，就是为了这个。
- 新题直接取空号段（如 36000+），不要复用。

### 7.2 qid / label

- `qid`：`p<quiz>-<qno>`（MTH028-Quizzes）/ `b<n>-<qno>`（题库2 第 n 份）/ `h<n>-<qno>`（HJT 第 n 份）。
  用于图片文件名与数据 join。
- `label`：`Q…` / `B…` / `H…`。只用于显示；题库页顶部有一行图例解释三种前缀。

### 7.3 type 与 blanks

- 单空填空 → `fill`，`blanks:1`；
- 多空（`m=__, n=__` 或 `a=__,b=__,c=__,d=__`）→ **必须是 `cloze`**，否则前端只渲染一个输入框、只判第一空（`answerAreaHtml` 里 `n=(it.type==='cloze')? it.blanks : 1`）；
- 选择题 → `choice`，`blanks:0`，答案在 `key`。

---

## 8. 常见改动怎么做

| 想做什么 | 改哪里 | 是否需要重建 |
|---|---|---|
| 改某题答案（临时/线上） | 后台 `/admin` → MTH028 → 题库管理 | 否，存取 `bank_overrides28` |
| 改某题答案（写进数据） | `data/answer_fixes.json` 的 `fill.<qid>.answers` / `choice.<qid>` | 是，从 `select_items.py` 起重跑 |
| 加一道新题 | 把题图放进 `img/q/`、答案图 `img/a/`，在 `selection.json` 加一条（或在 `extract_v2.json` 加原始记录后跑管线），再跑 `merge_bank.py`+`assemble_bank.py` | 是 |
| 加一个考点 | `data/topics.json` 加一行（`id/ch/en/zh/focus…`），题目的 `topic` 填这个 id | 是，`assemble_bank.py` |
| 改考点归属 | `data/topic_map_overrides.json`（`{"overrides":[{"qid":"p3-13","topic":"1.4"}]}`） | 是 |
| 加术语 | `data/glossary.json` 对应 group 的 `items` | 是 |
| 调整去重/选代表 | `build/select_items.py` 的 `rank()` 与 0.94/0.90 两个阈值 | 是（会改变 `selection.json`） |
| 换页面样式 | `app.css` / `index.html` 的 `<style>` | 否 |
| 加一个后台可改字段 | 前端 `applyOverrides28` + 后端 `_admin_bank28_ans` 的 `ans_json`，两边一起改 | 否 |

新增前端按钮时，记得把处理函数加进 `GLOBAL_HANDLERS`。

---

## 9. 部署

线上：`http://183.66.27.19:58621/`（弹性公网）→ 容器 `183.66.27.19:21491` SSH → 本机 8088。

```
/var/www/mth026/            静态根（index.html, bank.js, img/, katex/, mth026.html, q/, pq/）
/opt/mth026/server.py       后端
/opt/mth026/data/app.db     SQLite
/opt/mth026/bank_index28.json   028 后台答案索引（由 build/export_bank_index.py 生成）
/opt/mth026/admin.env       后台密码（MTH026_ADMIN_PW=...）
systemctl {status,restart} mth026
```

典型发布（只推静态，不碰数据库）：

```bash
export SSHPASS='***' SSH_ASKPASS=/tmp/askpass.sh SSH_ASKPASS_REQUIRE=force DISPLAY=:0
rsync -az -e "ssh -p 21491" bank.js index.html root@183.66.27.19:/var/www/mth026/
rsync -az --delete -e "ssh -p 21491" img/q/ root@183.66.27.19:/var/www/mth026/img/q/
rsync -az --delete -e "ssh -p 21491" img/a/ root@183.66.27.19:/var/www/mth026/img/a/
# 题库结构变了才需要下面两步：
rsync -az -e "ssh -p 21491" mth028/out/bank_index28.json root@183.66.27.19:/opt/mth026/bank_index28.json
ssh -p 21491 root@183.66.27.19 "systemctl restart mth026"
```

**三条铁律**

1. `--delete` 只对 `img/q/`、`img/a/` 用（纯生成目录）。往仓库根部同步**绝不要** `--delete`，会删掉 `README/server/unit`。
2. 改了题目集合 → **必须同步 `bank_index28.json` 并重启**，否则后台列表还是旧题、编辑新题返回 404 `no such item`（`bank28_map()` 有进程内缓存，重启才会重载）。
3. 部署前备份：`cp -a index.html index.html.bak.$(date +%Y%m%d)` 同理 `bank.js`、`bank_index28.json`。

---

## 10. 验证手段（改完必跑）

### 10.1 数据结构不变量（Node，秒级）

```bash
node -e "
global.window={};require('./bank.js');const b=window.MTH028_BANK,it=b.items,bad=[],ids=new Set();
it.forEach(x=>{ if(ids.has(x.id))bad.push('dup '+x.id); ids.add(x.id);
  if(!x.img)bad.push('noimg '+x.qid);
  if(x.type==='choice'&&!x.key)bad.push('nokey '+x.qid);
  if(x.type!=='choice'&&(!x.answers||x.answers.length!==x.blanks))bad.push('ans '+x.qid);
  if(!x.topic)bad.push('notopic '+x.qid); });
console.log(it.length,'bad',bad.length,bad.slice(0,5));"
```

期望输出：`285 bad 0`。

### 10.2 前端行为断言（无头 Edge 注入）

浏览器里没有测试框架，用「复制一份页面 + 追加脚本 + `--dump-dom` 取结果」：

```bash
python3 - <<'PY'
src=open('index.html',encoding='utf-8').read()
add='''<div id="__t" style="white-space:pre;font:12px monospace"></div>
<script>window.addEventListener('load',function(){setTimeout(function(){
 var R=[],A=window.MTH028_APP;
 function ck(n,c,x){R.push((c?'PASS ':'FAIL ')+n+(x!==undefined?' ['+x+']':''));}
 var z=A.ITEMS.filter(function(i){return i.type==='cloze'})[0];
 ck('items',A.ITEMS.length===228,A.ITEMS.length);
 ck('all gradable',A.ITEMS.every(A.autoGradeable));
 ck('cloze right',A.gradeCloze(z,z.answers).ok===true,z.qid);
 startSingle(z.id);
 var bx=document.querySelectorAll('[id^=ansIn]');
 ck('UI inputs',bx.length===z.blanks,bx.length);
 for(var k=0;k<bx.length;k++)bx[k].value=z.answers[k];
 submitAnswer(); ck('UI correct',/Correct/.test(document.body.innerText));
 document.getElementById('__t').textContent='RESULT\\n'+R.join('\\n');},600);});</script></body>'''
open('__test.html','w',encoding='utf-8').write(src.replace('</body>',add))
PY
python3 -m http.server 8899 &            # 或直接用线上地址
"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" --headless --disable-gpu \
  --user-data-dir=/tmp/ep --virtual-time-budget=10000 --dump-dom \
  "http://127.0.0.1:8899/__test.html" | grep -A20 RESULT
rm -f __test.html
```

### 10.3 线上核对

```bash
curl -s http://183.66.27.19:58621/api/health                     # {"ok":true,"port":8088}
curl -s http://183.66.27.19:58621/bank.js | head -c 120           # total 应为当前题量
curl -sI http://183.66.27.19:58621/img/q/p3-13.png | grep -i cache # 应为 no-cache
```

后台接口（需要密码，建议在服务器本机跑，避免密码外泄）：

```bash
ssh ... "python3 -" < admin_check.py   # login → GET /api/admin/bank28 → 打印 total
```

### 10.4 出图检查（截图类改动必做）

随机抽 6–8 张 `img/q/*.png` 用视觉模型/人眼确认：**题干完整、选项齐全、无 ✓/✗、无选中圆点、输入框为空**；再抽 2 张 `img/a/*.png` 确认答案是完整渲染（不是半截矩阵）。

---

## 11. 已知陷阱（按踩坑成本排序）

1. **题图裁切不能靠文字锚点。** Moodle 复习页每张卡片都是绘制矩形，颜色固定：header `#CAD0D7`、题干卡 `#B3D9E0`、反馈卡 `#FBE6CA`。用 `page.get_drawings()` 的 `color` 取卡，再用卡片矩形裁图，题目图就不可能包含反馈卡（旧实现用 `The correct answer is` 的 y 减 15，Quiz 3 没有 verdict 行时会把解题过程切进题目图）。
2. **`search_for("The correct answer is:")` 会命中同页上一题**。必须 `feed_rect.contains(hit)` 过滤，否则答案被判成 None。
3. **矩阵答案的首行在基线之上**，只取「标记行之后」会丢一行；要同时取 phrase 上方 ±46pt 且 x 在右侧的词。
4. **输入框有两种画法**：`Answer: [____]` 是蓝灰边 `#8F9AA0`；句内小框是**纯黑边 + 白底**（10–70pt 宽）。只按一种颜色匹配会漏掉学生填值 → 截图泄漏答案。
5. **多空题必须用 `cloze`**，`fill` 只渲染一个输入框、且 `gradeFill` 只比较第一空（会「答对一个空就判对」）。
6. **原卷答案优先于手算**：Q5-05 我按 b=[3,−6,−k] 算出 k=3，原卷印的是 −3（第三分量是 k）。手算只能填空缺，不能覆盖原卷；这条规则已写进 `select_items.py`。
7. **去重代表会漂移**：`rank()` 排序变了就可能换代表题 → `qid`/`id` 改变 → 学生进度错位。给已上线 qid 加权可稳定；`answer_fixes.json` 还会沿 `duplicates.json` 的合并链查找，否则修正会静默失效。
8. **`bank_index28.json` 是独立产物**：只更新 `bank.js` 不更新它，后台会显示旧题、拒绝编辑新题。
9. **`img/` 曾经是 1 天强缓存**：重建后同名的图会让老用户看到旧截图（可能是漏答案的那版）。现已改为 `no-cache`。以后若把图片改成内容哈希文件名，可以再改回长缓存。
10. **前端是 IIFE**：新增内联 `onclick` 必须把函数注册进 `GLOBAL_HANDLERS`，否则整页按钮 `ReferenceError`。
11. **zsh 不会对 `$OPTS` 分词**：ssh/rsync 的选项要写全，别拼变量。
12. **无头 Edge 最小视口约 492px**：`--window-size=360` 只是裁切，不能用来验手机断点。
13. **PDF 文字层的空格会丢**（`augmentedmatrix`）：所有文本匹配都要同时试「有空格」和「去空格」两种写法。
14. **`answer_fixes.json` 的修正只对同一 `qid` 生效，绝不跨模板复用**。同一模板的不同 attempt 数字不同、答案也不同：曾把「求 A⁻¹ 第一列」的答案沿去重组合套到另一道矩阵不同的题上，直接教错。若某题的修正值来自原卷说明（而不是自己算的），加 `"from": "paper"`，这样不会被打上 AI 标记。
15. **同一题在不同批次里可能是不同 qid**（去重代表会变）：修正项若指向一个已被合并掉的 qid，它就静默失效，该题会重新出现在「fill needing an answer」里——这是**正确**行为，重算那一道即可，不要改成按组合查找。

---

## 12. 术语

| 词 | 含义 |
|---|---|
| attempt review | Moodle 交卷后的复盘页，本项目的题源 |
| 反馈卡 | 复盘页黄框，含解题过程与 `The correct answer is:` |
| 代表题 | 同一模板（题干+选项，数字掩码后相同）里保留的那一道 |
| 题库2 | 第二批 15 份导出（`题库2/2-1…2-15.pdf`），题号前缀 B |
| 双层错题本 | `store.h`（最近一次）+ `store.miss`（只增不删的档案） |
| 自评题 | 没有可靠答案的题，展示原卷答案后由学生自己判对错（`self:1`） |
