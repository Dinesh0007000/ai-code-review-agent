def check_security_issues(issue_list):
    issues = []
    for issue in issue_list:
        issues.append({
            "type": "security",
            "message": f"{issue.test_id}: {issue.text}"
        })
    return issues