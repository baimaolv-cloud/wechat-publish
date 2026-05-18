---
name: wechat-publish
description: 公众号草稿发布完整工作流。当需要发布公众号文章时使用此技能，涵盖：文章排版生成预览链接、上传/生成封面图、调用API创建草稿、确认草稿是否正确推送到草稿箱。触发场景：「发公众号」「发布文章」「公众号草稿」「生成封面图」。
---

# wechat-publish

公众号草稿发布的标准工作流。

## 凭据（内置，无需传递）

```
APPID = wxeeb2399e2d6a85aa
SECRET = 9ce9cd99245ce3d36967dc622e69332a
```

## 标准发布五步

### Step 0：生成预览
文章 Markdown → 双版本预览链接：
```
node wechat-dual-copy.js <article.md> --emit-ai-draft
```
输出两个链接：AI结构化版、预设主题版。

### Step 1：封面图

**已有封面**：`C:\Users\mac\.qclaw\workspace\tools\cover_*.png`

**生成新封面**：调用 `scripts/make_cover.py` 或直接写 PIL 脚本生成。

**封面图路径**：统一存 `workspace/tools/` 目录。

### Step 2：写参数 JSON

在 `workspace/tools/` 创建参数文件，例如 `wp_xxx.json`：
```json
{
  "title": "文章标题",
  "author": "白毛驴",
  "digest": "文章摘要",
  "cover": "C:\\Users\\mac\\.qclaw\\workspace\\tools\\cover_xxx.png",
  "content": "C:\\Users\\mac\\.qclaw\\workspace\\article.ai.draft.html"
}
```

### Step 3：发布草稿
```
python workspace/tools/wechat_publish.py --params workspace/tools/wp_xxx.json
```

**如果脚本路径变化**，用绝对路径：
```
python C:\Users\mac\.qclaw\workspace\tools\wechat_publish.py --params C:\Users\mac\.qclaw\workspace\tools\wp_xxx.json
```

### Step 4：确认草稿
调用 `check_drafts2_fixed.py` 确认草稿在列表第一位。

## 关键规则

- **thumb_media_id 不可为空**，必须用 `add_material?type=image` 获取
- **凭据错误 40125**：确认 SECRET=`9ce9cd99245ce3d36967dc622e69332a`
- **中文参数乱码**：用 JSON `--params` 文件传参，不要用命令行参数
- **订阅号不能 API 群发**（errcode=48001），草稿创建成功后在后台发布
- **封面图上传**：`material/add_material?type=image` → 获得 `media_id` → 作为 `thumb_media_id`

## 脚本清单

| 脚本 | 用途 |
|------|------|
| `scripts/wechat_publish.py` | 标准化发布脚本 |
| `scripts/make_cover.py` | 封面图生成脚本（边际成本曲线示例） |
| `workspace/tools/check_drafts2_fixed.py` | 确认草稿列表 |
| `wechat-dual-copy.js` | 排版预览链接生成 |