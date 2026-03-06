import os
import json
import time
import requests
from github import Github, GithubIntegration

# Add the api directory to sys.path so we can import the core functions
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

# Import the core AI and GitHub functions from index.py
from index import (
    APP_ID, PRIVATE_KEY, GEMINI_API_URL, GEMINI_API_KEY, GROK_API_KEY, GROQ_API_URL, GEMINI2_API_KEY,
    audit_pending_reviews, get_repo_structure, read_file_content, query_gemini_scanner,
    query_groq, extract_json_from_response, apply_surgical_edits, query_gemini_reviewer,
    commit_changes_via_api, update_ai_communication_log
)

def run_cron():
    print("DEBUG: Cron triggered — Triple-AI Pipeline (GitHub Actions)")
    
    try:
        # Initialize GitHub App
        integration = GithubIntegration(APP_ID, PRIVATE_KEY)
        installations = integration.get_installations()
        
        if not installations or installations.totalCount == 0:
            print("DEBUG: No installations found")
            return
        
        installation = installations[0]
        token = integration.get_access_token(installation.id).token
        gh = Github(token)
        
        # === PHASE 0: REVIEWER AUDITS PENDING REVIEWS ===
        print("DEBUG: Phase 0 — Auditing pending reviews")
        audit_pending_reviews(gh)
        
        # === PHASE 0.5: CHECK APPROVED ISSUES ===
        print("DEBUG: Phase 0.5 — Checking for approved issues")
        try:
            bot_repo_name = os.environ.get('BOT_REPO_NAME', 'HOLYKEYZ/mayo')
            bot_repo = gh.get_repo(bot_repo_name)
            mem_file = bot_repo.get_contents("api/global_memory.md")
            mem_content = mem_file.decoded_content.decode('utf-8')
            
            import re as re_mod
            awaiting_entries = re_mod.findall(
                r'\(Ref: (https://github\.com/([^/]+/[^/]+)/issues/(\d+))\) - \*Status: AWAITING JOSEPH\'S INPUT\*',
                mem_content
            )
            
            for issue_url, repo_name, issue_num in awaiting_entries:
                try:
                    issue_repo = gh.get_repo(repo_name)
                    issue = issue_repo.get_issue(int(issue_num))
                    
                    # Check if Joseph replied with approval
                    approval_keywords = ['yes', 'go ahead', 'do it', 'proceed', 'approved', 'fix it', 'go for it', 'yeah', 'yep', 'sure']
                    joseph_approved = False
                    joseph_reply = ""
                    
                    for comment in issue.get_comments():
                        if comment.user.login != 'joe-gemini-bot[bot]':
                            body_lower = comment.body.lower().strip()
                            if any(kw in body_lower for kw in approval_keywords):
                                joseph_approved = True
                                joseph_reply = comment.body
                                break
                    
                    if not joseph_approved:
                        continue
                    
                    print(f"DEBUG: Joseph approved issue {issue_url} — executing!")
                    
                    # Extract the Scanner's original analysis from the issue body
                    scanner_context = issue.body or ""
                    
                    # Gather the repo's code context for the Executor
                    structure = get_repo_structure(issue_repo, max_depth=2)
                    source_files = []
                    try:
                        contents = issue_repo.get_contents("")
                        EXCLUDED_FILES = ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'bun.lockb', '.min.js', '.min.css']
                        for item in contents:
                            if item.type == 'file' and any(item.name.endswith(ext) for ext in ['.py', '.js', '.ts', '.go', '.c', '.cpp', '.h', '.md', '.json']):
                                if not any(excl in item.name for excl in EXCLUDED_FILES):
                                    source_files.append(item.path)
                    except:
                        pass
                    
                    import random
                    random.shuffle(source_files)
                    target_paths = source_files[:10]
                    file_contents = ""
                    for tp in target_paths:
                        content = read_file_content(issue_repo, tp)
                        if content:
                            file_contents += f"\n--- {tp} ---\n{content}\n"
                    
                    if not file_contents:
                        print(f"DEBUG: Could not read files for approved issue {issue_url}")
                        continue
                    
                    ts = int(time.time())
                    target_path_display = ", ".join(target_paths)
                    
                    # Run Executor with Joseph's approval context
                    executor_prompt = (
                        f"You are the EXECUTOR — a Senior Code Engineer.\n"
                        f"Joseph has approved this change via GitHub Issue: {issue.title}\n\n"
                        f"Joseph's reply: \"{joseph_reply}\"\n\n"
                        f"Original Scanner analysis:\n{scanner_context}\n\n"
                        f"Repo: {issue_repo.full_name}\nFiles: {target_path_display}\n"
                        f"Repo structure:\n{structure}\n\n"
                        f"File contents:\n{file_contents}\n\n"
                        f"Execute the approved change. Output strict JSON:\n"
                        f'{{"title": "[TYPE] Brief title", "body": "Description", '
                        f'"branch_name": "bot/issue-{issue_num}-{ts}", '
                        f'"edits": [{{"file": "path", "search": "exact original", "replace": "replacement"}}]}}'
                    )
                    
                    executor_response = query_groq(executor_prompt)
                    if executor_response:
                        improvement_data = extract_json_from_response(executor_response)
                        if improvement_data and 'edits' in improvement_data:
                            
                            file_edits = {}
                            for edit in improvement_data['edits']:
                                fpath = edit.get('file') or (target_paths[0] if target_paths else '')
                                if fpath not in file_edits:
                                    file_edits[fpath] = []
                                file_edits[fpath].append(edit)
                            
                            file_changes = {}
                            for fpath, edits in file_edits.items():
                                content = read_file_content(issue_repo, fpath)
                                if not content:
                                    continue
                                new_content = apply_surgical_edits(content, edits)
                                if new_content != content:
                                    file_changes[fpath] = new_content
                            
                            if file_changes:
                                branch = improvement_data.get('branch_name', f'bot/issue-{issue_num}-{ts}')
                                title = improvement_data.get('title', f'Fix from approved issue #{issue_num}')
                                
                                if commit_changes_via_api(issue_repo, branch, file_changes, title):
                                    pr = issue_repo.create_pull(
                                        title=f"[VALIDATED] {title}",
                                        body=f"Approved by Joseph in {issue_url}\n\n{improvement_data.get('body', '')}\n\n*Executed by Mayo 🤖*",
                                        head=branch,
                                        base=issue_repo.default_branch
                                    )
                                    print(f"DEBUG: PR created from approved issue: {pr.html_url}")
                                    
                                    # Close the issue
                                    issue.create_comment(f"✅ Done! PR created: {pr.html_url}")
                                    issue.edit(state='closed')
                                    
                                    # Update memory
                                    mem_file = bot_repo.get_contents("api/global_memory.md")
                                    mem = mem_file.decoded_content.decode('utf-8')
                                    mem = mem.replace(
                                        f"(Ref: {issue_url}) - *Status: AWAITING JOSEPH'S INPUT*",
                                        f"(Ref: {issue_url}) - *Status: EXECUTED → {pr.html_url}*"
                                    )
                                    bot_repo.update_file("api/global_memory.md", f"feat(memory): executed approved issue on {repo_name}", mem, mem_file.sha)
                except Exception as e:
                    print(f"DEBUG: Error processing approved issue {issue_url}: {e}")
        except Exception as e:
            print(f"DEBUG: Phase 0.5 error: {e}")
        
        # Get all repos via REST API
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        repos_response = requests.get('https://api.github.com/installation/repositories', headers=headers)
        repos_data = repos_response.json()
        repo_names = [r['full_name'] for r in repos_data.get('repositories', [])]
        print(f"DEBUG: Found {len(repo_names)} repos: {repo_names}")
        
        if not repo_names:
            print("No repos found")
            return
        
        # Fetch Global Memory first for priority/cooldown analysis
        bot_repo_name = os.environ.get('BOT_REPO_NAME', 'HOLYKEYZ/mayo')
        print(f"DEBUG: BOT_REPO_NAME = '{bot_repo_name}'")
        try:
            bot_repo = gh.get_repo(bot_repo_name)
            print(f"DEBUG: Successfully accessed bot repo: {bot_repo.full_name}")
            memory_file_obj = bot_repo.get_contents("api/global_memory.md")
            global_memory = memory_file_obj.decoded_content.decode('utf-8')
            print(f"DEBUG: Global memory fetched (len: {len(global_memory)})")
        except Exception as e:
            print(f"DEBUG: PyGithub failed to fetch global memory: {e}")
            # Fallback: try direct REST API
            try:
                mem_url = f"https://api.github.com/repos/{bot_repo_name}/contents/api/global_memory.md"
                mem_resp = requests.get(mem_url, headers=headers)
                print(f"DEBUG: REST API fallback status: {mem_resp.status_code}")
                if mem_resp.status_code == 200:
                    import base64
                    global_memory = base64.b64decode(mem_resp.json()['content']).decode('utf-8')
                    print(f"DEBUG: Global memory fetched via REST (len: {len(global_memory)})")
                else:
                    print(f"DEBUG: REST fallback also failed: {mem_resp.text[:200]}")
                    global_memory = "No global memory found. Start with fresh excellence."
            except Exception as e2:
                print(f"DEBUG: REST fallback exception: {e2}")
                global_memory = "No global memory found. Start with fresh excellence."

        # === REPO SELECTION: Exclusions, Cooldown, Priority ===
        EXCLUDED_REPOS = ['Square-farms', 'Jo-ayanda-real-estate', 'Backend-images-app', 'ecom-stor', 'private-storage']
        
        candidates = [r for r in repos_data.get('repositories', []) 
                      if not r.get('fork') and not r.get('archived') 
                      and r.get('name') not in EXCLUDED_REPOS]
        
        if not candidates:
            print("No eligible repos found")
            return
            
        # Parse last 3 repos from memory for cooldown
        recent_repos = []
        import re as re_mod
        for line in reversed(global_memory.split('\n')):
            match = re_mod.search(r'\*\*Repo: ([^\*]+)\*\*', line)
            if match:
                r_name = match.group(1).strip()
                if r_name not in recent_repos:
                    recent_repos.append(r_name)
                if len(recent_repos) >= 3:
                    break
                    
        # Filter out cooldown repos
        available = [r for r in candidates if r.get('name') not in recent_repos]
        if not available:
            print("DEBUG: All candidates in cooldown. Ignoring cooldown.")
            available = candidates
            
        # Priority Queue: rank by oldest occurrence in memory
        def repo_score(repo):
            return global_memory.rfind(f"**Repo: {repo.get('name')}**")
            
        available.sort(key=repo_score)
        
        # Pick randomly from the top 30% most-needing repos
        import random
        top_k = max(1, len(available) // 3)
        chosen = random.choice(available[:top_k])
        target_repo = gh.get_repo(chosen['full_name'])
        print(f"DEBUG: Targeting repo {target_repo.full_name} (cooldown/priority applied)")

        # Gather codebase context
        structure = get_repo_structure(target_repo, max_depth=2)
        readme_content = read_file_content(target_repo, "README.md") or "(No README found)"
        
        # List source files
        source_files = []
        EXCLUDED_FILES = ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'bun.lockb', '.min.js', '.min.css']
        try:
            contents = target_repo.get_contents("")
            for item in contents:
                if item.type == 'file' and any(item.name.endswith(ext) for ext in ['.py', '.js', '.ts', '.go', '.c', '.cpp', '.h', '.md', '.json']):
                    if not any(excl in item.name for excl in EXCLUDED_FILES):
                        source_files.append(item.path)
            for dirname in ['src', 'api', 'lib', 'app', 'pages']:
                try:
                    dir_contents = target_repo.get_contents(dirname)
                    for item in dir_contents:
                        if item.type == 'file' and any(item.name.endswith(ext) for ext in ['.py', '.js', '.ts', '.go', '.jsx', '.tsx', '.c', '.cpp', '.h', '.md', '.json']):
                            if not any(excl in item.name for excl in EXCLUDED_FILES):
                                source_files.append(item.path)
                except:
                    pass
        except Exception as e:
            print(f"DEBUG: Error listing files: {e}")
        
        if not source_files:
            if readme_content != "(No README found)":
                source_files = ["README.md"]
            else:
                print("No source files found")
                return
        
        # Multi-file support: Pick up to 10 files for deeper architecture context
        import random
        random.shuffle(source_files)
        target_paths = [sf.path if hasattr(sf, 'path') else sf for sf in source_files[:10]]
        
        file_contents = ""
        for tp in target_paths:
            content = read_file_content(target_repo, tp)
            if content:
                file_contents += f"\n--- {tp} ---\n{content}\n"
        
        if not file_contents:
            print("DEBUG: Could not read target files")
            return

        ts = int(time.time())
        target_path_display = ", ".join(target_paths)

        # === PHASE 1: SCANNER (Gemini A) ===
        print(f"DEBUG: Phase 1 — Scanner analyzing {target_path_display}")
        try:
            scanner_path = os.path.join(os.path.dirname(__file__), 'api', 'scanner_prompt.txt')
            with open(scanner_path, 'r') as f:
                scanner_template = f.read()
            
            # Escape curly braces for JSON
            scanner_prompt = scanner_template.replace('{{REPO_NAME}}', target_repo.full_name)\
                                             .replace('{{FILE_PATH}}', target_path_display)\
                                             .replace('{{REPO_STRUCTURE}}', structure)\
                                             .replace('{{README_CONTENT}}', readme_content)\
                                             .replace('{{FILE_CONTENT}}', file_contents)\
                                             .replace('{{GLOBAL_MEMORY}}', global_memory)
        except Exception as e:
            print(f"DEBUG: Failed to load scanner prompt: {e}")
            scanner_prompt = f"Analyze {target_repo.full_name} ({target_path_display}) and recommend one improvement. Text only, no code."
        
        scanner_plan = query_gemini_scanner(scanner_prompt)
        if not scanner_plan:
            print("DEBUG: Scanner returned nothing")
            return
        
        print(f"DEBUG: Scanner plan length: {len(scanner_plan)}")

        # === OPEN_ISSUE DIRECTIVE: Scanner wants human input ===
        if 'DIRECTIVE: OPEN_ISSUE' in scanner_plan:
            print("DEBUG: Scanner requested OPEN_ISSUE — opening GitHub Issue instead of PR")
            try:
                import re as re_mod
                title_match = re_mod.search(r'TITLE:\s*(.+)', scanner_plan)
                body_match = re_mod.search(r'BODY:\s*([\s\S]+?)(?:\n\n##|\Z)', scanner_plan)
                issue_title = title_match.group(1).strip() if title_match else f"🤖 Scanner needs input on {target_repo.name}"
                issue_body = body_match.group(1).strip() if body_match else scanner_plan
                
                owner_login = target_repo.owner.login
                full_body = (
                    f"Hey @{owner_login}! 👋\n\n"
                    f"The Scanner AI found something on **{target_repo.name}** that needs your input before I can proceed.\n\n"
                    f"---\n\n{issue_body}\n\n"
                    f"---\n\n"
                    f"**Please reply with your decision** and I'll pick it up on the next cycle.\n\n"
                    f"*Generated by Mayo 🤖 — Triple-AI Pipeline (Scanner flagged OPEN_ISSUE)*"
                )
                issue = target_repo.create_issue(title=f"🤖 {issue_title}", body=full_body)
                print(f"DEBUG: Issue created: {issue.html_url}")
                
                # Save to memory
                try:
                    bot_repo = gh.get_repo(os.environ.get('BOT_REPO_NAME', 'HOLYKEYZ/mayo'))
                    mem_file = bot_repo.get_contents("api/global_memory.md")
                    old_mem = mem_file.decoded_content.decode('utf-8')
                    note = f"\n- **Repo: {target_repo.name}**: Opened issue — {issue_title}. (Ref: {issue.html_url}) - *Status: AWAITING JOSEPH'S INPUT*"
                    bot_repo.update_file("api/global_memory.md", f"feat(memory): scanner opened issue on {target_repo.name}", old_mem + note, mem_file.sha)
                except Exception as e:
                    print(f"DEBUG: Failed to save issue to memory: {e}")
            except Exception as e:
                print(f"DEBUG: Failed to create issue: {e}")
            return

        # === PHASE 2 & 3: EXECUTOR + REVIEWER (with retry) ===
        max_attempts = 2
        reviewer_feedback = ""
        final_edits = None
        final_title = ""
        final_body = ""
        final_branch = ""
        reviewer_verdict_text = ""

        for attempt in range(1, max_attempts + 1):
            print(f"DEBUG: Phase 2 — Executor attempt {attempt}")
            
            # Load executor prompt
            try:
                executor_path = os.path.join(os.path.dirname(__file__), 'api', 'executor_prompt.txt')
                with open(executor_path, 'r') as f:
                    executor_template = f.read()
                
                executor_prompt = executor_template.replace('{{REPO_NAME}}', target_repo.full_name)\
                                                   .replace('{{FILE_PATH}}', target_path_display)\
                                                   .replace('{{REPO_STRUCTURE}}', structure)\
                                                   .replace('{{SCANNER_PLAN}}', scanner_plan)\
                                                   .replace('{{FILE_CONTENT}}', file_contents)\
                                                   .replace('{{GLOBAL_MEMORY}}', global_memory)\
                                                   .replace('{{TIMESTAMP}}', str(ts))\
                                                   .replace('{{REVIEWER_FEEDBACK}}', reviewer_feedback)
            except Exception as e:
                print(f"DEBUG: Failed to load executor prompt: {e}")
                break
            
            # Llama 3.3 70B executes via Groq
            executor_response = query_groq(executor_prompt)
            if not executor_response:
                print("DEBUG: Executor returned nothing")
                break
            
            print(f"DEBUG: Executor response length: {len(executor_response)}")
            improvement_data = extract_json_from_response(executor_response)
            
            if not improvement_data or 'edits' not in improvement_data:
                print("DEBUG: No valid improvement JSON from Executor")
                break

            # === PHASE 3: REVIEWER (Gemini B) — validates ACTUAL DIFF ===
            print(f"DEBUG: Phase 3 — Reviewer validating attempt {attempt}")
            
            # Pre-apply edits to compute a real diff for the Reviewer
            proposed_edits = improvement_data.get('edits', [])
            diff_preview = ""
            for edit in proposed_edits:
                fpath = edit.get('file') or target_paths[0]
                original = read_file_content(target_repo, fpath) or ""
                patched = apply_surgical_edits(original, [edit])
                if patched != original:
                    orig_lines = original.splitlines()
                    new_lines = patched.splitlines()
                    lines_removed = len(orig_lines) - len(new_lines)
                    diff_preview += f"\n--- {fpath} (original: {len(orig_lines)} lines → patched: {len(new_lines)} lines, net: {'+' if lines_removed < 0 else '-'}{abs(lines_removed)})\n"
                    # Show what was removed/added
                    for line in orig_lines:
                        if line not in new_lines:
                            diff_preview += f"- {line[:120]}\n"
                    for line in new_lines:
                        if line not in orig_lines:
                            diff_preview += f"+ {line[:120]}\n"
                else:
                    diff_preview += f"\n--- {fpath}: NO CHANGES (search block not found or blocked by safety guard)\n"
            
            try:
                reviewer_path = os.path.join(os.path.dirname(__file__), 'api', 'reviewer_prompt.txt')
                with open(reviewer_path, 'r') as f:
                    reviewer_template = f.read()
                
                reviewer_prompt = reviewer_template.replace('{{REPO_NAME}}', target_repo.full_name)\
                                                   .replace('{{FILE_PATH}}', target_path_display)\
                                                   .replace('{{FILE_CONTENT}}', file_contents)\
                                                   .replace('{{PROPOSED_EDITS}}', json.dumps(proposed_edits))\
                                                   .replace('{{SCANNER_PLAN}}', scanner_plan)\
                                                   .replace('{{GLOBAL_MEMORY}}', global_memory)
                # Append the actual diff so Reviewer sees real impact
                reviewer_prompt += f"\n\n## ACTUAL DIFF PREVIEW (what will be committed):\n{diff_preview}\n\nIMPORTANT: If the diff shows more lines removed than expected, REJECT the edit. The Executor's search block may be matching too broadly."
            except Exception as e:
                print(f"DEBUG: Failed to load reviewer prompt: {e}")
                final_edits = improvement_data.get('edits', [])
                final_title = improvement_data.get('title', 'Automated improvement')
                final_body = improvement_data.get('body', '')
                final_branch = improvement_data.get('branch_name', f'bot/fix-{ts}')
                break
            
            reviewer_response = query_gemini_reviewer(reviewer_prompt)
            if not reviewer_response:
                print("DEBUG: Reviewer returned nothing, using Executor's edits as-is")
                final_edits = improvement_data.get('edits', [])
                final_title = improvement_data.get('title', 'Automated improvement')
                final_body = improvement_data.get('body', '')
                final_branch = improvement_data.get('branch_name', f'bot/fix-{ts}')
                reviewer_verdict_text = "Reviewer unavailable — used Executor's edits directly"
                break
            
            reviewer_data = extract_json_from_response(reviewer_response)
            
            if not reviewer_data:
                print("DEBUG: Could not parse Reviewer JSON, using Executor's edits")
                final_edits = improvement_data.get('edits', [])
                final_title = improvement_data.get('title', 'Automated improvement')
                final_body = improvement_data.get('body', '')
                final_branch = improvement_data.get('branch_name', f'bot/fix-{ts}')
                reviewer_verdict_text = "Reviewer response unparseable"
                break
            
            verdict = reviewer_data.get('verdict', 'REJECT').upper()
            reviewer_verdict_text = f"{verdict}: {reviewer_data.get('reason', 'No reason given')}"
            print(f"DEBUG: Reviewer verdict: {verdict}")
            
            if verdict == 'APPROVE':
                final_edits = improvement_data.get('edits', [])
                final_title = improvement_data.get('title', 'Automated improvement')
                final_body = improvement_data.get('body', '')
                final_branch = improvement_data.get('branch_name', f'bot/fix-{ts}')
                break
            elif verdict == 'CORRECT':
                corrected = reviewer_data.get('corrected_edits', improvement_data.get('edits', []))
                
                # Verify the Reviewer's corrections actually work and pass safety guards
                valid_corrections = False
                for edit in corrected:
                    fpath = edit.get('file') or target_paths[0]
                    original = read_file_content(target_repo, fpath) or ""
                    if apply_surgical_edits(original, [edit]) != original:
                        valid_corrections = True
                        break
                
                if not valid_corrections:
                    print("DEBUG: Reviewer's corrected edits failed safety guards or found no matches. Aborting.")
                    final_edits = []  # Clear edits so no PR is made
                    reviewer_verdict_text = "CORRECT (but corrected edits failed safety checks)"
                    break
                
                final_edits = corrected
                final_title = improvement_data.get('title', 'Automated improvement')
                final_body = improvement_data.get('body', '')
                final_branch = improvement_data.get('branch_name', f'bot/fix-{ts}')
                break
            elif verdict == 'REJECT':
                reviewer_feedback = reviewer_data.get('feedback_for_executor', 'Your edits were rejected. Try smaller, safer changes.')
                # Save rejection to memory
                memory_note = reviewer_data.get('memory_note', f'Rejected edit on {target_repo.name}')
                try:
                    bot_repo = gh.get_repo(os.environ.get('BOT_REPO_NAME', 'HOLYKEYZ/mayo'))
                    mem_file = bot_repo.get_contents("api/global_memory.md")
                    mem_content = mem_file.decoded_content.decode('utf-8')
                    mem_content += f"\n- **REJECTED by Reviewer**: {memory_note}"
                    bot_repo.update_file("api/global_memory.md", f"feat(memory): reviewer rejected edit on {target_repo.name}", mem_content, mem_file.sha)
                except Exception as e:
                    print(f"DEBUG: Failed to save rejection to memory: {e}")
                
                if attempt == max_attempts:
                    print("DEBUG: Max attempts reached, skipping PR")
                    # Log the failed cycle
                    update_ai_communication_log(gh, ts, scanner_plan or "", executor_response or "", f"REJECTED x{max_attempts}: {reviewer_feedback}")
                    return
                continue

        if not final_edits:
            print("DEBUG: No valid edits after pipeline")
            return

        # Group edits by file
        file_edits = {}
        for edit in final_edits:
            # Fallback to the first target path if the AI forgot the file field
            fpath = edit.get('file') or target_paths[0]
            if fpath not in file_edits:
                file_edits[fpath] = []
            file_edits[fpath].append(edit)
            
        file_changes = {}
        for fpath, edits in file_edits.items():
            content = read_file_content(target_repo, fpath)
            if not content:
                print(f"DEBUG: Could not read {fpath} for edits")
                continue
            new_content = apply_surgical_edits(content, edits)
            if new_content != content:
                file_changes[fpath] = new_content
        
        if not file_changes:
            print("DEBUG: No changes applied after surgical edits (search failed or no valid files)")
            return

        # Create PR
        print(f"DEBUG: Creating branch {final_branch} with validated edits for {list(file_changes.keys())}")
        success = commit_changes_via_api(target_repo, final_branch, file_changes, final_title)
        
        if success:
            owner_login = target_repo.owner.login
            pr = target_repo.create_pull(
                title=f"[VALIDATED] {final_title}",
                body=f"Hey @{owner_login}! Joseph, I've found an improvement for you.\n\n{final_body}\n\n---\n*Validated by Triple-AI: Scanner (Gemini 2.5 Flash) → Executor (Llama 3.3 70B) → Reviewer (Gemini 2.5 Flash)*\n\nGenerated autonomously by Mayo 🤖",
                head=final_branch,
                base=target_repo.default_branch
            )
            
            try:
                pr.add_to_assignees(owner_login)
                pr.create_review_request(reviewers=[owner_login])
            except Exception as e:
                print(f"DEBUG: Failed to assign/request review: {e}")

            print(f"DEBUG: PR created: {pr.html_url}")
            
            # Save to memory
            try:
                bot_repo = gh.get_repo(os.environ.get('BOT_REPO_NAME', 'HOLYKEYZ/mayo'))
                old_memory_file = bot_repo.get_contents("api/global_memory.md")
                old_memory = old_memory_file.decoded_content.decode('utf-8')
                lesson = f"\n- **Repo: {target_repo.name}**: {final_title}. (Ref: {pr.html_url}) - *Status: PENDING REVIEW*"
                bot_repo.update_file(
                    "api/global_memory.md",
                    f"feat(memory): record lesson from {target_repo.name}",
                    old_memory + lesson,
                    old_memory_file.sha
                )
            except Exception as e:
                print(f"DEBUG: Failed to update memory: {e}")
            
            # Log the successful cycle
            update_ai_communication_log(gh, ts, scanner_plan or "", executor_response or "", reviewer_verdict_text)

            print("SUCCESS")
        else:
            print("DEBUG: Commit failed")
        
    except Exception as e:
        print(f"Cron error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_cron()
