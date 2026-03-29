# mayo Global Memory & Experience

- *[ARCHIVED] 1 older lessons were archived to preserve focus.*
- **Repo: git-pulse**: [LOGIC] Enhance Error Handling and Type Safety in Notifications Page. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/62) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor incorrectly moved an existing import (`getLanguageColor`) instead of adding a new function (`formatRelativeTime`) to the correct utility import (`@/lib/utils`), leading to a functional error. This is a recurring issue with import management and `ReferenceError`s.
- **Repo: git-pulse**: [FEAT] Enhance RepoCard with Relative Time Formatting. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/63) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor submitted duplicate edits, used an imprecise search block that led to destructive deletion of existing logic, and introduced indentation errors in `git-pulse/test_graphql_contributions.ts`. Recurring issues.
- **Repo: git-pulse**: [DX] Enhance test_graphql_contributions.ts with Configurable GitHub Username. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/64) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [FEAT] Add View All Links for Truncated Search Results. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/65) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor submitted duplicate and conflicting edits for `git-pulse`, one of which was destructive (replacing an existing function instead of appending a new one). Also, inconsistent implementation of the new function across edits.
- **REJECTED by Reviewer**: Executor failed to append a new function using `search: ""`, resulting in 'NO CHANGES'. This confirms `search: ""` is unsuitable for insertions and leads to patching failures.
- **Repo: git-pulse**: [LOGIC] Fix GitHub Repositories API Route Pagination. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/66) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [LOGIC] Correct params type and await usage in comments API route. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/68) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [REFACTOR] Centralize Custom Colors in Tailwind Config. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/70) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [REFACTOR] Enhance Type Safety in Auth JWT Callback. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/71) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [LOGIC] Optimize User Identification in Authenticated API Routes. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/72) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [PERF] Implement In-Memory Cache for GitHub Contributions. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/73) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [PERF] Fix Ineffective LRU Cache in Trending Tags Page. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/74) - *Status: APPROVED - Joseph liked this!*
- **Joseph's Feedback on IntellectSafe#18**: "push your fix , mayo" — Mayo acknowledged and responded.
- **Repo: git-pulse**: [REFACTOR] Centralize Post Mapping Logic. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/75) - *Status: COMMENTED - Joseph had feedback*
- **Repo: git-pulse**: [LOGIC] Fix Conditional Rendering of View All Links. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/76) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [REFACTOR] Centralize Scoring Parameters in calculatePostScore. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/77) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor failed to create a new file using `search: ""`, failed to apply a second edit due to an incorrect search block (search == replace), and introduced indentation errors and missing imports, leading to an incomplete and broken change for `git-pulse`. Recurring issues.
- **REJECTED by Reviewer**: Executor failed to create new file `apps/web/src/types/github.ts` using `search: ""`, leading to `ReferenceError` in dependent files. Confirms `search: ""` is unreliable for file creation/insertion in `git-pulse`.
- **REJECTED by Reviewer**: Executor failed to apply a critical `tailwind.config.ts` update due to search block mismatch, leading to an incomplete and non-functional change for `git-pulse`. This is a recurring issue.
- **Repo: git-pulse**: [REFACTOR] Centralize Custom Colors in RepoCard. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/78) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [REFACTOR] Centralize Custom Colors in RightSidebar. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/79) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [REFACTOR] Ensure Consistent Return Types for List-Fetching Functions. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/80) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [LOGIC] Fix userId in Reaction Creation. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/81) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor failed due to search block mismatch (indentation), introduced indentation errors, and submitted duplicate edits for `git-pulse`. This is a recurring issue.
- **Repo: git-pulse**: [LOGIC] Consistent Styling for NotificationBell. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/82) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor introduced a functional error by not updating all references to a variable after changing its type, and submitted duplicate edits for `git-pulse`.
- **REJECTED by Reviewer**: Executor failed to implement sliding window rate limit correctly by omitting `tokenCache.set` after incrementing count, leading to functional error in `git-pulse`.
- **Repo: git-pulse**: [REFACTOR] Correct Type Definition and Remove Redundant Await in page.tsx. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/83) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [REFACTOR] Unify Timestamp Formatting in FeedClient. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/84) - *Status: COMMENTED - Joseph had feedback*
- **Joseph's Feedback on git-pulse#84**: "mayo , see gemini's reccomendations?
implement it asap" — Mayo acknowledged and responded.
- **Joseph's Feedback on git-pulse#84**: "try again" — Mayo acknowledged and responded.
- **Joseph's Feedback on git-pulse#78**: "mayo ?" — Mayo acknowledged and responded.
- **Repo: git-pulse**: [REFACTOR] Enhance TypeScript Configuration for Path Aliases. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/85) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [SEC] Validate User Status Input. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/87) - *Status: APPROVED - Joseph liked this!*
<!-- LAST_DISCUSSION_REPLY=1774768090 -->
- **REJECTED by Reviewer**: Executor failed to create new file and insert import using `search: ""` for `git-pulse`, confirming previous rejections for this repo due to unreliable patching for file creation/insertion.
- **REJECTED by Reviewer**: Executor failed to create a new file `apps/web/src/lib/constants.ts` using `search: ""`, leading to a `ReferenceError` in `stars/page.tsx`. This confirms `search: ""` is unreliable for file creation/insertion in `git-pulse`.
- **Repo: git-pulse**: [REFACTOR] Remove Redundant Conditional Check in CollabWidget. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/88) - *Status: APPROVED - Joseph liked this!*
<!-- LAST_PROACTIVE_ISSUE=1774723533 -->
- **Repo: git-pulse**: Automated improvement. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/90) - *Status: APPROVED - Joseph liked this!*
<!-- LAST_ISSUE_JUDGE=1774752153 -->
- **Repo: git-pulse**: [PERF] Optimize findSimilarDevs Function. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/91) - *Status: APPROVED - Joseph liked this!*
- **Joseph's Feedback on git-pulse#90**: "what is this??
just what the hell, mayo ??" — Mayo acknowledged and responded.
- **Joseph's Feedback on git-pulse#90**: "wth is this @gemini-code-assist ?" — Mayo acknowledged and responded.
- **REJECTED by Reviewer**: Executor failed to correctly identify blocks for deletion vs. replacement, leading to duplicate code and redeclared variables. Also, `search: ""` continues to be unreliable for insertions in `git-pulse`, causing critical edits to fail.
- **Repo: git-pulse**: [LOGIC] Fix Critical Bugs in Algorithm Scoring. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/92) - *Status: COMMENTED - Joseph had feedback*
- **Joseph's Feedback on git-pulse#92**: "mayo , do this" — Mayo acknowledged and responded.
- **Repo: git-pulse**: [FEAT] Enhance Markdown Link Generation for Hashtags and Mentions. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/93) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor failed to apply a critical logic fix due to patching failure, despite an apparent exact search match. This is a recurring 'NO CHANGES' issue for `git-pulse`.
- **REJECTED by Reviewer**: Executor's proposed edit was correct and aligned, but the patching mechanism failed to apply the change, resulting in 'NO CHANGES' for `git-pulse`. This is a recurring issue with patching even for exact search matches.
- **Repo: git-pulse**: [LOGIC] Fix lastCheckedTime Logic in SSE Feed Stream. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/94) - *Status: PENDING REVIEW*
- **REJECTED by Reviewer**: Executor failed to delete a function due to patching failure and introduced syntax errors by placing imports incorrectly within a `const` declaration in `git-pulse`. Also missed a required import.
- **REJECTED by Reviewer**: Executor failed to delete a function in `git-pulse` due to patching failure, despite an apparent exact search match. This is a recurring 'NO CHANGES' issue for this repo.
<!-- LAST_PR_JUDGE=1774761197 -->
- **Repo: git-pulse**: [LOGIC] Enhance Error Logging for GitHub API Sync Failures. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/95) - *Status: PENDING REVIEW*
- **REJECTED by Reviewer**: Executor failed to correctly patch `tailwind.config.ts` by using an imprecise search block that led to destructive overwriting of existing color definitions, a recurring issue for `git-pulse`.