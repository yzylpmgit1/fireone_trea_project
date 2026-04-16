#!/usr/bin/env python3
"""Query the latest content of a GitHub repository."""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.github.com"


def github_api_request(path, token=None, params=None):
    url = API_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    request.add_header("User-Agent", "github-latest-query-script")

    try:
        with urllib.request.urlopen(request) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8")
        print(f"GitHub API error: {exc.code} {exc.reason}", file=sys.stderr)
        try:
            error_data = json.loads(message)
            print(error_data.get("message", message), file=sys.stderr)
        except Exception:
            print(message, file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"网络错误: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def format_commit(commit_data):
    sha = commit_data.get("sha")
    commit = commit_data.get("commit", {})
    author = commit.get("author", {})
    author_name = author.get("name", "未知")
    date = author.get("date", "未知")
    message = commit.get("message", "")
    return sha, author_name, date, message


def print_latest_info(owner, repo, branch, token):
    repo_data = github_api_request(f"/repos/{owner}/{repo}", token=token)
    default_branch = repo_data.get("default_branch", branch or "main")
    branch = branch or default_branch

    print("仓库:", repo_data.get("full_name", f"{owner}/{repo}"))
    print("描述:", repo_data.get("description", "(无描述)"))
    print("默认分支:", default_branch)
    print("查询分支:", branch)
    print("Stars:", repo_data.get("stargazers_count", 0))
    print("Forks:", repo_data.get("forks_count", 0))
    print("Open Issues:", repo_data.get("open_issues_count", 0))
    print()

    commits = github_api_request(
        f"/repos/{owner}/{repo}/commits",
        token=token,
        params={"sha": branch, "per_page": 1},
    )
    if not commits:
        print("未能获取最新提交。", file=sys.stderr)
        return

    latest_commit = commits[0]
    sha, author_name, date, message = format_commit(latest_commit)
    print("最新提交:")
    print(f"  SHA: {sha}")
    print(f"  作者: {author_name}")
    print(f"  日期: {date}")
    print(f"  提交信息: {message}")
    print()

    commit_details = github_api_request(
        f"/repos/{owner}/{repo}/commits/{sha}", token=token
    )
    changed_files = commit_details.get("files", [])
    if changed_files:
        print("提交修改文件:")
        for file_info in changed_files:
            status = file_info.get("status", "unknown")
            filename = file_info.get("filename")
            additions = file_info.get("additions", 0)
            deletions = file_info.get("deletions", 0)
            changes = file_info.get("changes", 0)
            print(
                f"  - {filename} ({status}, +{additions}/-{deletions}, 总改动 {changes})"
            )
        print()

    contents = github_api_request(
        f"/repos/{owner}/{repo}/contents",
        token=token,
        params={"ref": branch},
    )
    if isinstance(contents, list):
        print(f"{branch} 分支根目录内容:")
        for entry in contents:
            print(f"  - {entry.get('type', 'file')}: {entry.get('path')}")
    else:
        print("无法读取仓库根目录内容。")


def main():
    parser = argparse.ArgumentParser(description="查询 GitHub 仓库最新内容")
    parser.add_argument("owner", help="GitHub 仓库所有者")
    parser.add_argument("repo", help="GitHub 仓库名")
    parser.add_argument("--branch", help="要查询的分支（默认为默认分支）")
    parser.add_argument(
        "--token",
        help="GitHub 访问令牌（可选，用于提高 API 限额，环境变量 GITHUB_TOKEN 也可用）",
    )
    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    print_latest_info(args.owner, args.repo, args.branch, token)


if __name__ == "__main__":
    import os

    main()
