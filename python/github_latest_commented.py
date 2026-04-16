#!/usr/bin/env python3  # 指定脚本使用系统环境中的 Python3 解释器执行
"""查询 GitHub 仓库最新内容的脚本，包含详细中文注释。"""  # 模块说明

import argparse  # 处理命令行参数
import json  # 处理 JSON 数据
import os  # 访问操作系统环境变量
import sys  # 获取标准输入输出和退出状态
import urllib.error  # 处理 URL 请求错误
import urllib.parse  # 编码 URL 查询参数
import urllib.request  # 发送 HTTP 请求

# GitHub API 的基础 URL
API_BASE = "https://api.github.com"


def github_api_request(path, token=None, params=None):
    """向 GitHub API 发送请求并返回 JSON 结果。"""
    url = API_BASE + path  # 拼接请求 URL
    if params:
        url += "?" + urllib.parse.urlencode(params)  # 将参数编码为查询字符串

    request = urllib.request.Request(url)  # 构造请求对象
    request.add_header("Accept", "application/vnd.github+json")  # 请求 GitHub JSON 格式
    if token:
        request.add_header("Authorization", f"Bearer {token}")  # 如果有 token 传入则添加授权头

    request.add_header("User-Agent", "github-latest-query-script")  # GitHub 要求设置 User-Agent

    try:
        with urllib.request.urlopen(request) as response:  # 发送请求并接收响应
            data = response.read().decode("utf-8")  # 读取响应内容并解码为字符串
            return json.loads(data)  # 将 JSON 字符串解析为 Python 对象
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8")  # 读取错误响应内容
        print(f"GitHub API error: {exc.code} {exc.reason}", file=sys.stderr)  # 打印 HTTP 错误代码
        try:
            error_data = json.loads(message)  # 尝试解析 GitHub 返回的错误 JSON
            print(error_data.get("message", message), file=sys.stderr)  # 打印错误信息
        except Exception:
            print(message, file=sys.stderr)  # 如果解析失败则打印原始错误内容
        sys.exit(1)  # 退出程序，返回非零状态
    except urllib.error.URLError as exc:
        print(f"网络错误: {exc.reason}", file=sys.stderr)  # 打印网络异常信息
        sys.exit(1)  # 退出程序，返回非零状态


def format_commit(commit_data):
    """从提交对象中提取常用字段。"""
    sha = commit_data.get("sha")  # 提交 SHA
    commit = commit_data.get("commit", {})  # 提取 commit 字段
    author = commit.get("author", {})  # 提取作者信息
    author_name = author.get("name", "未知")  # 作者名称，若缺失则用“未知"
    date = author.get("date", "未知")  # 提交日期，若缺失则用“未知"
    message = commit.get("message", "")  # 提交信息
    return sha, author_name, date, message  # 返回解析后的提交数据


def print_latest_info(owner, repo, branch, token):
    """查询仓库信息、最新提交和根目录内容，并打印结果。"""
    repo_data = github_api_request(f"/repos/{owner}/{repo}", token=token)  # 获取仓库详细信息
    default_branch = repo_data.get("default_branch", branch or "main")  # 获取默认分支
    branch = branch or default_branch  # 如果没有指定分支，则使用默认分支

    print("仓库:", repo_data.get("full_name", f"{owner}/{repo}"))  # 打印仓库全名
    print("描述:", repo_data.get("description", "(无描述)"))  # 打印仓库描述
    print("默认分支:", default_branch)  # 打印默认分支
    print("查询分支:", branch)  # 打印实际查询的分支
    print("Stars:", repo_data.get("stargazers_count", 0))  # 打印 star 数
    print("Forks:", repo_data.get("forks_count", 0))  # 打印 fork 数
    print("Open Issues:", repo_data.get("open_issues_count", 0))  # 打印打开 issue 数
    print()  # 空行分隔输出

    commits = github_api_request(
        f"/repos/{owner}/{repo}/commits",
        token=token,
        params={"sha": branch, "per_page": 1},
    )  # 查询指定分支的最新提交
    if not commits:
        print("未能获取最新提交。", file=sys.stderr)  # 如果没有返回提交，则输出错误
        return  # 结束函数

    latest_commit = commits[0]  # 取第一条最新提交
    sha, author_name, date, message = format_commit(latest_commit)  # 解析提交数据
    print("最新提交:")  # 打印段落标题
    print(f"  SHA: {sha}")  # 打印提交 SHA
    print(f"  作者: {author_name}")  # 打印提交作者
    print(f"  日期: {date}")  # 打印提交日期
    print(f"  提交信息: {message}")  # 打印提交信息
    print()  # 空行分隔输出

    commit_details = github_api_request(
        f"/repos/{owner}/{repo}/commits/{sha}", token=token
    )  # 查询指定提交的详细信息
    changed_files = commit_details.get("files", [])  # 获取提交变更的文件列表
    if changed_files:
        print("提交修改文件:")  # 打印更改文件标题
        for file_info in changed_files:
            status = file_info.get("status", "unknown")  # 文件状态
            filename = file_info.get("filename")  # 文件路径
            additions = file_info.get("additions", 0)  # 增加行数
            deletions = file_info.get("deletions", 0)  # 删除行数
            changes = file_info.get("changes", 0)  # 总改动行数
            print(
                f"  - {filename} ({status}, +{additions}/-{deletions}, 总改动 {changes})"
            )  # 打印文件变更摘要
        print()  # 空行分隔输出

    contents = github_api_request(
        f"/repos/{owner}/{repo}/contents",
        token=token,
        params={"ref": branch},
    )  # 查询仓库根目录内容
    if isinstance(contents, list):
        print(f"{branch} 分支根目录内容:")  # 当返回列表时，说明读取成功
        for entry in contents:
            print(f"  - {entry.get('type', 'file')}: {entry.get('path')}")  # 打印每个根目录项类型和路径
    else:
        print("无法读取仓库根目录内容。")  # 处理无法读取根目录的情况


def main():
    """命令行入口，解析参数并调用查询函数。"""
    parser = argparse.ArgumentParser(description="查询 GitHub 仓库最新内容")  # 创建参数解析器
    parser.add_argument("owner", help="GitHub 仓库所有者")  # 必填仓库所有者参数
    parser.add_argument("repo", help="GitHub 仓库名")  # 必填仓库名参数
    parser.add_argument("--branch", help="要查询的分支（默认为默认分支）")  # 可选分支参数
    parser.add_argument(
        "--token",
        help="GitHub 访问令牌（可选，用于提高 API 限额，环境变量 GITHUB_TOKEN 也可用）",
    )  # 可选 token 参数
    args = parser.parse_args()  # 解析命令行参数

    token = args.token or os.environ.get("GITHUB_TOKEN")  # 优先使用命令行 token，否则读取环境变量
    print_latest_info(args.owner, args.repo, args.branch, token)  # 调用主查询函数


if __name__ == "__main__":
    main()  # 如果脚本直接执行，则运行 main()
