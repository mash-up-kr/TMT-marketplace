# People And Atlassian Accounts

Volatile org data for the team. Edit this file (not `spec.md`) when a member, accountId, displayName, or alias changes. `spec.md` owns the policy that uses this table; this file owns the data.

| Name | Atlassian displayName | Jira accountId | Aliases / common STT errors |
|---|---|---|---|
| 이창우 | changchangwoo119 | `712020:69ebe92d-f78e-4b83-9c45-639435e36b74` | 창후, 창호, 창우 형, 창호영 |
| 이준표 | Dradnats | `712020:cdb6b0e7-8a68-4e9d-9d79-511f92898ad6` | 준표, 준포, dradnats |
| 이서원 | 이서원 | `712020:04061ce9-2704-419e-bbb9-b8f8d7512f8f` | 서원, 서원님 |
| 하아얀 | 하아얀 | `712020:19ac4adb-ae00-41f7-810b-3bea326a0172` | 아연, 아얀, 하얀, 하아얀 언니 |
| 장정우 | 장정우 | `712020:7a4a319d-e043-4edc-8378-e0e5353c8717` | 정우, 장정후 |
| 임준형 | 임준형 | `712020:aaabb651-1817-46ef-96b5-e759b841fad5` | 준형, 임준영 |
| 정혜인 | hyein396 | `712020:c165ade4-ad82-416f-b24e-8d96ebd3e732` | 혜인, 해인, hyein396 |
| 장민서 | Minseo Jang | `712020:eba24041-39c7-46a8-a960-7581cb007de3` | 민서, minseo, minseo jang |

## Account rules

- Prefer the table accountId over fresh lookup.
- Put Jira assignees in `assignee_account_id`, not in display-name fields.
- Use ADF mention with `attrs.id=<accountId>` and `attrs.text=@<displayName>`.
- Use Confluence HTML mention as `<span data-type="mention" data-user-id="<accountId>">@<displayName></span>`.
- If an owner is not in the table or lookup returns multiple candidates, ask the user before Jira creation.
- An alias that could match more than one row (a shared name fragment) must not be auto-assigned — see `spec.md` Name Normalization → Ambiguous tokens.
