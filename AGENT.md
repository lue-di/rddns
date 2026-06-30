# 版本管理流程

版本号完全由 **git tag** 管理，没有 VERSION 文件，没有硬编码。

## 数据流

```
git tag v0.2.12
    ↓ CI (docker build --build-arg VERSION=0.2.12)
    ↓ Dockerfile → echo "0.2.12" > /rddns/VERSION
    ↓ main.py → 读取 VERSION 文件
    ↓ 输出 "RDDNS Version: V0.2.12"
```

## 查看版本

```bash
# 查看所有 tag
git tag --list

# 本地运行（无 VERSION 文件时自动从 git tag 获取）
python main.py
# RDDNS Version: V0.2.11
```

## 更新版本

### 日常推送（自动 bump patch）

```bash
git add .
git commit -m "fix: something"
git push
```

CI 自动：读取最新 tag → bump patch → 创建新 tag → 构建 Docker 镜像。

### 手动升级 minor / major

GitHub 网页 → **Actions** → **Build and Release** → **Run workflow** → 选择 `minor` 或 `major`。

### 本地创建 tag 再推送

```bash
git tag v0.3.0
git push origin v0.3.0
```

推送后 CI 基于新 tag 继续自动 bump。

## 初始化（首次部署）

```bash
git push origin <initial-tag>
git push
```
