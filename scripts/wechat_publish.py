# -*- coding: utf-8 -*-
"""
公众号标准发布脚本 wechat_publish.py
用法:
  python wechat_publish.py --title "标题" --author "作者" --digest "摘要" --cover path/to/cover.png --content path/to/article.html
  python wechat_publish.py --params path/to/params.json  # 通过JSON文件传参（避免命令行编码问题）

标准五步:
  Step 0: 预览 (markdown -> dual-copy HTML)
  Step 1: 封面 (已有 cover_*.png 或生成)
  Step 2: 调用本脚本发布
  Step 3: 确认草稿
  Step 4: 后台发布
"""
import sys, os, json, urllib.request, re, argparse

sys.stdout.reconfigure(encoding='utf-8')

# ========== 凭据（2026-05-18 验证正确）==========
APPID = "wxeeb2399e2d6a85aa"
SECRET = "9ce9cd99245ce3d36967dc622e69332a"

def get_token():
    tu = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + APPID + "&secret=" + SECRET
    resp = urllib.request.urlopen(tu, timeout=15)
    result = json.loads(resp.read())
    if "access_token" not in result:
        raise Exception("Token failed: {}".format(result))
    return result["access_token"]

def upload_material(token, path, mtype="image"):
    """上传永久素材，返回 media_id"""
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={}&type={}".format(token, mtype)
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    with open(path, "rb") as f:
        img_data = f.read()
    fname = os.path.basename(path)
    body = ("--{}\r\n"
            "Content-Disposition: form-data; name=\"media\"; filename=\"{}\"\r\n"
            "Content-Type: image/png\r\n\r\n"
    ).format(boundary, fname).encode() + img_data + "\r\n--{}--\r\n".format(boundary).encode()
    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", "multipart/form-data; boundary={}".format(boundary))
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read())
    if "media_id" not in result:
        raise Exception("Upload failed: {}".format(result))
    return result["media_id"]

def create_draft(token, title, author, digest, content, thumb_id):
    """创建草稿，返回 media_id"""
    url = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token={}".format(token)
    payload = json.dumps({"articles": [{
        "title": title,
        "author": author,
        "digest": digest,
        "content": content,
        "thumb_media_id": thumb_id,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]}, ensure_ascii=False)
    req = urllib.request.Request(url, data=payload.encode("utf-8"))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read())
    if "media_id" in result:
        return result["media_id"]
    raise Exception("Draft failed: {}".format(result))

def read_content(content_path):
    """读取正文，支持 .html 和 .md"""
    with open(content_path, "r", encoding="utf-8") as f:
        raw = f.read()
    if content_path.endswith(".md"):
        import markdown
        md = markdown.Markdown(extensions=['tables', 'fenced_code'])
        html = md.convert(raw)
        return "<section>{}</section>".format(html)
    body_match = re.search(r'<body[^>]*>(.*?)</body>', raw, re.DOTALL | re.IGNORECASE)
    if body_match:
        content = body_match.group(1).strip()
    else:
        content = raw
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    return content

def main():
    p = argparse.ArgumentParser(description="公众号标准发布脚本")
    p.add_argument("--title", help="文章标题")
    p.add_argument("--author", default="白毛驴", help="作者")
    p.add_argument("--digest", default="", help="摘要")
    p.add_argument("--cover", help="封面图路径")
    p.add_argument("--content", help="HTML 正文路径")
    p.add_argument("--md", help="Markdown 正文路径")
    p.add_argument("--params", help="JSON参数文件路径（可替代所有参数）")
    args = p.parse_args()

    # 从 JSON 文件加载参数
    if args.params:
        with open(args.params, "r", encoding="utf-8") as f:
            params = json.load(f)
        title = params.get("title") or args.title
        author = params.get("author") or args.author
        digest = params.get("digest") or args.digest
        cover = params.get("cover") or args.cover
        content_path = params.get("content") or params.get("md") or args.content or args.md
    else:
        title = args.title
        author = args.author
        digest = args.digest
        cover = args.cover
        content_path = args.content or args.md

    if not title:
        raise Exception("缺少 --title 或 --params")
    if not cover:
        raise Exception("缺少 --cover")
    if not content_path:
        raise Exception("缺少 --content 或 --md")

    print("=" * 50)
    print("wechat_publish.py start")
    print("=" * 50)

    token = get_token()
    print("[OK] Token: {}...".format(token[:10]))

    thumb_id = upload_material(token, cover)
    print("[OK] thumb_id: {}".format(thumb_id))

    content = read_content(content_path)
    print("[OK] content bytes: {}".format(len(content)))

    draft_id = create_draft(token, title, author, digest, content, thumb_id)
    print("[OK] draft_id: {}".format(draft_id))

    print("=" * 50)
    print("DONE")
    print("=" * 50)

if __name__ == "__main__":
    main()