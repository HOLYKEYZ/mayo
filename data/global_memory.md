# mayo Global Memory & Experience

- *[ARCHIVED] 1 older lessons were archived to preserve focus.*
- **Repo: git-pulse**: [LOGIC] Correct params type in reactions/route.ts. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/54) - *Status: APPROVED - Joseph liked this!*
<!-- LAST_PROACTIVE_ISSUE=1774712118 -->
- **Repo: git-pulse**: [LOGIC] Distinguish Between No Repositories and Fetch Error. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/56) - *Status: APPROVED - Joseph liked this!*
<!-- LAST_ISSUE_JUDGE=1774715941 -->
- **Repo: git-pulse**: [FEAT] Enhance Star Reaction Icon in ReactionPicker. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/57) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [REFACTOR] Centralize Thresholds and Standardize Timestamps. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/58) - *Status: APPROVED - Joseph liked this!*
<!-- LAST_PR_JUDGE=1774702862 -->
- **REJECTED by Reviewer**: Executor failed to apply most edits due to search block mismatches, specifically `let` vs `const` and large JSX blocks, leading to 'NO CHANGES' for `git-pulse`. This is a recurring issue.
- **REJECTED by Reviewer**: Executor's JSON for replacement was correct, but the 'ACTUAL DIFF PREVIEW' showed an extraneous `)}` causing a syntax error in `repos/page.tsx`. This indicates a patching or diff generation issue.
- **REJECTED by Reviewer**: Executor failed to apply a critical logic fix due to search block mismatch, a recurring issue for `git-pulse`.
- **REJECTED by Reviewer**: Executor failed to apply a critical logic fix due to search block mismatch in `apps/web/src/app/page.tsx`, a recurring issue for `git-pulse`.
- **Repo: git-pulse**: [LOGIC] Correct Accessibility and Semantic Meaning of GrabberIcon in PinnedRepos. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/59) - *Status: APPROVED - Joseph liked this!*
- **REJECTED by Reviewer**: Executor failed to match JSX conditional rendering block due to missing wrapper div in search, and introduced a functional error by removing the div key={n.id} wrapper in the replacement, leading to a syntactically broken patch for git-pulse. Recurring search block mismatch and functional error issue.
- **Repo: git-pulse**: [SEC] Validate Notification Link URLs. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/60) - *Status: APPROVED - Joseph liked this!*
- **Repo: git-pulse**: [LOGIC] Minor JSX Return Syntax Improvement. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/61) - *Status: APPROVED - Joseph liked this!*
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
- **Repo: git-pulse**: [REFACTOR] Enhance TypeScript Configuration for Path Aliases. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/85) - *Status: PENDING REVIEW*
- **Repo: git-pulse**: [SEC] Validate User Status Input. (Ref: https://github.com/HOLYKEYZ/git-pulse/pull/87) - *Status: PENDING REVIEW*