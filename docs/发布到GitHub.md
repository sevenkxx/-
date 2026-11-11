# 发布到 GitHub（私有仓库）

仓库已经在本地建好并提交了，路径：

```
~/Desktop/WorkBuddy/奶龙鼠标指针主题
```

只剩「推到 GitHub」这一步。以下全部在图形界面点，不用命令行。

## 一、装 GitHub Desktop

1. 双击 `~/Downloads/GitHubDesktop-osx-universal.dmg`
2. 把 **GitHub Desktop** 图标拖进 `Applications` 文件夹
3. 打开它，选 **Sign in to GitHub.com**，浏览器会弹出授权页，点 **Authorize**

> 没有 GitHub 账号就先在 github.com 注册一个，免费。

## 二、把本地仓库加进去

1. 菜单 **File → Add Local Repository…**
2. 路径选 `~/Desktop/WorkBuddy/奶龙鼠标指针主题`
3. 它会认出这是一个已有仓库，直接点 **Add Repository**

此时左侧会出现这个仓库，History 里已经有一条提交：  
`奶龙鼠标指针主题 v2.2：18 状态 MaCursor 主题包`

## 三、发布成私有仓库

1. 右上角点 **Publish repository**
2. 填 Name：`nailoong-cursor-theme`（Description 随意）
3. **把 "Keep this code private" 勾上** ← 关键，别漏
4. 点 **Publish repository**

完成。地址会是 `https://github.com/你的用户名/nailoong-cursor-theme`。

## 四、以后怎么分享给别人

私有仓库别人打不开。三种给法：

**A. 直接发文件（最省事，推荐）**
从 Finder 里把这个文件发过去（微信 / 邮件 / AirDrop 都行）：

```
themes/奶龙鼠标指针-官方动作扩展版-v2.2.cursor
```

对方双击 → MaCursor 自动导入 → 选中应用。前提是 macOS 13+ 且装了 MaCursor。

**B. 加协作者**
GitHub 仓库页 → **Settings → Collaborators → Add people**，填对方 GitHub 用户名。对方接受邀请后能看整个仓库。

**C. 打一个 zip 发过去**
想连预览图和说明一起给，右键仓库文件夹 → 压缩。但注意 `.git` 目录会让体积翻倍，压缩前可以先复制一份再删掉 `.git`。

## 五、以后改了主题怎么更新

改完文件后，GitHub Desktop 会自动列出改动：

1. 左下角填一句 Summary（比如「调整为 10 帧」）
2. 点 **Commit to main**
3. 点右上角 **Push origin**

就同步到 GitHub 了。
