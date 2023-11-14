# ERC4626 Inflation Attack

This folder contains Certora CVL specification for the [inflation attack](https://tienshaoku.medium.com/eip-4626-inflation-sandwich-attack-deep-dive-and-how-to-solve-it-9e3e320cc3f1) on ERC4626. 

The verification is checked against OpenZeppelin's [implementation of ERC4626](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/ERC4626.sol).

In this folders there are two commits, a variant that contains the bug (commit d5d9d4b) and a variant where the fix has been applied (commit d64d7aa).


# About the CVL specs
The [specifications](InflationAttack/certora/spec/ERC4626-InflationAttack.spec) contain two rules. A CVL rule that step-by-step models inflation attack as described in the blog bost by 田少谷 Shao. But there is also a second rule, that is way simple but also detects the bug. 