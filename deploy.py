# -*- coding: utf-8 -*-
import zipfile
import io
import os
import json
import urllib.request

def create_zip_from_dir(source_dir):
    """把 source_dir 下的文件（index.html + images/）打包成 zip 字节流"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            # 跳过无关目录
            dirs[:] = [d for d in dirs if d not in ('backend', 'frontend', '.git')]
            for fname in files:
                fpath = os.path.join(root, fname)
                # 只保留网页相关文件
                if fname == 'index.html' or root.endswith('images'):
                    arcname = os.path.relpath(fpath, source_dir)
                    zf.write(fpath, arcname)
                    print(f'  [OK] 已添加: {arcname}')
    buf.seek(0)
    return buf

def deploy_to_netlify(zip_buf):
    """通过 Netlify Drop 公开 API 部署 zip 到公网"""
    zip_data = zip_buf.read()
    size = len(zip_data)
    print(f'\n📦 zip 包大小: {size / 1024:.1f} KB')

    url = 'https://api.netlify.com/api/v1/sites'
    req = urllib.request.Request(
        url,
        data=zip_data,
        headers={
            'Content-Type': 'application/zip',
            'User-Agent': 'ximuchacang-deploy'
        },
        method='POST'
    )

    print('🚀 正在部署到公网（Netlify）...')
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            site_url = data.get('url') or data.get('ssl_url')
            site_id = data.get('id')
            print(f'\n✅ 部署成功！')
            print(f'   公网访问地址: {site_url}')
            print(f'   站点 ID: {site_id}')
            print(f'\n💡 提示: 你可以把这个地址分享给任何人，手机/电脑浏览器都能打开')
            print(f'💡 如果想永久保留站点，可在 https://app.netlify.com 登录后认领')
            return site_url
    except urllib.error.HTTPError as e:
        print(f'❌ 部署失败 HTTP {e.code}: {e.read().decode("utf-8")[:500]}')
        return None
    except Exception as e:
        print(f'❌ 部署失败: {e}')
        return None

if __name__ == '__main__':
    source_dir = os.path.dirname(os.path.abspath(__file__))
    print(f'📂 部署目录: {source_dir}')
    zip_buf = create_zip_from_dir(source_dir)
    site_url = deploy_to_netlify(zip_buf)
    if site_url:
        print(f'\n🎯 访问链接: {site_url}')
