# Basic ERC4626 properties [1] 

MustNotRevertProps
---
* `asset()` must not revert
* `totalAssets()` must not revert
* `maxDeposit()` must not revert
* `maxMint()` must not revert
* `maxRedeem()` must not revert
* `maxWithdraw()` must not revert


FunctionalAccountingProps
---
* `deposit()` must deduct assets from the owner
* `deposit()` must credit shares to the receiver
* `deposit()` must mint greater than or equal to the number of shares predicted by `previewDeposit()`
* `mint()` must deduct assets from the owner
* `mint()` must credit shares to the receiver
* `mint()` must consume less than or equal to the number of assets predicted by `previewMint()`
* `withdraw()` must deduct shares from the owner
* `withdraw()` must credit assets to the receiver
* `withdraw()` must deduct less than or equal to the number of shares predicted by `previewWithdraw()`
* `redeem()` must deduct shares from the owner
* `redeem()` must credit assets to the receiver
* `redeem()` must credit greater than or equal to the number of assets predicted by `previewRedeem()`

RedeemUsingApprovalProps
---
* `withdraw()` must allow proxies to withdraw tokens on behalf of the owner using share token approvals
* `redeem()` must allow proxies to redeem shares on behalf of the owner using share token approvals
* Third party `withdraw()` calls must update the msg.sender's allowance
* Third party `redeem()` calls must update the msg.sender's allowance
* Third parties must not be able to `withdraw()` tokens on an owner's behalf without a token approval
* Third parties must not be able to `redeem()` shares on an owner's behalf without a token approval

SenderIndependentProps
---
* `maxDeposit()` must assume the receiver/sender has infinite assets
* `maxMint()` must assume the receiver/sender has infinite assets
* `previewMint()` must not account for msg.sender asset balance
* `previewDeposit()` must not account for msg.sender asset balance
* `previewWithdraw()` must not account for msg.sender share balance
* `previewRedeem()` must not account for msg.sender share balance

RoundingProps
---
* Shares may never be minted for free using:
  * `previewDeposit()`
  * `previewMint()`
  * `convertToShares()`

* Tokens may never be withdrawn for free using:
  * `previewWithdraw()`
  * `previewRedeem()`
  * `convertToAssets()`
* Shares may never be minted for free using:
  * `deposit()`
  * `mint()`

* Tokens may never be withdrawn for free using:
  * `withdraw()`
  * `redeem()`

SecurityProps
---
* `decimals()` should be larger than or equal to `asset.decimals()`
* Accounting system must not be vulnerable to share price inflation attacks

* `deposit/mint` must increase `totalSupply/totalAssets`
* `withdraw/redeem` must decrease `totalSupply/totalAssets`


* `previewDeposit()` must not account for vault specific/user/global limits
* `previewMint()` must not account for vault specific/user/global limits
* `previewWithdraw()` must not account for vault specific/user/global limits
* `previewRedeem()` must not account for vault specific/user/global limits


[1] https://github.com/crytic/properties/blob/13a8724f688b201a771a5554fc917b73a818dd95/contracts/ERC4626/README.md?plain=1#L100